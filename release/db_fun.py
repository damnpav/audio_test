import sqlite3
import pandas as pd
from datetime import datetime as dt


db_path = '../audio_db.db'


def initialize_cursor():
    """
    Function to initialize connection to db for logging
    :return: cursor
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return cursor, conn


def check_for_order(conn):
    """
    Function to query DB for new orders
    :return:
    """
    check_sql = """
                SELECT * 
                FROM control_panel
                WHERE 
                OrderID IS NOT NULL and AudioCompleted IS NULL
                """
    order_df = pd.read_sql(check_sql, conn)
    if len(order_df) > 0:
        return True
    else:
        return False


def audio_completed(cursor, conn):
    """
    Mark that audio stream is completed
    :return:
    """
    update_sql = f"""
                 UPDATE control_panel
                 SET AudioCompleted = '{dt.now().strftime('%H_%M_%S_%d_%m')}'
                 WHERE OrderID IS NOT NULL
                 AND AudioCompleted IS NULL
                 """
    cursor.execute(update_sql)
    conn.commit()


def record_audio_file(file_path, cursor, conn):
    """
    Record to db path to saved audio file
    :param file_path:
    :return:
    """
    alter_sql = f"""
                UPDATE control_panel
                SET AudioFilePath = '{file_path}'
                WHERE OrderID IS NOT NULL
                AND AudioFilePath IS NULL
                """
    cursor.execute(alter_sql)
    conn.commit()

