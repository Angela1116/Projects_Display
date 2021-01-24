from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:angelaxu@localhost/height_collector' #address of database,app will know where to look for database
#app.config['SQLALCHEMY_DATABASE_URI']='postgres://bmlafugnjiobqa:4b970831bfb494578a5f8efb973a02fcd039e4af14a622d6c3fb6e39f720d962@ec2-54-163-47-62.compute-1.amazonaws.com:5432/d92m9hlro0ol47?sslmode=require'   #bmlafugnjiobqa is user name, 4b..is password. @ec2-54....is server address. port is 5432 d92..is database name
#app.config['SQLALCHEMY_DATABASE_URI']='postgres://pcczwsuyuiltzn:1cbe14479def61f0e4afdcb024a67bb03360777c5fb85d52323df77677ed3846@ec2-54-144-45-5.compute-1.amazonaws.com:5432/d5j0diu71erel8?sslmode=require'
db=SQLAlchemy(app) #create a SQLAlchemy object for your flask application


class Data(db.Model): #line 11 to 19 is create data Model
    __tablename__="data" #instruction, tabble name is 'data'
    id=db.Column(db.Integer,primary_key=True)
    email_=db.Column(db.String(120), unique=True) #max charactor is 120
    height_=db.Column(db.Integer)

    def __init__(self, email_, height_):  #init variables
        self.email_=email_
        self.height_=height_


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST']) #if you need POST method just specify it in route()
def success():
    if request.method=='POST':             #line 28 to 30 is capture the data from user are pass to the server by POST method
        email = request.form["email_name"] #line 29 & 30 should match index.html file line from 15 to 17
        height=request.form["height_name"]
        #print(email, height)
        if db.session.query(Data).filter(Data.email_==email).count()==0: #avoid repeated email address
            data=Data(email,height) #create Data object
            db.session.add(data) # add data to postgreSQL
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height_)).scalar() #calcu average height
            average_height=round(average_height,1) #around average_height to one decimal point
            #print(average_height)
            count=db.session.query(Data.height_).count() #count how many  height in database we stored
            send_email(email, height, average_height,count)
            return render_template("success.html")
    return render_template('index.html',
     text="we've got height information from this email address already!") # set an alert message to repeated user



if __name__ == '__main__':
    app.debug=True
    app.run() #specify port by passing  a parameter(port=5001) otherwise will run port 5000

#Line 26 to 43 is mapping success url
#Line 1,6,22-24,47-49 build and run index html, go localhost:5000 to see it

#Note: we can call Data() class but it will execute flask app, so we go to command line and trigger python session we can import DB object : python -> from app import db -> db.create_all() after done this we will see id,email_,height_ in postgreSQL database showed 0 rows.

#How to save user`s data to PostgreSQL? when user press submit button will go to 'index.html' file line 15, then will execute line 27 success function in this file, and send user`s data to PostgreSQL database table 'data' we create before
