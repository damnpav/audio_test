import sqlite3
import pandas as pd
from datetime import datetime as dt
import subprocess


#db_path = '../audio_db.db'
db_path = '/Users/dp_user/PycharmProjects/audio_test/audio_db.db'
remote_path = '/usr/projects/audio'
remote_pass_path = '/Users/dp_user/PycharmProjects/audio_test/remote_pass.txt'
remote_address_path = '/Users/dp_user/PycharmProjects/audio_test/remote_address.txt'

with open(remote_pass_path, 'r') as file:
    remote_pass = file.read().strip()

with open(remote_address_path, 'r') as file:
    remote_address = file.read().strip()


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


def transcriber_listener(conn):
    """
    Listen DB for new audio files to transcribe
    :param cursor:
    :param conn:
    :return:
    """
    listen_sql = f"""
                  SELECT OrderID, AudioFilePath 
                  FROM control_panel
                  WHERE TranscribeCompleted IS NULL
                  AND OrderID IS NOT NULL
                  AND AudioFilePath IS NOT NULL
                  """
    listen_df = pd.read_sql(listen_sql, conn)
    return listen_df


def question_listener(conn):
    """
    Listen DB for new questions
    :param cursor:
    :param conn:
    :return:
    """
    listen_sql = f"""
                  SELECT OrderID, TranscribeText 
                  FROM control_panel
                  WHERE TranscribeCompleted IS NOT NULL
                  AND OrderID IS NOT NULL
                  AND ChatQuerySend IS NULL
                  """
    listen_df = pd.read_sql(listen_sql, conn)
    return listen_df


def transcribing_results(transcribed_text, order_id, cursor, conn):
    """
    Write time and text from transcribing
    :param cursor:
    :param conn:
    :return:
    """
    transcribed_sql = f"""
                       UPDATE control_panel
                       SET TranscribeCompleted = "{dt.now().strftime('%H_%M_%S_%d_%m')}",
                           TranscribeText = "{transcribed_text.replace('"', '')}"
                       WHERE OrderID = "{order_id}"
                       """
    cursor.execute(transcribed_sql)
    conn.commit()
    synchronize_db()


def question_results(answer_text, order_id, cursor, conn):
    """
    Write time and text from question
    :param cursor:
    :param conn:
    :return:
    """
    answer_sql = f"""
                       UPDATE control_panel
                       SET ChatResponseGet = "{dt.now().strftime('%H_%M_%S_%d_%m')}",
                           ChatResponseText = "{answer_text.replace('"', '')}"
                       WHERE OrderID = "{order_id}"
                       """
    cursor.execute(answer_sql)
    conn.commit()


def question_send(question_text, order_id, cursor, conn):
    """
    Write time and text from question
    :param cursor:
    :param conn:
    :return:
    """
    question_sql = f"""
                       UPDATE control_panel
                       SET ChatQuerySend = "{dt.now().strftime('%H_%M_%S_%d_%m')}",
                           ChatQueryText = "{question_text.replace('"', '')}"
                       WHERE OrderID = "{order_id}"
                       """
    cursor.execute(question_sql)
    conn.commit()


def add_order(order_id, cursor, conn):
    """
    Function to append order_id
    :param order_id:
    :param cursor:
    :param conn:
    :return:
    """
    truncate_db(cursor, conn)
    ts = dt.now().strftime('%H_%M_%S_%d_%m')
    order_sql = f"""
                INSERT INTO control_panel (TimeStamp, OrderID)
                VALUES ('{ts}', '{order_id}')
                """
    cursor.execute(order_sql)
    conn.commit()


def answer_listener(conn):
    """
    Listen DB for new answers
    :param cursor:
    :param conn:
    :return:
    """
    listen_sql = f"""
                  SELECT ChatResponseGet, ChatResponseText 
                  FROM control_panel
                  WHERE ChatResponseGet IS NOT NULL
                  AND ChatResponseText IS NOT NULL
                  """
    listen_df = pd.read_sql(listen_sql, conn)
    return listen_df


def stop_check(conn):
    """
    Listen DB for new stop flags
    :param conn:
    :return:
    """
    stop_sql = f"""
                  SELECT TimeStamp
                  FROM stop_panel
                  """
    stop_df = pd.read_sql(stop_sql, conn)

    if len(stop_df) > 0:
        stop_df['TimeStamp'] = pd.to_datetime(stop_df['TimeStamp'], format='%H_%M_%S_%d_%m_%Y')
        max_time = stop_df['TimeStamp'].max()
        # TODO need to test it
        if max_time > (dt.now() - pd.Timedelta(minutes=1)):
            return True
    return False


def insert_stop_flag(cursor, conn):
    """
    Insert stop flag
    :param cursor:
    :param conn:
    :return:
    """
    ts = dt.now().strftime('%H_%M_%S_%d_%m_%Y')
    stop_sql = f"""
                INSERT INTO stop_panel (TimeStamp)
                VALUES ('{ts}')
                """
    cursor.execute(stop_sql)
    conn.commit()


def synchronize_db():
    command = f'sshpass -p {remote_pass} scp {db_path} {remote_address}:{remote_path}'
    try:
        subprocess.run(command, shell=True, check=True)
        print(f'File transferred')
    except Exception as e:
        print(f'Exception: {e}')


def truncate_db(cursor, conn):
    truncate_sql = """
                   DELETE FROM control_panel
                   """
    cursor.execute(truncate_sql)
    conn.commit()







    
