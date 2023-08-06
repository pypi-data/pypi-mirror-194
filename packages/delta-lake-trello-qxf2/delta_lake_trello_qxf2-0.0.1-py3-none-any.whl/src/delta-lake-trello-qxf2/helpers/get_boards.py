
import sys
import os
sys.path.append(os.path.dirname((os.path.abspath(__file__))))
import trello_functions as tf

def get_boards_data():
    total_boards = tf.get_boards_list()
    few_boards = total_boards[0:20]
    return few_boards