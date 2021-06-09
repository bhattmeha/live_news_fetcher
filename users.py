from flask import Flask,render_template,request
import pymysql as sql
from flask_mail import Mail,Message
import os
from newsapi import NewsApiClient
import requests,json
from bs4 import BeautifulSoup
import requests
 





app = Flask(__name__)

#source = requests.get('https://www.flipkart.com/').text
#soup = BeautifulSoup(source, 'lxml')
#print(soup)

mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'bhatt.meha45@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_HOST_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

@app.route('/')
def index():
    
    
    return render_template("one.html")
    #return "hello world"


@app.route("/home/<var>/")
def home(var):
    return render_template("one.html",name=var)
    
@app.route('/login/')
def login():
    return render_template("login.html")


@app.route("/afterlogin/",methods=['POST'])
def afterlogin():
    email = request.form.get('email')
    password = request.form['pswd']
    try:
        db = sql.connect(host="localhost",port=3306,user="root",password="",database="project")
    except:
        return "Connectivity Error...."
    else:
        c = db.cursor()
        c.execute(f"select * from user where email='{email}'")
        data = c.fetchone()
        if data:
            #print(data)
            if password == data[2]:
                return render_template("nav.html")
            else:
                error = "Invalid password"
                return render_template("login.html",error=error)
        else:
            error = "No such user...."
            return render_template("login.html",error=error)
    return f"Email {email} and password {password}"

@app.route("/signup/")
def signup():
    return render_template("signup.html")

@app.route("/aftersignup/",methods=['POST'])
def signup1():
    email = request.form.get('email')
    password = request.form.get('pswd')
    username = request.form.get('uname')
    gender = request.form.get('gender')
    try:
        db = sql.connect(host="localhost",port=3306,user="root",password="",database="project")
    except:
        return "Connectivity Error...."
    else:
        c = db.cursor()
        c.execute(f"select * from user where email = '{email}'")
        data = c.fetchone()
        print(data)
        if data:
            error = "User already exist....."
            return render_template("signup.html",error=error)
        else:
            cmd = f"insert into user values('{username}','{email}','{password}','{gender}')"
            c.execute(cmd)
            db.commit()
            return render_template("login.html")
@app.route("/about/")
def about():
    newsapi = NewsApiClient(api_key="b0f75ce660c0466a9a98c2478f8abb62")
    topheadlines = newsapi.get_top_headlines(sources="al-jazeera-english")
 
 
    articles = topheadlines['articles']
 
    desc = []
    news = []
    img = []
 
 
    for i in range(len(articles)):
        myarticles = articles[i]
 
 
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
 
 
 
    mylist = zip(news, desc, img)
 
 
    return render_template('about.html', context = mylist)
 
 

@app.route("/contact/")
def contact():
    to = "bhatt.meha45@gmail.com"
    body = """This is a message to all the students."""
    m = Message(subject="Mail from flask app",recipients=["bhatt.meha45@gmail.com"],body=body,sender="bhatt.meha45@gmail.com")
    mail.send(m)
    return "SUCCESS"


@app.route("/afterlogin1/",methods=['POST'])
def afterlogin1():
     pass

   


app.run(host="localhost",port=80,debug=True)

