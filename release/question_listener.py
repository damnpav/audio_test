from langchain.chat_models import ChatOpenAI
from db_fun import initialize_cursor, question_listener, question_results, question_send, stop_check

cursor, conn = initialize_cursor()
auth_path = 'auth_file.txt'
question_path = 'question_form.txt'
# auth_path = '/Users/dp_user/PycharmProjects/audio_test/auth_file.txt'
# question_path = '/Users/dp_user/PycharmProjects/audio_test/release/question_form.txt'

with open(auth_path, 'r') as keyfile:
    api_key = keyfile.read()
llm = ChatOpenAI(openai_api_key=api_key, model_name='gpt-4-0613')

# gpt-4-0613

with open(question_path, 'r') as file:
    question_form = file.read()

stop_flag = 0
while stop_flag == 0:
    # if stop_check(conn):
    #     stop_flag = 1
    #     break
    try:
        listen_df = question_listener(conn)

        if len(listen_df) > 0:
            if len(listen_df) > 1:
                print(f'There are more than 1 line! Take last rows')
                listen_df = listen_df[-1:].copy()
            order_id = listen_df['OrderID'].values[0]
            transcribed_text = listen_df['TranscribeText'].values[0]
            question_query = f'{question_form}: "{transcribed_text}"'
            question_send(question_query, order_id, cursor, conn)
            response = llm.invoke(question_query)
            question_results(response.content, order_id, cursor, conn)
            # stop_flag = 1
    except:
        pass





