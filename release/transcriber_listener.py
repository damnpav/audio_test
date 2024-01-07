import whisper
from db_fun import initialize_cursor, transcriber_listener, transcribing_results

cursor, conn = initialize_cursor()
model = whisper.load_model('base')


stop_flag = 0
while stop_flag == 0:
    listen_df = transcriber_listener(conn)

    if len(listen_df) > 0:
        if len(listen_df) > 1:
            print(f'There are more than 1 line! Take last rows')
            listen_df = listen_df[-1:].copy()
        order_id = listen_df['OrderID'].values[0]
        audio_file_path = listen_df['AudioFilePath'].values[0]
        model_result = model.transcribe(audio=audio_file_path)
        transcribed_text = model_result['text']
        transcribing_results(transcribed_text, order_id, cursor, conn)
        stop_flag = 1





