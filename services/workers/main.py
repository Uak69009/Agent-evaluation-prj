"""
Background evaluation worker entrypoint placeholder.
Will process evaluation jobs off the Redis queue.
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agentevalops.worker")


def start_worker():
    logger.info("AgentEvalOps Evaluation Worker process initialized.")


if __name__ == "__main__":
    start_worker()
