"""Checkpoint Persistence for LangGraph Multi-Agent Organization."""
import logging
from typing import Any
from langgraph.checkpoint.memory import MemorySaver

logger = logging.getLogger(__name__)


def get_checkpointer(use_postgres: bool = False, postgres_conn_str: str | None = None) -> Any:
    """Instantiate a durable checkpoint store.
    
    Args:
        use_postgres: When True, initializes PostgreSQL checkpointer; otherwise MemorySaver.
        postgres_conn_str: Connection URI string for PostgreSQL.
    """
    if use_postgres and postgres_conn_str:
        try:
            from langgraph.checkpoint.postgres import PostgresSaver
            logger.info("Initializing PostgreSQL state checkpointer...")
            return PostgresSaver.from_conn_string(postgres_conn_str)
        except Exception as e:
            logger.warning(f"Failed to connect to PostgreSQL checkpointer ({e}). Falling back to MemorySaver.")
            return MemorySaver()

    logger.info("Using in-memory state checkpointer (MemorySaver).")
    return MemorySaver()
