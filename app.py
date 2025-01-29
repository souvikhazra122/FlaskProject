from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)

def connect_db():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="Mysql@123",
            database="Salary",
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/add_employee', methods=['POST'])
def add_employee():
    try:
        data = request.json
        name = data.get("name")
        salary = data.get("salary")

        if not name or not salary:
            return jsonify({"error": "Missing name or salary"}), 400

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user_data (employee_name, salary) VALUES (%s, %s)", (name, salary))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"message": f"Employee {name} added successfully!"})
        return jsonify({"error": "Database connection failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_employees', methods=['GET'])
def get_employees():
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_data")
            employees = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify(employees)
        return jsonify({"error": "Database connection failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_employee', methods=['POST'])
def update_employee():
    try:
        data = request.json
        emp_id = data.get("id")
        name = data.get("name")
        salary = data.get("salary")

        if not emp_id or not name or not salary:
            return jsonify({"error": "Missing fields"}), 400

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE user_data SET employee_name=%s, salary=%s WHERE id=%s", (name, salary, emp_id))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"message": "Employee updated successfully!"})
        return jsonify({"error": "Database connection failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    try:
        data = request.json
        emp_id = data.get("id")

        if not emp_id:
            return jsonify({"error": "Missing employee ID"}), 400

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_data WHERE id=%s", (emp_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"message": "Employee deleted successfully!"})
        return jsonify({"error": "Database connection failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
