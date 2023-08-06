"""
This job will run the steps which will extract raw cards data of a trello board and place them
in a Delta Lake Bronze table
It is scheduled to run daily
"""

import os
import sys
from loguru import logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from operations import bronze_layer_operations as bl
from helpers import common_functions as cf, spark_helper as sh
from helpers import trello_functions as tf
from helpers import get_boards as gb

def perform_cards_ingestion_to_bronze():
    """
    Run the steps to extract raw cards data and place it Delta Lake Bronze table
    """
    logger.info("Starting the cards ingestion job")
    try:
        #Get SparkSession
        spark, spark_context = sh.start_spark()


        few_boards = gb.get_boards_data()
        print("Boards for which data will be collected", few_boards)

        for each_board in few_boards:
            board_id = each_board.id
            print("Board ID is", board_id)
            board_name = each_board.name
            print("Board name is", board_name)

            # Extract raw cards data
            bl.ingest_raw_cards_data_bronze(
                spark, spark_context, board_id, board_name)
            logger.info(
                f'Extraction of raw cards data completed for board {board_id} {board_name}')
        logger.success("Completed the cards ingestion job")

    except Exception as error:
        logger.exception(
            f'Failure in job to fetch raw cards data for board {board_id} {board_name}')
        raise error


# --------START OF SCRIPT
if __name__ == "__main__":
    perform_cards_ingestion_to_bronze()
