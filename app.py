from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "employee123"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="AishuShiro13",
    database="company"
)

cursor = db.cursor(dictionary=True)

# Registration
@app.route("/", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        address = request.form["address"]
        department = request.form["department"]
        city = request.form["city"]
        salary = request.form["salary"]
        experience = request.form["experience"]
        email = request.form["email"]
        phone = request.form["phone"]
        username = request.form["username"]
        password = request.form["password"]

        sql = """
        INSERT INTO employees
        (name, age, address, department, city, salary, experience, email, phone, username, password)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            name,
            age,
            address,
            department,
            city,
            salary,
            experience,
            email,
            phone,
            username,
            password
        )

        cursor.execute(sql, values)
        db.commit()

        return redirect("/view")

    return render_template("register.html")
# View Employees
@app.route("/view")
def view():

    search = request.args.get("search")

    if search:

        sql = "SELECT * FROM employees WHERE name LIKE %s"
        value = ("%" + search + "%",)

        cursor.execute(sql, value)

    else:

        cursor.execute("SELECT * FROM employees")

    data = cursor.fetchall()

    return render_template("view.html", data=data)
# Edit Employee
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        department = request.form["department"]

        sql = """
        UPDATE employees
        SET name=%s, age=%s, department=%s
        WHERE id=%s
        """

        cursor.execute(sql, (name, age, department, id))
        db.commit()

        return redirect("/view")

    cursor.execute("SELECT * FROM employees WHERE id=%s", (id,))
    employee = cursor.fetchone()

    return render_template("edit.html", employee=employee)


# Delete Employee
@app.route("/delete/<int:id>")
def delete(id):

    cursor.execute(
        "DELETE FROM employees WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect("/view")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT * FROM employees WHERE username=%s AND password=%s"
        cursor.execute(sql, (username, password))

        employee = cursor.fetchone()

        if employee:
            session["user_id"] = employee["id"]
            session["username"] = employee["username"]
            return redirect("/dashboard")
        else:
            return "Invalid Username or Password"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    cursor.execute("SELECT * FROM employees WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    return render_template("dashboard.html", user=user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)

