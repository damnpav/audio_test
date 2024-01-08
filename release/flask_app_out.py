from flask import Flask, jsonify, render_template
from db_fun import initialize_cursor, answer_listener

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('output.html')

@app.route('/get_updates')
def get_updates():
    cursor, conn = initialize_cursor()
    data = answer_listener(conn)
    return jsonify(data.to_dict(orient='records'))

if __name__ == "__main__":
    app.run(debug=True, port=8000)
