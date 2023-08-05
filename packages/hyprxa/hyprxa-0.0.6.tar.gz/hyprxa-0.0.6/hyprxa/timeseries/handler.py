import logging
import queue
import sys
import threading
from collections.abc import Iterable
from dataclasses import asdict
from datetime import datetime
from typing import Any

import pymongo
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import BulkWriteError, OperationFailure

from hyprxa.timeseries.models import TimeseriesDocument
from hyprxa.util.models import StorageHandlerInfo, WorkerInfo
from hyprxa.util.mongo import MongoWorker



_LOGGER = logging.getLogger("hyprxa.timeseries.db")


class TimeseriesWorker(MongoWorker):
    """Manages the submission of timeseries samples to MongoDB in a background
    thread.
    """
    def __init__(self, **kwargs: Any) -> None:
        self._expire_after = kwargs.pop("expire_after")
        super().__init__(**kwargs)

    @staticmethod
    def default_collection_name() -> str:
        return "timeseries"

    def send(self, client: MongoClient, exiting: bool = False) -> None:
        done = False

        max_batch_size = self._buffer_size

        db = client[self._database_name]
        try:
            collection = Collection(db, self._collection_name)
            collection.create_index(
                [
                    ("timestamp", pymongo.ASCENDING),
                    ("subscription", pymongo.ASCENDING),
                    ("source", pymongo.ASCENDING)
                ],
                unique=True
            )
            collection.create_index("expire", expireAfterSeconds=self._expire_after)
        except OperationFailure:
            _LOGGER.warning(
                f"Attempted to set a different expiry for {self._collection_name} "
                "collection. An existing TTL index already exists and will be "
                "used instead."
            )
            collection = db[self._collection_name]

        # Loop until the queue is empty or we encounter an error
        while not done:
            try:
                while len(self._pending_documents) < max_batch_size:
                    document = self._queue.get_nowait()
                    self._pending_documents.append(document)
                    self._pending_size += sys.getsizeof(document)

            except queue.Empty:
                done = True

            if not self._pending_documents:
                continue
            
            try:
                try:
                    _LOGGER.debug("Sending batch of samples to database", extra=self.info)
                    collection.insert_many(self._pending_documents, ordered=False)
                except BulkWriteError as e:
                    codes = [detail.get("code") == 11000 for detail in e.details.get("writeErrors", [])]
                    if codes and not all(codes):
                        raise
                else:
                    _LOGGER.debug("All samples saved")
                    self._pending_documents.clear()
                    self._pending_size = 0
                    self._retries = 0
            except Exception:
                # Attempt to send on the next call instead
                done = True
                self._retries += 1

                _LOGGER.warning("Error in worker", exc_info=True)
                
                info = self.info
                
                if exiting:
                    _LOGGER.info("The worker is stopping", extra=info)
                elif self._retries > self._max_retries:
                    _LOGGER.error("Dropping samples", extra=info)
                else:
                    _LOGGER.info("Resending samples attempt %i of %i",
                        self._retries,
                        self._max_retries,
                        extra=info
                    )

                if self._retries > self._max_retries:
                    # Drop this batch of samples
                    self._pending_documents.clear()
                    self._pending_size = 0
                    self._retries = 0


class MongoTimeseriesHandler:
    """A handler that sends timeseries samples to MongoDB.

    The handler starts a worker thread in the background and submits timeseries
    samples to the worker which flushes samples to the database at set intervals
    or if the buffer reaches a certain size.

    If a worker fails, the next call to `publish` will attempt to start
    another worker for this handler. When a worker is started, the handler will
    wait up to 10 seconds and confirm if the worker is running. If it is not,
    the worker is stopped and `TimeoutError` is raised on `publish`. The caller
    can choose what to do with the samples from there, including re-publish them.

    Args:
        connection_url: Mongo DSN connection url.
        database_name: The database to save samples to.
        collection_name: The collection name to save samples to.
        flush_interval: The time (in seconds) between flushes on the worker.
        buffer_size: The number of samples that can be buffered before a flush
            is done to the database.
        max_retries: The maximum number of attempts to make sending a batch of
            samples before giving up on the batch.
        expire_after: The value of the TTL index for samples.
        **kwargs: Additional kwargs for `MongoClient`.
    """
    worker: TimeseriesWorker = None

    def __init__(self, expire_after: int = 2_592_000, **kwargs: Any) -> None:
        kwargs.update({"expire_after": expire_after})
        self.kwargs = kwargs
        self._lock = threading.Lock()

        self._created = datetime.utcnow()
        self._workers_used = 0

    @property
    def info(self) -> StorageHandlerInfo:
        worker = None
        if self.worker is not None:
            worker = WorkerInfo.parse_obj(self.worker.info)
        return StorageHandlerInfo(
            created=self._created,
            uptime=(datetime.utcnow() - self._created).total_seconds(),
            workers_used=self._workers_used,
            worker=worker
        )

    def start_worker(self) -> TimeseriesWorker:
        """Start the timeseries worker thread."""
        worker = TimeseriesWorker(**self.kwargs)
        worker.start()
        worker.wait(10)
        if not worker.is_running:
            worker.stop()
            raise TimeoutError("Timed out waiting for worker thread to be ready.")
        self._workers_used += 1
        return worker

    def get_worker(self) -> TimeseriesWorker:
        """Get a timeseries worker. If a worker does not exist or the worker
        is not running, a new worker is started.
        """
        if self.worker is None:
            worker = self.start_worker()
            self.worker = worker
        elif not self.worker.is_running:
            worker, self.worker = self.worker, None
            if not worker.is_stopped:
                worker.stop()
            worker = self.start_worker()
            self.worker = worker
        return self.worker

    def flush(self, block: bool = False):
        """Tell the worker to send any currently enqueued samples.
        
        Blocks until enqueued samples are sent if `block` is set.
        """
        with self._lock:
            if self.worker is not None:
                self.worker.flush(block)

    def publish(self, samples: Iterable[TimeseriesDocument]):
        """Publish a sample to the worker."""
        with self._lock:
            worker = self.get_worker()
            for sample in samples:
                worker.publish(asdict(sample))

    def close(self) -> None:
        """Shuts down this handler and the flushes the worker."""
        with self._lock:
            if self.worker is not None:
                self.worker.flush()
                self.worker.stop()