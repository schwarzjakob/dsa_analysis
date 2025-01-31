import os
import logging
from contextlib import contextmanager
from psycopg2 import pool, extras
from dotenv import load_dotenv

# Load environment variables (DATABASE_URL, etc.)
load_dotenv()


class Database:
    """
    A singleton class that manages a PostgreSQL connection pool.
    """

    __instance = None
    __pool = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Database, cls).__new__(cls)
        return cls.__instance

    def __init__(
        self,
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        minconn=1,
        maxconn=10,
    ):
        if not hasattr(self, "__initialized") or not self.__initialized:
            try:
                self.__pool = pool.ThreadedConnectionPool(
                    minconn, maxconn, dbname=dbname, user=user, password=password, host=host, port=port
                )
                self.__initialized = True
                logging.info("Database connection pool initialized successfully.")
            except Exception as e:
                logging.error(f"Error initializing connection pool: {e}")
                raise

    @contextmanager
    def get_connection(self):
        """
        Yields a connection from the pool, then returns it to the pool.
        """
        conn = None
        try:
            conn = self.__pool.getconn()
            yield conn
        finally:
            if conn:
                self.__pool.putconn(conn)

    @contextmanager
    def transaction(self):
        """
        Yields a cursor in a transaction block.
        Commits on success; rolls back on error.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=extras.DictCursor)
            try:
                yield cursor
                conn.commit()
            except Exception as e:
                conn.rollback()
                logging.error(f"Transaction failed: {e}")
                raise
            finally:
                cursor.close()

    def execute_query(self, query: str, params=None) -> bool:
        """
        Execute a single query (INSERT, UPDATE, DELETE, etc.) with autocommit.
        Returns True on success, False on error.
        """
        try:
            with self.transaction() as cursor:
                cursor.execute(query, params)
            return True
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            return False

    def fetch_query(self, query: str, params=None):
        """
        Execute a SELECT query and fetch all results as a list of DictRows.
        Returns None on error.
        """
        try:
            with self.transaction() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
        except Exception as e:
            logging.error(f"Error fetching query: {e}")
            return None

    def close(self):
        """Close the connection pool when shutting down."""
        if self.__pool:
            self.__pool.closeall()
            logging.info("Database connection pool closed.")
