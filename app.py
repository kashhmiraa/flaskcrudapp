try :
    from flask import Flask, render_template, request, flash
    from flask_mysqldb import MySQL
    import re
    import os
    from werkzeug.utils import secure_filename
    app = Flask(__name__)
    UPLOAD_FOLDER = 'C:/Users/KashmiraRaghuwanshi/OneDriveDesktop/flaskform/static'
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg'}
    app.secret_key = "secret key"
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'Ihatemaths#02'
    app.config['MYSQL_DB'] = 'mydb'
    mysql = MySQL(app)
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == "POST":
            details = request.form
            name = details['name']
            email = details['email']
            phone = details['phone']
            dob = details['dateofbirth']
            file = request.files['image_file']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            profile_picture = convertToBinaryData("C:/Users/KashmiraRaghuwanshi/OneDriveDesktop/flaskform/static/image_file")
            regex_email = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
            if re.fullmatch(regex_email, email):
                flag = 1
            else:
                raise ValueError("Invalid email format")
            regex_phone = r'(^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$)'
            if re.fullmatch(regex_phone, phone):
                flag = 1
            else:
                raise ValueError("Invalid phone number")
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO storage(name, email, phone, dob, profile_picture) VALUES (%s, %s, %s,%s,%s)", (name, email, phone, dob,profile_picture))
            mysql.connection.commit()
            cur.execute("select * from storage")
            data = cur.fetchall()
            cur.close()
            return render_template("template.html", data=data)
        return render_template('index.html')
    def convertToBinaryData(filename):
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData
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
            dob = details['dateofbirth']
            id_data=details['id']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE storage set name=%s,email=%s,phone=%s,dob=%s where id=%s",(name,email,phone,dob,id_data))
            mysql.connection.commit()
            return 'UPDATED SUCCESSFULLY'
except OSError:
    print("Operating System Error")
if __name__ == '__main__':
    app.run(debug=True)