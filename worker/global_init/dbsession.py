from typing import Dict, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from urllib.parse import quote_plus
from . import logger


class ConnectionHandler:
    """Manages database connections and sessions for multiple databases."""

    def __init__(self, username: str, password: str, database_list: List[str], server: str):
        """
        Initialize the ConnectionHandler with credentials and database list.
        Args:
            username (str): Database username.
            password (str): Database password.
            database_list (List[str]): List of database IDs (names) to connect to.
            server (str): Database server hostname or IP.
        """
        self.__username = username
        self.__password = password
        self.__database_list = database_list
        self.__server = server
        self.__engines: Dict[str, create_engine] = {}
        self.__session_factories: Dict[str, sessionmaker] = {}
        self.__scoped_sessions: Dict[str, scoped_session] = {}
        # Initilize connection
        self.__initilize_connections()

    def __initilize_connections(self) -> None:
        """
        Initialize engines and session factories for each database.
        """
        for db_id in self.__database_list:
            try:
                # Construct database URI
                conn_string = f"mssql+pymssql://{self.__username}:{self.__password}@{self.__password}/{self.__server}?charset=utf8&tds_version=7.0"

                # Create engine with connection pooling
                engine = create_engine(conn_string, pool_size=5, max_overflow=10)

                # Test connection
                with engine.connect() as conn:
                    logger.info(f"Successfully connected to databaseid: {db_id}")
                
                # Store engine and session factories
                self.__engines[db_id] = engine
                self.__session_factories[db_id] = sessionmaker(bind=engine, autoflush=False)
                self.__scoped_sessions[db_id] = scoped_session(self.__session_factories[db_id])

            except Exception as e:
                logger.error(f"Failed to connect to database {db_id}: {str(e)}")
                continue
        
        if not self.__engines:
            logger.error(f"No database could be connected. Database list: {','.join(self.__database_list)} ")
            raise RuntimeError("Failed to connect to any database")
        
    def get_session(self, db_id: str) -> scoped_session:
        """
        Return the scoped session for a specific database_id.
        """
        if db_id not in self.__scoped_sessions:
            logger.error(f"Database {db_id} not available.")
            raise ValueError(f"Database {db_id} not configured or connected.")

        return self.__scoped_sessions[db_id]
    
    def dispose_engines(self) -> None:
        """
        Dispose all engines to release the connections
        """
        for db_id, engine in self.__engines.items():
            try:
                logger.info(f"Disposing engine for {db_id}")
                engine.dispose()

            except Exception as e:
                logger.error(f"Could not dispose engine for {db_id}: {str(e)} ")


@contextmanager
def db_session_scope(handler: ConnectionHandler, db_id: str, read_only: bool = False, batch_size: int = 500):
    """
    Provide a single transactional scoped for a database.
    Args:
        handler (ConnectionHandler): The connection handler instance.
        db_id (str): The database id to use.
        read_only (bool, optional): If True, skip commit (for read operation). Default to False.
        batch_size (int, optional): If set, you can manually flush every batch_size operations in your loop.

    Yield:
        The session instance.

    Example usage:
        ```
        # Insertion
        processed_count = 0
        with db_session_scope(handler, 'DBID', batch_size=500) as session:
            for row in dictionary:
                insert to table
                ....
                session.add(...)

                processed_count += 1
                if batch_size and processed_count % batch_size == 0:
                    session.flush() # manually flush to free up memory and stage the changes
        ```
        ```
        # Read-only
        with db_session_scope(handler, 'DBID', read_only=True) as session:
            query_output = session.query(...).all()
        ```

    """
    scoped_session = handler.get_session(db_id)
    session = scoped_session()
    try:
        yield session
        if not read_only:
            session.commit()

    except Exception as e:
        logger.error(f"Operation failed on database {db_id}.")
        session.rollback()
        raise

    finally:
        session.close()
        scoped_session.remove()
        logger.debug(f"Session close for database {db_id}.")
