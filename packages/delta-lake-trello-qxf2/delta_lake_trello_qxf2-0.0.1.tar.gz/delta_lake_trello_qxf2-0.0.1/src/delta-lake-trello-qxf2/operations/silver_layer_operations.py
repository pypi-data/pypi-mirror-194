"""
This script contains the functions that help in refinement operations
"""

from config import delta_table_conf as dc
import os
import sys
from loguru import logger
from delta.tables import DeltaTable
from pyspark.sql.functions import col, date_format, lit, row_number
from pyspark.sql.window import Window
# add project root to sys path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def refine_current_board_cards_silver(spark, board_id, board_name):
    """
    Refine cards data of a trello board and save it into a Delta Lake Silver table
    :param board_id: Trello board id
    :return none
    """
    path = dc.cards_silver_table_path
    

    try:
        # Fetch raw cards data from bronze delta table that have been recently added
        raw_cards_data = spark.read.format(
            "delta").load(dc.cards_bronze_table_path)
        logger.info(f'Fetched the raw cards data')

        raw_mem_data = spark.read.format(
            "delta").load(dc.members_bronze_table_path)
        logger.info(f'Fetched the raw members data')

        # Filter data based on sprint board
        refined_cards_data = raw_cards_data.filter(
            raw_cards_data.idBoard == board_id)

        before = refined_cards_data.count()

        # Create temporary views for members and cards data to run sql queries
        refined_cards_data.createOrReplaceTempView("trello_cards")
        raw_mem_data.createOrReplaceTempView("trello_members")

        refined_cards_data = spark.sql("select tc.*, array_join(collect_list(tm.fullName), ', ') as card_members from trello_cards tc \
                                        left outer join trello_members tm where array_contains (tc.idMembers, tm.id) \
                                        group by tc.id, tc.closed, tc.dateLastActivity, tc.due, tc.idBoard, tc.idList, \
                                        tc.idMembers, tc.name, tc.desc, tc.shortLink, tc.shortUrl, tc.url")

        after = refined_cards_data.count()

        lost = before - after
        with open("/tmp/lost.csv", 'a') as f:
            f.write("lost cards: " + str(lost) + " board id: " + str(board_id) + str(board_name) + '  ')

        # Change the format of dateLastActivity for readability
        refined_cards_data = refined_cards_data.withColumn(
            'LastUpdated', date_format('dateLastActivity', "dd-MM-yyyy"))

        # Add board_name to the list of columns
        refined_cards_data = refined_cards_data.withColumn(
            'board_name', lit(board_name))

        logger.info(
            "Completed refining the data, writing cleaned and conformed data as a Silver table in Delta Lake")

        # refined_cards_data.write.format('delta').mode(
        #     "append").option("mergeSchema", 'true').save(path)
        deltaTable = DeltaTable.forPath(spark, path)
        deltaTable.alias("target").merge(
            source=refined_cards_data.alias("source"),
            condition="target.id = source.id").whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
        logger.success(
            f'\n Refined data and created cards Silver Delta Table successfully for board {board_id} {board_name} in path {path}')

    except Exception as error:
        logger.exception(
            f'Exception while creating Silver Delta Table for board {board_id} {board_name}')
        raise error


def get_unique_cards_silver(spark):
    """
    Removed the duplicate cards of silver table and save it into a Delta Lake Silver table
    :param spark: Spark session object
    """
    unique_cards_path = dc.cards_unique_silver_table_path

    try:
        # Fetch refined cards data from Silver table
        refined_cards_data = spark.read.format(
            "delta").load(dc.cards_silver_table_path)
        logger.info(f'Fetched the refined silver cards data')

        win = Window.partitionBy("name").orderBy(col("dateLastActivity").desc())
        deduplicated_cards = refined_cards_data.withColumn(
            "row", row_number().over(win)).filter(col("row") == 1).drop("row")

        logger.info(
            "Completed deduplicating the data, writing it as a Silver table in Delta Lake")

        deduplicated_cards.write.format('delta').mode(
            "append").option("mergeSchema", 'true').save(unique_cards_path)

        logger.info("Completed writing the data to Silver table")

    except Exception as error:
        logger.exception(
            f'Exception while creating Silver Delta Table')
        raise error