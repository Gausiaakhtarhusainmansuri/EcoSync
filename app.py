from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        college = request.form["college"]
        e_waste_type = request.form["e_waste_type"]

        connection = sqlite3.connect("ecosync.db")

        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO participants
        (name, email, phone, college, e_waste_type)
        VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, college, e_waste_type))

        connection.commit()
        connection.close()

        return render_template("success.html", name=name)

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():

    connection = sqlite3.connect("ecosync.db")
    cursor = connection.cursor()

    # Total participants
    cursor.execute("SELECT COUNT(*) FROM participants")
    total_participants = cursor.fetchone()[0]

    # Mobile count
    cursor.execute(
        "SELECT COUNT(*) FROM participants WHERE e_waste_type = ?",
        ("Mobile",)
    )
    mobile_count = cursor.fetchone()[0]

    # Laptop count
    cursor.execute(
        "SELECT COUNT(*) FROM participants WHERE e_waste_type = ?",
        ("Laptop",)
    )
    laptop_count = cursor.fetchone()[0]

    # Charger count
    cursor.execute(
        "SELECT COUNT(*) FROM participants WHERE e_waste_type = ?",
        ("Charger",)
    )
    charger_count = cursor.fetchone()[0]

    # Keyboard count
    cursor.execute(
        "SELECT COUNT(*) FROM participants WHERE e_waste_type = ?",
        ("Keyboard",)
    )
    keyboard_count = cursor.fetchone()[0]

    # Total e-waste collected
    cursor.execute("SELECT SUM(quantity) FROM collections")
    total_e_waste = cursor.fetchone()[0]

    if total_e_waste is None:
        total_e_waste = 0

    connection.close()

    return render_template(
        "dashboard.html",
        total_participants=total_participants,
        mobile_count=mobile_count,
        laptop_count=laptop_count,
        charger_count=charger_count,
        keyboard_count=keyboard_count,
        total_e_waste=total_e_waste
    )


@app.route("/participants")
def participants():

    connection = sqlite3.connect("ecosync.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM participants")

    data = cursor.fetchall()

    connection.close()

    return render_template(
        "participants.html",
        participants=data
    )
@app.route("/delete/<int:participant_id>")
def delete_participant(participant_id):

    connection = sqlite3.connect("ecosync.db")
    cursor = connection.cursor()

    # Delete collection records of the participant
    cursor.execute(
        "DELETE FROM collections WHERE participant_id = ?",
        (participant_id,)
    )

    # Delete participant
    cursor.execute(
        "DELETE FROM participants WHERE participant_id = ?",
        (participant_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/participants")

@app.route("/collection", methods=["GET", "POST"])
def collection():

    if request.method == "POST":

        participant_id = request.form["participant_id"]
        e_waste_type = request.form["e_waste_type"]
        quantity = request.form["quantity"]
        collection_date = request.form["collection_date"]

        connection = sqlite3.connect("ecosync.db")
        cursor = connection.cursor()

        # Check participant
        cursor.execute(
            "SELECT * FROM participants WHERE participant_id = ?",
            (participant_id,)
        )

        participant = cursor.fetchone()

        if participant is None:

            connection.close()

            return "Participant ID not found. Please enter a valid Participant ID."

        # Save collection
        cursor.execute("""
        INSERT INTO collections
        (participant_id, e_waste_type, quantity, collection_date)
        VALUES (?, ?, ?, ?)
        """, (
            participant_id,
            e_waste_type,
            quantity,
            collection_date
        ))

        connection.commit()
        connection.close()

        return render_template("collection_success.html")

    return render_template("collection.html")


@app.route("/collections")
def collections():

    connection = sqlite3.connect("ecosync.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM collections")

    data = cursor.fetchall()

    connection.close()

    return render_template(
        "collections.html",
        collections=data
    )


@app.route("/certificate", methods=["GET", "POST"])
def certificate():

    if request.method == "POST":

        participant_id = request.form["participant_id"]

        connection = sqlite3.connect("ecosync.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT name, e_waste_type FROM participants WHERE participant_id = ?",
            (participant_id,)
        )

        participant = cursor.fetchone()

        connection.close()

        if participant:

            today = date.today()

            return render_template(
                "certificate_result.html",
                name=participant[0],
                e_waste_type=participant[1],
                date=today
            )

        else:
            return render_template("certificate_error.html")

    return render_template("certificate.html")


@app.route("/reports")
def reports():

    connection = sqlite3.connect("ecosync.db")
    cursor = connection.cursor()

    # Total participants
    cursor.execute("SELECT COUNT(*) FROM participants")
    total_participants = cursor.fetchone()[0]

    # Total e-waste collected
    cursor.execute(
        "SELECT COALESCE(SUM(quantity), 0) FROM collections"
    )
    total_e_waste = cursor.fetchone()[0]

    # E-waste summary
    cursor.execute("""
    SELECT e_waste_type, SUM(quantity)
    FROM collections
    GROUP BY e_waste_type
    """)

    waste_summary = cursor.fetchall()

    connection.close()

    return render_template(
        "reports.html",
        total_participants=total_participants,
        total_e_waste=total_e_waste,
        waste_summary=waste_summary
    )


if __name__ == "__main__":
    app.run(debug=True)