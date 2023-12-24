from flask import Flask, render_template, request, redirect, url_for
from db_fun import initialize_cursor, add_order

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        initialize_cursor()
        add_order()  # Call the function to insert a row
        return redirect(url_for('index'))
    return render_template('index.html')


if __name__ == "__main__":
    database.init_db()  # Initialize the database
    app.run(debug=True)
