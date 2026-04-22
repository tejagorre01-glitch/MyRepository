from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

# ===========================
# DATABASE CONNECTION
# ===========================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="expense_tracker",
    port=3306
)
cursor = db.cursor(dictionary=True)

# ===========================
# FLASK APP SETUP
# ===========================
app = Flask(__name__)
app.secret_key = "secret123"

# ===========================
# ROOT ROUTE (ALWAYS LOGIN FIRST)
# ===========================
@app.route("/")
def root():
    if "user" in session:
        return redirect("/home")
    return redirect("/login")

# ===========================
# LOGIN
# ===========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        if user:
            session["user"] = username
            return redirect("/home")
        else:
            return "Invalid username or password"

    return render_template("login.html")

# ===========================
# SIGNUP
# ===========================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        db.commit()
        return redirect("/login")

    return render_template("signup.html")

# ===========================
# HOME / EXPENSE PAGE
# ===========================
@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/login")

    cursor.execute("SELECT member_id, member_name FROM members")
    members = cursor.fetchall()

    cursor.execute("""
        SELECT e.id, e.name, e.amount, e.category,
               m.member_name, e.date,
               e.payee, e.description, e.mode_of_payment
        FROM expenses e
        LEFT JOIN members m ON e.member_id = m.member_id
    """)
    expenses = cursor.fetchall()

    return render_template("index.html", expenses=expenses, members=members)

# ===========================
# ADD EXPENSE
# ===========================
@app.route("/add_expense", methods=["POST"])
def add_expense():
    if "user" not in session:
        return redirect("/login")

    cursor.execute("""
        INSERT INTO expenses
        (name, amount, category, date, member_id, payee, description, mode_of_payment)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        request.form["name"],
        request.form["amount"],
        request.form["category"],
        request.form["date"],
        request.form["member_id"],
        request.form["payee"],
        request.form["description"],
        request.form["mode_of_payment"]
    ))

    db.commit()
    return redirect("/home")

# ===========================
# DELETE EXPENSE
# ===========================
@app.route("/delete/<int:id>")
def delete_expense(id):
    if "user" not in session:
        return redirect("/login")

    cursor.execute("DELETE FROM expenses WHERE id=%s", (id,))
    db.commit()
    return redirect("/home")

# ===========================
# EDIT EXPENSE
# ===========================
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_expense(id):
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        cursor.execute(
            "UPDATE expenses SET name=%s, amount=%s, date=%s WHERE id=%s",
            (request.form["name"], request.form["amount"], request.form["date"], id)
        )
        db.commit()
        return redirect("/home")

    cursor.execute("SELECT * FROM expenses WHERE id=%s", (id,))
    expense = cursor.fetchone()
    return render_template("edit.html", expense=expense)

# ===========================
# MEMBERS
# ===========================
@app.route("/members")
def members_page():
    if "user" not in session:
        return redirect("/login")

    cursor.execute("""
        SELECT m.member_id, m.member_name,
               IFNULL(SUM(e.amount), 0) AS total
        FROM members m
        LEFT JOIN expenses e ON m.member_id = e.member_id
        GROUP BY m.member_id
    """)
    members = cursor.fetchall()

    return render_template("index1.html", members=members)

@app.route("/add_member", methods=["POST"])
def add_member():
    cursor.execute(
        "INSERT INTO members (member_name) VALUES (%s)",
        (request.form["member_name"],)
    )
    db.commit()
    return redirect("/members")

@app.route("/delete_member/<int:id>")
def delete_member(id):
    cursor.execute("DELETE FROM members WHERE member_id=%s", (id,))
    db.commit()
    return redirect("/members")

# ===========================
# BALANCES
# ===========================
@app.route("/balances")
def balances():
    if "user" not in session:
        return redirect("/login")

    cursor.execute("SELECT COUNT(*) AS cnt FROM members")
    member_count = cursor.fetchone()["cnt"]

    cursor.execute("SELECT SUM(amount) AS total FROM expenses")
    total_expense = cursor.fetchone()["total"] or 0

    if member_count == 0:
        return render_template("balances.html", balances=[])

    share = total_expense / member_count

    cursor.execute("""
        SELECT m.member_name, SUM(e.amount) AS spent
        FROM members m
        LEFT JOIN expenses e ON m.member_id = e.member_id
        GROUP BY m.member_id
    """)
    data = cursor.fetchall()

    balances = []
    for row in data:
        spent = row["spent"] or 0
        balances.append({
            "name": row["member_name"],
            "spent": spent,
            "share": round(share, 2),
            "balance": round(spent - share, 2)
        })

    return render_template("balances.html", balances=balances)

# ===========================
# MONTHLY EXPENSES
# ===========================
@app.route("/monthly")
def monthly():
    cursor.execute("SELECT * FROM monthly_expenses")
    expenses = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) AS total FROM monthly_expenses")
    result = cursor.fetchone()
    total = result["total"] if result and result["total"] else 0

    return render_template(
        "monthly.html",
        expenses=expenses,
        total=total
        )

@app.route("/add_monthly", methods=["POST"])
def add_monthly():
    cursor.execute("""
        INSERT INTO monthly_expenses
        (expense_name, amount, month_year, description)
        VALUES (%s,%s,%s,%s)
    """, (
        request.form["expense_name"],
        request.form["amount"],
        request.form["month_year"],
        request.form["description"]
    ))
    db.commit()
    return redirect("/monthly")

@app.route("/delete_monthly/<int:id>")
def delete_monthly(id):
    cursor.execute("DELETE FROM monthly_expenses WHERE id=%s", (id,))
    db.commit()
    return redirect("/monthly")

# ===========================
# LOGOUT
# ===========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ===========================
# OFFLINE SYNC ROUTES (PWA)
# ===========================
@app.route("/sync_expenses", methods=["POST"])
def sync_expenses():
    for e in request.json:
        cursor.execute("""
            INSERT INTO expenses (name, amount, category, date)
            VALUES (%s,%s,%s,%s)
        """, (e["name"], e["amount"], e["category"], e["date"]))
    db.commit()
    return {"status": "expenses synced"}

@app.route("/sync_monthly", methods=["POST"])
def sync_monthly():
    for e in request.json:
        cursor.execute("""
            INSERT INTO monthly_expenses
            (expense_name, amount, month_year, description)
            VALUES (%s,%s,%s,%s)
        """, (
            e["expense_name"],
            e["amount"],
            e["month_year"],
            e["description"]
        ))
    db.commit()
    return {"status": "monthly synced"}

# ===========================
# START SERVER
# ===========================
if __name__ == "__main__":
    app.run(debug=True)
