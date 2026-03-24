from flask import Flask, render_template, request, redirect, url_for, session
import random
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "secret123"

users_db = {}

# ---------------- EMAIL OTP FUNCTION ----------------

def send_otp(email, otp):

    sender_email = "ramaasubasini@gmail.com"
    app_password = "hbqv olfu iput vzoy"

    msg = MIMEText(f"Your OTP is: {otp}")
    msg["Subject"] = "OTP Verification"
    msg["From"] = sender_email
    msg["To"] = email

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(sender_email,app_password)
    server.sendmail(sender_email,email,msg.as_string())
    server.quit()

# ---------------- COURSES ----------------

courses = [
{"name":"Python","youtube":"https://youtu.be/_uQrJ0TkZlc","website":"https://python.org"},
{"name":"Java","youtube":"https://youtu.be/grEKMHGYyns","website":"https://oracle.com/java"},
{"name":"C Programming","youtube":"https://youtu.be/KJgsSFOSQv0","website":"https://learn-c.org"},
{"name":"C++","youtube":"https://youtu.be/vLnPwxZdW4Y","website":"https://cplusplus.com"},
{"name":"JavaScript","youtube":"https://youtu.be/W6NZfCO5SIk","website":"https://developer.mozilla.org"},
{"name":"HTML","youtube":"https://youtu.be/UB1O30fR-EE","website":"https://developer.mozilla.org"},
{"name":"CSS","youtube":"https://youtu.be/yfoY53QXEnI","website":"https://developer.mozilla.org"},
{"name":"React","youtube":"https://react.dev","website":"https://react.dev"},
{"name":"NodeJS","youtube":"https://nodejs.org","website":"https://nodejs.org"},
{"name":"Flask","youtube":"https://flask.palletsprojects.com","website":"https://flask.palletsprojects.com"},
{"name":"Django","youtube":"https://djangoproject.com","website":"https://djangoproject.com"},
{"name":"SQL","youtube":"https://mysql.com","website":"https://mysql.com"},
{"name":"MongoDB","youtube":"https://mongodb.com","website":"https://mongodb.com"},
{"name":"Machine Learning","youtube":"https://scikit-learn.org","website":"https://scikit-learn.org"},
{"name":"Deep Learning","youtube":"https://tensorflow.org","website":"https://tensorflow.org"},
{"name":"Data Science","youtube":"https://datasciencecentral.com","website":"https://datasciencecentral.com"},
{"name":"Cyber Security","youtube":"https://cybrary.it","website":"https://cybrary.it"},
{"name":"Cloud Computing","youtube":"https://aws.amazon.com","website":"https://aws.amazon.com"},
{"name":"AWS","youtube":"https://aws.amazon.com","website":"https://aws.amazon.com"},
{"name":"Docker","youtube":"https://docker.com","website":"https://docker.com"},
{"name":"Kubernetes","youtube":"https://kubernetes.io","website":"https://kubernetes.io"},
{"name":"Git","youtube":"https://git-scm.com","website":"https://git-scm.com"},
{"name":"Linux","youtube":"https://linux.org","website":"https://linux.org"},
{"name":"Networking","youtube":"https://cisco.com","website":"https://cisco.com"},
{"name":"Operating System","youtube":"https://geeksforgeeks.org","website":"https://geeksforgeeks.org"},
{"name":"Software Engineering","youtube":"https://geeksforgeeks.org","website":"https://geeksforgeeks.org"},
{"name":"Data Structures","youtube":"https://geeksforgeeks.org","website":"https://geeksforgeeks.org"},
{"name":"Algorithms","youtube":"https://geeksforgeeks.org","website":"https://geeksforgeeks.org"},
{"name":"Android Development","youtube":"https://developer.android.com","website":"https://developer.android.com"},
{"name":"UI UX","youtube":"https://interaction-design.org","website":"https://interaction-design.org"},
{"name":"Power BI","youtube":"https://powerbi.microsoft.com","website":"https://powerbi.microsoft.com"}
]

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register',methods=['GET','POST'])
def register():

    if request.method=='POST':

        username=request.form['username']
        email=request.form['email']
        password=request.form['password']

        otp=random.randint(100000,999999)

        session['otp']=str(otp)

        session['temp_user']={
            "username":username,
            "email":email,
            "password":password
        }

        send_otp(email,otp)

        return redirect(url_for('verify'))

    return render_template("register.html")


@app.route('/verify',methods=['GET','POST'])
def verify():

    if request.method=='POST':

        entered=request.form['otp']

        if entered==session.get('otp'):

            user=session.get('temp_user')

            users_db[user['username']]=user

            session['user']=user['username']

            return render_template("verified.html")

        else:
            return render_template("verify.html",error="Wrong OTP")

    return render_template("verify.html")


@app.route('/login',methods=['GET','POST'])
def login():

    if request.method=='POST':

        username=request.form['username']
        password=request.form['password']

        user=users_db.get(username)

        if user and user['password']==password:

            session['user']=username

            return redirect(url_for('dashboard'))

        else:
            return render_template("login.html",error="Invalid Login")

    return render_template("login.html")


@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template("dashboard.html")


@app.route('/courses')
def courses_page():

    return render_template("courses.html",courses=courses)


@app.route('/profile')
def profile():

    user=users_db.get(session['user'])

    return render_template("profile.html",user=user)


@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))


if __name__=="__main__":
    app.run(debug=False)