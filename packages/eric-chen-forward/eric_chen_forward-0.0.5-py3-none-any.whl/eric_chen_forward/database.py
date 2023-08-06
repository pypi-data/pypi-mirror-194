import sqlite3

class Database:

    def __init__(self) -> None:
        self.db_name = "sqlite3_database.db"

    def insert_initial_classifier_data(labels_file, passages_file):
        query = """
             CREATE TABLE "dataset" (
                "id"	INTEGER NOT NULL,
                "labels"	TEXT NOT NULL,
                "passages"	TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        
        """
