import whisper
from datetime import datetime as dt
from db_fun import initialize_cursor, transcriber_listener, transcribing_results

cursor, conn = initialize_cursor()
model = whisper.load_model('base')


stop_flag = 0
while stop_flag == 0:
    listen_df = transcriber_listener(cursor, conn)

    if len(listen_df) > 0:
        order_id = listen_df['OrderID'].values[0]
        audio_file_path = listen_df['AudioFilePath'].values[0]
        model_result = model.transcribe(audio=audio_file_path)
        transcribed_text = model_result['text']
        transcribing_results(transcribed_text, order_id, cursor, conn)

    stop_flag = 1





