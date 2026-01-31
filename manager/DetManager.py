# VibeFlux, AGPL-3.0 license

import sqlite3
from sqlite3 import Error
import threading
import queue
import time
from ..base.Manager import BaseDB


class DetectionDB(BaseDB):
    """
    SQLite database manager for storing object detection results.
    Supports asynchronous insertion operations to accommodate high-frame-rate video streams.
    """

    def __init__(self, db_path: str = 'detection_results.db') -> None:
        """
        Initializes the database connection and starts the background insertion thread.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        super().__init__(db_path, check_same_thread=False)

        self.queue: queue.Queue = queue.Queue()
        self.lock: threading.Lock = threading.Lock()
        self.create_table()
        self.stop_event: threading.Event = threading.Event()
        self.thread: threading.Thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def create_table(self) -> None:
        """
        Creates the table for storing detection results if it does not already exist.
        """
        create_table_sql: str = """
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT NOT NULL,
            class_id INTEGER NOT NULL,
            confidence REAL NOT NULL,
            bbox_xmin INTEGER NOT NULL,
            bbox_ymin INTEGER NOT NULL,
            bbox_xmax INTEGER NOT NULL,
            bbox_ymax INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            with self.lock:
                self.cursor.execute(create_table_sql)
                self.conn.commit()
                print("Detections table created or already exists.")
        except Error as e:
            print(f"Failed to create table: {e}")

    def insert(
        self,
        class_name: str,
        class_id: int,
        confidence: float,
        bbox: tuple[int, int, int, int],
        image_path: str
    ) -> None:
        """
        Adds a single detection result to the insertion queue.

        Args:
            class_name (str): Name of the detected object class.
            class_id (int): Identifier for the detected object class.
            confidence (float): Confidence score of the detection.
            bbox (tuple[int, int, int, int]): Bounding box coordinates as (xmin, ymin, xmax, ymax).
            image_path (str): Path to the image where the detection was made.
        Returns:
            None
        """
        detection: tuple = (
            class_name,
            class_id,
            confidence,
            bbox[0],
            bbox[1],
            bbox[2],
            bbox[3],
            image_path
        )
        self.queue.put(detection)

    def insert_bulk(self, detections: list[dict] | list[tuple]) -> None:
        """
        Adds multiple detection results to the insertion queue in bulk.

        Args:
            detections (list[dict] | list[tuple]): List of detection results, each as a dictionary or tuple containing necessary information.
        """
        for det in detections:
            detection: tuple = (
                det['class_name'],
                det['class_id'],
                det['confidence'],
                det['bbox'][0],
                det['bbox'][1],
                det['bbox'][2],
                det['bbox'][3],
                det['image_path']
            )
            self.queue.put(detection)

    def _worker(self) -> None:
        """
        Background thread that continuously retrieves data from the queue and inserts it into the database.
        """
        while not self.stop_event.is_set() or not self.queue.empty():
            try:
                detections_batch: list[tuple] = []
                # Batch retrieval to improve insertion efficiency
                while len(detections_batch) < 100 and not self.queue.empty():
                    detections_batch.append(self.queue.get())
                if detections_batch:
                    self._insert_batch(detections_batch)
                else:
                    time.sleep(0.01)  # Prevents tight loop when queue is empty
            except Exception as e:
                print(f"Error in background insertion thread: {e}")

    def _insert_batch(self, batch: list[tuple]) -> None:
        """
        Inserts a batch of detection results into the database.

        Args:
            batch (list[tuple]): List of detection tuples to be inserted.
        """
        insert_sql: str = """
        INSERT INTO detections (class_name, class_id, confidence, 
                                bbox_xmin, bbox_ymin, bbox_xmax, bbox_ymax, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        try:
            with self.lock:
                self.cursor.executemany(insert_sql, batch)
                self.conn.commit()
                # print(f"Inserted batch of {len(batch)} detection results.")
        except Error as e:
            print(f"Failed to insert batch data: {e}")

    def close(self) -> None:
        """
        Stops the background thread and closes the database connection.
        """
        self.stop_event.set()
        self.thread.join()
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def __del__(self) -> None:
        """
        Ensures the database connection is closed when the object is destroyed.
        """
        self.close()
