from flask import Flask, render_template, request, redirect, url_for
from db_fun import initialize_cursor, add_order, insert_stop_flag
from datetime import datetime as dt

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    cursor, conn = initialize_cursor()  # Initialize the cursor
    if request.method == "POST":
        if "check_button" in request.form:
            add_order(dt.now().strftime('%H%M%S%s%d%m'), cursor, conn)
        elif "stop_button" in request.form:
            insert_stop_flag(cursor, conn)  # Call insert_stop_flag
        return redirect(url_for('index'))
    return render_template('button.html')


if __name__ == "__main__":
    app.run(debug=True)
