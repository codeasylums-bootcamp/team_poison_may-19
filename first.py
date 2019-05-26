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

            if data:
                data = {
                    'username':data[1],
                    'password':data[2],
                    'email':data[3],
                    'name':data[4]
                }
                return cls(data)
        except:
            cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT, name TEXT)')
        finally:
            connection.close()

@app.route("/",methods=['GET'])
def main():
    return render_template('index.html')

@app.route("/",methods=['POST'])
def main1():
    source = request.form['Source']
    dest = request.form['Destination']
    date = request.form['Date_of_Journey']
    sel()
    return redirect(url_for('det'))

@app.route("/details",methods=['GET'])
def det():
    return render_template('details.html')

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

def sel():
    import time
    import gettext
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.keys import Keys
    
    browser = webdriver.Firefox()
    browser.get("https://www.irctc.co.in/nget/train-search")

    # username = browser.find_element_by_id("user_name")
    # password = browser.find_element_by_id("password")
    # from_station   = browser.find_element_by_id("origin")

    from_station = browser.find_element_by_xpath('//*[@id="origin"]/span/input')
    to_station = browser.find_element_by_xpath('//*[@id="destination"]/span/input')
    date = browser.find_element_by_xpath('//input[@placeholder="Journey Date(dd-mm-yyyy)*"]')

    from_station.click()
    from_station.send_keys("RNC")
    time.sleep(1)
    from_station.send_keys(Keys.RETURN)

    to_station.click()
    to_station.send_keys("NDLS")
    time.sleep(1)
    to_station.send_keys(Keys.RETURN)

    for i in range(10):
        date.send_keys(Keys.BACKSPACE)
    date.send_keys('30-05-2019')
    time.sleep(1)
    date.send_keys(Keys.RETURN)

    time.sleep(5)

    # element = browser.find_elements_by_xpath("//span")
    # browser.execute_script("arguments[0].style.visibility='hidden'", element)

    time.sleep(2)

    # status = browser.find_element_by_xpath('//a[@id="T_12453"]/../../../../div[3]/div[2]/div/span[@class="waitingstatus"].getText()')
    # print(status)
    found = browser.find_element_by_xpath('//a[@id="T_12453"]/../../../../div[3]/div[2]/div/div/button')
    # found = browser.find_elements_by_xpath('//button[@id="check-availability"]')[0]
    found.send_keys(Keys.RETURN)



    time.sleep(10)
    book_now = browser.find_elements_by_xpath('//button[@class="b1"]')[0]
    book_now_text = book_now.get_attribute("aria-label")
    book_list = book_now_text.split()
    book_now.send_keys(Keys.RETURN)
    time.sleep(6)
    def check(word, book_list):
        if word in book_list:
            book_now.send_keys(Keys.RETURN)

    check('RAC',book_list)
    time.sleep(5)
    login_Id = browser.find_element_by_id('userId')
    login_Id.send_keys('rameleswar')
    login_Id.send_keys(Keys.TAB)

    login_pw = browser.find_element_by_id('pwd')
    login_pw.send_keys('nsso(fod)')
    login_pw.send_keys(Keys.TAB)

    time.sleep(10)


    captcha = browser.find_element_by_id('nlpAnswer')
    captcha.send_keys("Invesco")
    sign_in = browser.find_element_by_xpath('//button[@class="search_btn"]')
    # captcha.send_keys(Keys.RETURN)

    login_pw.click()
    login_pw.send_keys(Keys.RETURN)


    time.sleep(20)



    psgn_name = "LAlitha"
    psgn_age = "21"
    psgn_gender = "female"

    psgn = browser.find_element_by_id('psgn-name')
    psgn = send_keys(psgn_name)


    psgn.send_keys(Keys.Tab)
    psgn.send_keys(psgn_age)
    psgn.send_keys(Keys.Tab)

    if psgn_gender == "Male":
        psgn.send_keys(Keys.ARROW_DOWN)
    elif psgn_gender == "Female":
        psgn.send_keys(Keys.ARROW_DOWN)
        psgn.send_keys(Keys.ARROW_DOWN)


    # book_now.send_keys(Keys.RETURN)
    # book_now.send_keys('nsso(fod)')
    # book_now.send_keys(Keys.RETURN)



    # book_now.send_keys(Keys.RETURN)
    # print(len(book_now))


  


if __name__=='__main__':
    app.run()

