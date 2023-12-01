from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Replace these with your MySQL database credentials
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="yash"  # Change to your database name
)

def is_email_exists(email):
    cursor = db.cursor(buffered=True)  # Set buffered=True
    cursor.execute("SELECT email FROM feedback WHERE email = %s", (email,))
    result = cursor.fetchone()  # Fetch the result
    cursor.close()
    return result is not None

def is_name_exists(first_name, last_name):
    cursor = db.cursor(buffered=True)  # Set buffered=True
    cursor.execute("SELECT first_name, last_name FROM feedback WHERE first_name = %s AND last_name = %s", (first_name, last_name))
    result = cursor.fetchone()  # Fetch the result
    cursor.close()
    return result is not None


@app.route("/")
def index():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    first_name = request.form.get("firstName")
    last_name = request.form.get("lastName")
    email = request.form.get("email")
    course = request.form.get("course")
    class_name = request.form.get("class")
    rating1 = request.form.get("rating1")
    rating2 = request.form.get("rating2")
    rating3 = request.form.get("rating3")
    rating4 = request.form.get("rating4")
    rating5 = request.form.get("rating5")
    hour = request.form.get("hour")
    minute = request.form.get("minute")
    ampm = request.form.get("ampm")
    review = request.form.get("review")
    comments = request.form.get("comments")

    # Validation: Check if the name already exists
    if is_name_exists(first_name, last_name):
        return "Sorry your name already exists. You cannot fill the form twice."

    # Validation: Check if the email already exists
    if is_email_exists(email):
        return "This Email already exists for an existing user. Please use your email."

    cursor = db.cursor()
    insert_query = """
    INSERT INTO feedback (first_name, last_name, email, course, class_name, rating1, rating2, rating3, rating4, rating5, hour, minute, ampm, review, comments)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (first_name, last_name, email, course, class_name, rating1, rating2, rating3, rating4, rating5, hour, minute, ampm, review, comments)
    cursor.execute(insert_query, values)
    db.commit()
    cursor.close()

    return "Feedback submitted successfully."

if __name__ == "__main__":
    app.run(debug=True)
