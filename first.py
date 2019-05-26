from flask import Flask ,flash , request , jsonify, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash


import sqlite3

app = Flask(__name__)
app.secret_key = "super secret key"


class User:
    def __init__(self, user):
        self.username = user['username']
        self.password = user['password']
        self.email = user['email']
        self.name = user['name']
    
    def save_to_db(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        try:
            cursor.execute('INSERT INTO users (username, password , email ,name) VALUES (?, ?, ?,?)', (self.username, self.password ,self.email, self.name))
        except:
            cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT , email TEXT, name TEXT)')
            cursor.execute('INSERT INTO users (username, password, email , name) VALUES (?, ?, ?, ?)', (self.username, self.password, self.email, self.name))
        finally:
            connection.commit()
            connection.close()
    
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        try:
            data = cursor.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
            data = {
                'username':data[1],
                'password':data[2],
                'email':data[3],
                'name':data[4]
            }

            if data:
                return cls(data)
        except:
            cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT, name TEXT)')
        finally:
            connection.close()

@app.route("/",methods=['GET'])
def main():
    return render_template('index.html')

@app.route("/signup",methods=['GET'])
def sgnup():
    return render_template('signup.html')

@app.route("/signup",methods=['POST'])
def sgnupPost():
    password = request.form['password']
    cpassword = request.form['cpassword']
    if cpassword != password:
        flash('Passwords do not match!','danger')
        return redirect(url_for('sgnup'))
    _user = {}
    _user['name'] = request.form['full_name']
    _user['email'] = request.form['email_address']
    _user['username'] = request.form['user_name']
    _user['password'] = generate_password_hash(request.form['password'])


    user = User.find_by_username(_user['username'])

    if user:
        flash('User already exists!','danger')
        return redirect(url_for('sgnup'))

    # users.append(_user)
    try:
        User(_user ).save_to_db()
        flash('Registration Successfull','success')
        return redirect(url_for('lgn'))
    except:
        flash('Something went wrong!','error')
        return redirect(url_for('lgn'))

@app.route("/login",methods=['GET'])
def lgn():
    return render_template('login.html')

@app.route("/login",methods=['POST'])
def lgnPost():
    username = request.form['username']
    password = request.form['password']

    user = User.find_by_username(username)
    
    if user and check_password_hash(user.password, password):
        flash('Logged In successfully!','success')
        return redirect(url_for('main'))          
    flash("Wrong Username or Password!",'danger')
    return redirect(url_for('lgn'))



if __name__=='__main__':
    app.run()

