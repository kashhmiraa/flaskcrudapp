from base64 import b64encode
from flask import Flask, render_template, request, flash, url_for , redirect
from flask_mysqldb import MySQL
import re
import os
from werkzeug.utils import secure_filename
try :
    app = Flask(__name__)
    UPLOAD_FOLDER = 'static/uploads/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg'}
    app.secret_key = "secret key"
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'Ihatemaths#02'
    app.config['MYSQL_DB'] = 'mydb'
    mysql = MySQL(app)
    def check_email(email):
        try:
           regex_email = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
           if re.fullmatch(regex_email, email)==None:
               raise ValueError
        except ValueError:
            msg = 'The email has an invalid format'
            return msg
        try:
           cur = mysql.connection.cursor()
           cur.execute("select id from storage where email=%s", [email])
           data = cur.fetchone()
           cur.close()
           if data:
               raise ValueError
        except ValueError:
            msg = 'Email already exists'
            return msg
    def check_phone(phone):
        try:
            regex_phone = r'(^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$)'
            if re.fullmatch(regex_phone, phone)==None:
                raise ValueError
        except ValueError:
            msg = 'The phone no has an invalid format'
            return msg
        try:
           cur = mysql.connection.cursor()
           cur.execute("select id from storage where phone=%s", [phone])
           data = cur.fetchone()
           cur.close()
           if data:
                raise ValueError
        except ValueError:
           msg = 'Phone no already exists'
           return msg
    def convertToBinaryData(filename):
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData
    @app.route('/', methods=['GET', 'POST'])
    def view():
        cur = mysql.connection.cursor()
        cur.execute("select * from storage")
        data = cur.fetchall()
        length_of_data = len(data)
        cur.close()
        l = []
        for i in range(len(data)):
            if data[i][4] is None:
                l.append('no_image')
            else:
                image = b64encode(data[i][4]).decode("utf-8")
                l.append(image)
        return render_template("template.html", data=data, l=l, i=i, length_of_data=length_of_data)
    @app.route('/formpage', methods=['GET','POST'])
    def index():
        if request.method == "POST":
            details = request.form
            name = details['name']
            email = details['email']
            phone = details['phone']
            file = request.files['image_file']
            if file:
               file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            file_name = secure_filename(file.filename)
            profile_picture = convertToBinaryData('C:/Users/Kashmira Raghuwanshi/OneDrive/Desktop/flaskform/static/uploads/' + file_name)
            if check_email(email):
                return check_email(email)
            if check_phone(phone):
                return check_phone(phone)
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO storage(name, email, phone,profile_picture) VALUES (%s, %s, %s,%s)",  (name, email, phone, profile_picture))
            mysql.connection.commit()
            msg = "The form is submitted successfully"
            return render_template('index.html', msg=msg)
        return render_template('index.html')
    @app.route('/delete/<string:id>')
    def delete(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE from storage where id=%s", [id])
        mysql.connection.commit()
        return 'Deleted Successfully'
    @app.route('/update/<string:id>')
    def update(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from storage where id=%s", [id])
        data = cur.fetchall()
        cur.close()
        return render_template("update.html", data=data)
    @app.route('/updatedata',methods=['GET','POST'])
    def updatedata():
        if request.method == "POST":
            details = request.form
            name = details['name']
            email = details['email']
            phone = details['phone']
            file = request.files['image_file']
            if file:
               file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            file_name = secure_filename(file.filename)
            profile_picture = convertToBinaryData('C:/Users/Kashmira Raghuwanshi/OneDrive/Desktop/flaskform/static/uploads/' + file_name)
            id_data=details['id']
            if check_email(email):
                return check_email(email)
            if check_phone(phone):
                return check_phone(phone)
            cur = mysql.connection.cursor()
            cur.execute("UPDATE storage set name=%s,email=%s,phone=%s,profile_picture=%s where id=%s",(name, email, phone, profile_picture, id_data))
            mysql.connection.commit()
            return 'UPDATED SUCCESSFULLY'
except OSError:
    print("Operating System Error")
except ValueError:
    print("This email already being used")
if __name__ == '__main__':
    app.run(debug=True)

