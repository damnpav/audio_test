from flask import Flask, render_template, request, redirect, url_for
from db_fun import initialize_cursor, add_order
from datetime import datetime as dt

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cursor, conn = initialize_cursor()  # Initialize the cursor
        add_order(dt.now().strftime('%H%M%S%s%d%m'), cursor, conn)
        return redirect(url_for('index'))
    return render_template('button.html')


if __name__ == "__main__":
    app.run(debug=True)
