""""
This module is used to generate the results of the gold table
"""

import os
import sys
from loguru import logger
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import delta_table_conf as dc
from helpers import spark_helper as sh
from helpers import skype_sender as ss

def generate_results():
    """
    Generate results of gold table
    """
    path = dc.noactive_cards_gold_path
    # data = [{"Category": 'A', "ID": 1, "Value": 121.44},
    #     {"Category": 'B', "ID": 2, "Value": 300.01},
    #     {"Category": 'C', "ID": 3, "Value": 10.99},
    #     {"Category": 'E', "ID": 4, "Value": 33.87}
    #     ]

    try:
        spark, spark_context = sh.start_spark()
        print("Generating results")
        noactive_cards_data = df.read_delta_table(spark,path)
        #df2 = spark.createDataFrame(data)
        #ss.post_message_on_skype(str(df2.toJSON().collect()))
        print("The results are", str(noactive_cards_data.toJSON().collect()))

    except Exception as error:
        logger.exception(f"")
        raise error

if __name__ == "__main__":
    generate_results()