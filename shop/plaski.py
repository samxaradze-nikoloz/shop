from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

con = sqlite3.connect('employ.db')
con.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')
con.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        address TEXT NOT NULL,
        card_number TEXT NOT NULL,
        expiry_date TEXT NOT NULL,
        cvv TEXT NOT NULL,
        cardholder_name TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')
con.commit()
con.close()

app = Flask(__name__, template_folder="temp")
app.secret_key = "your_secret_key_here"

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        con = sqlite3.connect("employ.db")
        cur = con.cursor()
        cur.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cur.fetchone():
            con.close()
            return render_template("register.html", error="Email already registered")
        cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        con.commit()
        con.close()
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        con = sqlite3.connect("employ.db")
        cur = con.cursor()
        cur.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, password))
        user = cur.fetchone()
        con.close()
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        else:
            return render_template("login.html", error="Invalid login")
    return render_template("login.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/savedetails", methods=["POST"])
def saveDetails():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    if request.method == "POST":
        try:
            address = request.form.get("address", "")
            card_number = request.form["card_number"]
            expiry_date = request.form["expiry_date"]
            cvv = request.form["cvv"]
            cardholder_name = request.form["cardholder_name"]
            with sqlite3.connect("employ.db") as con:
                cur = con.cursor()
                cur.execute("""
                    INSERT INTO orders (user_id, address, card_number, expiry_date, cvv, cardholder_name) 
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (user_id, address, card_number, expiry_date, cvv, cardholder_name))
                con.commit()
            return render_template("success.html", msg="Purchase successfully made")
        except Exception as e:
            return render_template("success.html", msg=f"Error: {str(e)}")
    return render_template("form.html")

@app.route('/costumers')
def view_customers():
    with sqlite3.connect('employ.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT id, username, email FROM users")
        customers = cur.fetchall()
    return render_template('custumers.html', customers=customers)

@app.route('/detales')
def view_card_details():
    with sqlite3.connect('employ.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""
            SELECT orders.id, users.username, orders.address, orders.card_number, orders.expiry_date, orders.cvv, orders.cardholder_name
            FROM orders
            JOIN users ON orders.user_id = users.id
        """)
        cards = cur.fetchall()
    return render_template('detales.html', cards=cards)

@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/deleterecord", methods=["POST"])
def deleterecord():
    id = request.form["id"]
    msg = ""
    with sqlite3.connect("employ.db") as con:
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM orders WHERE id = ?", (id,))
            con.commit()
            msg = "Record successfully deleted"
        except Exception as e:
            msg = f"Cannot delete record: {e}"
    return render_template("delete_record.html", msg=msg)

@app.route("/creators")
def creators():
    return render_template("creators.html")

@app.route("/wheel")
def wheel():
    return render_template("wheel.html")

if __name__ == "__main__":
    app.run(debug=True)
