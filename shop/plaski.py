from flask import Flask, render_template, request,session, redirect, url_for, render_template, flash
import sqlite3


con = sqlite3.connect('employ.db')
print("Database opened successfully")
con.execute('''
    CREATE TABLE IF NOT EXISTS employ (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        address TEXT NOT NULL,
        card_number TEXT NOT NULL,
        expiry_date TEXT NOT NULL,
        cvv TEXT NOT NULL,
        cardholder_name TEXT NOT NULL
    )
''')
con.close()


print("Table created successfully")
con.close()


app = Flask(__name__, template_folder="temp")

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/add")
def add():
    return render_template("add.html")
@app.route("/savedetails", methods=["POST", "GET"])
def saveDetails():
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            card_number = request.form["card_number"]
            expiry_date = request.form["expiry_date"]
            cvv = request.form["cvv"]
            cardholder_name = request.form["cardholder_name"]

            with sqlite3.connect("employ.db") as con:
                cur = con.cursor()
                cur.execute("""
                    INSERT INTO employ (name, email, address, card_number, expiry_date, cvv, cardholder_name) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (name, email, address, card_number, expiry_date, cvv, cardholder_name))
                user_id = cur.lastrowid
                con.commit()
                return render_template("success.html", msg="Purchase succesfouly made", user_id=user_id)

        except Exception as e:
            try:
                con.rollback()
            except:
                pass
            return render_template("success.html", msg=f"Error: {str(e)}") 
    return render_template("form.html")



@app.route("/view")
def view():
    con = sqlite3.connect('employ.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM employ")
    rows = cur.fetchall()
    return render_template("view.html", rows=rows)

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
            cur.execute("DELETE FROM employ WHERE id = ?", (id,))
            con.commit()
            msg = "Record successfully deleted"
        except Exception as e:
            msg = f"Cannot delete record: {e}"
        finally:
            return render_template("delete_record.html", msg=msg)




    
@app.route("/creators")
def creators():
    return render_template("creators.html")



    
@app.route("/wheel")
def wheel():
    return render_template("wheel.html")




if __name__ == "__main__":
    app.run(debug=True)