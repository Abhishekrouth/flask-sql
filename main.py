from flask import Flask,request,jsonify, abort
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'students'

mysql = MySQL(app)

@app.route('/newEntry', methods=['POST'])
def add_student():
    name = request.form['name']
    subject = request.form['subject'] 
    Marks = request.form['Marks']

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO Marks (name, subject, Marks) VALUES (%s, %s, %s)",
        (name, subject, Marks)
    )
    mysql.connection.commit()
    cursor.close()
    return "User added successfully!"

@app.route('/showMarks', methods=['GET'])
def stu_details():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Marks")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

@app.route('/deleteMarks/<name>', methods=['DELETE'])
def del_marks(name):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Marks WHERE name=%s", (name,))
    mysql.connection.commit()
    cursor.close()
    return f"Marks of {name} deleted successfully"

@app.route('/editMarks/<name>', methods=['PUT'])
def edit_marks(name):
    marks = request.form.get('Marks')
    if not name:
        return "Name is required to update a record", 400
    if not marks:
        return "Marks value is required", 400
    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE Marks SET Marks=%s WHERE name=%s",
        (marks, name)
    )
    mysql.connection.commit()
    cursor.close()

    return f"Record of {name} updated successfully"

if __name__ == "__main__":
    app.run(debug=True)
