import base64
import os
from datetime import timedelta
from functools import wraps
from random import randint

from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_bootstrap import Bootstrap
from werkzeug.urls import url_encode

from utils import databaseUtils


UPLOAD_FOLDER = "C:\\Users\\18452\\Documents\\Development\\WebDev\\NestEgg\\static\\img"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'wav'}


def require_login(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if 'user' not in session:
            flash("Please log in to create posts")
            return redirect(url_for("login"))
        else:
            return f(*args, **kwargs)

    return inner


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(16)
Bootstrap(app)


@app.template_global()
def modify_query(origin, **new_values):
    args = request.args.copy()

    for key, value in new_values.items():
        args[key] = value

    return '{}?{}'.format(origin, url_encode(args))


@app.route('/')
def root():
    return render_template("home.html")


@app.route("/report")
@require_login
def report():
    return render_template("report.html")


@app.route("/jobs", methods=["GET", "POST"])
def jobs():
    return render_template("jobs.html", jobs=databaseUtils.get_jobs())


@app.route("/job")
def job():
    return render_template("job.html", job=databaseUtils.get_job_by_id(request.args.get('jobid')))


@app.route("/apply", methods=["GET","POST"])
def apply():
    databaseUtils.apply(session['user'], request.form['jobid'])

    flash("Application Recieved!")
    return redirect(url_for('jobs'))


@app.route("/createJob")
@require_login
def createJob():
    return render_template("createJob.html")


@app.route("/postJob", methods=["GET", "POST"])
@require_login
def postJob():
    if 'position' not in request.form or 'company' not in request.form or 'term' not in request.form or 'requirements' not in request.form or 'location' not in request.form or 'salary' not in request.form:
        flash("No field can be left blank")
        return redirect(url_for("createJob"))

    temp = databaseUtils.add_job(request.form['position'], request.form['company'], request.form['term'],
                                 request.form['requirements'], request.form['location'], request.form['salary'],
                                 request.form['description'])

    flash("Job Posted!")
    return redirect(url_for('jobs'))


@app.route("/housing")
def housing():
    return render_template("housing.html", houses=databaseUtils.get_houses())


@app.route("/createHouse", methods=["GET", "POST"])
@require_login
def createHouse():
    return render_template("createHouse.html")


@app.route("/postHouse", methods=["GET", "POST"])
@require_login
def postHouse():
    filename = str(randint(0, 999999999999)) + ".png"
    print(request.files)

    if 'price' not in request.form or 'location' not in request.form or 'term' not in request.form:
        flash("No field can be left blank")
        return redirect(url_for("createHouse"))
    if 'file' not in request.files:
        flash("No File Uploaded")
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash("No  selected file")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    databaseUtils.add_house(request.form['price'], request.form['location'], request.form['term'], session['user'],
                            filename)

    flash("Listing Posted!")
    return redirect(url_for('housing'))


@app.route("/classes")
def classes():
    return render_template("classes.html", classes=databaseUtils.get_classes())


@app.route("/createClass", methods=["GET", "POST"])
def create_class():
    if request.args.get('numPages'):
        return render_template("createClass.html", numPages=request.args.get('numPages'))


    else:
        return render_template("createClass.html", numPages=1)


@app.route("/postClass", methods=["GET", "POST"])
def post_class():
    print(request.form)
    print(request.files)

    pages = []

    for i in range(int(request.form['totalPages'])):
        print(i)
        type = request.form['pageType' + str(i)]
        tempPage = {
            'title': request.form['page-' + str(i + 1) + '-title'],
            'type': type
        }

        if type == 'Text':
            tempPage['text'] = request.form['text' + str(i)]

        elif type == 'Audio':
            filename = str(randint(0, 999999999999)) + ".wav"

            if 'fileUpload' + str(i) not in request.files:
                print("No File Uploaded")
                flash("No File Uploaded")
                #return redirect(request.url)

            file = request.files['fileUpload' + str(i)]
            if file.filename == '':
                flash("No  selected file")
                return redirect(request.url)
            if file and allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            tempPage['file'] = filename

        elif type == 'Video':
            filename = str(randint(0, 999999999999)) + ".mp4"

            if 'fileUpload' + str(i) not in request.files:
                print("No File Uploaded")
                flash("No File Uploaded")
                #return redirect(request.url)

            file = request.files['fileUpload' + str(i)]
            if file.filename == '':
                flash("No  selected file")
                return redirect(request.url)
            if file and allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            tempPage['file'] = filename

        elif type == 'Multiple Choice':
            tempPage['question'] = request.form['McQ' + str(i)]
            tempPage['answers'] = []
            for j in range(int(request.form['McNumAnswers' + str(i)])):
                tempPage['answers'].append(request.form['McA' + str(request.form['totalPages']) + str(j)])
                if 'McC' + str(request.form['totalPages']) + str(j) in request.form: #["McC" + str(i + 1) + str(j)]:
                    tempPage['correct'] = j

        elif type == 'Select Answers':
            tempPage['question'] = request.form['SelQ' + str(i)]
            tempPage['answers'] = []
            tempPage['correct'] = []
            for j in range(int(request.form['SelNumAnswers' + str(i)])):
                tempPage['answers'].append(request.form['SelC' + str(request.form['totalPages']) + str(j)])
                if "SelC" + str(request.form['totalPages']) + str(j) in request.form:
                    tempPage['correct'].append(j)

        elif type == 'Short Answer':
            tempPage['question'] = request.form['SaQ' + str(i)]
            tempPage['answers'] = request.form['SaKey' + str(i)].split(';')

        pages.append(tempPage)
    if 'user' in session:
        databaseUtils.add_class(request.form['title'], request.form['prerequisites'], request.form['description'], pages, session['user'])
    else:
        databaseUtils.add_class(request.form['title'], request.form['prerequisites'], request.form['description'],
                                pages, None)


    flash("Class Created!")
    return redirect(url_for('classes'))


@app.route("/report_button", methods=["POST"])
def report_button():
    flash("Thank you for the feedback!")
    databaseUtils.add_report(request.form['report'])
    return redirect('/report')


@app.route("/profile/<username>")
@require_login
def profile(username):
    return render_template("profile.html", user=databaseUtils.get_user_by_name(username))


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/logout')
@require_login
def logout():
    if 'user' in session:
        session.pop('user')
        session.pop('username')
        session.pop('admin')
    return redirect(url_for('login'))


@app.route("/addHouse", methods=["POST"])
@require_login
def addHouse():
    databaseUtils.add_to_watchlist(session['user'], databaseUtils.get_house_by_image(request.form['houseid']))
    flash("House added to watchlist")
    return redirect(url_for('housing'))


@app.route("/auth", methods=["POST"])
def auth():
    if "submit" not in request.form or "user" not in request.form or "pwd" not in request.form:
        flash("At least one form input was incorrect")
        return redirect(url_for('login'))

    if request.form['submit'] == 'Login':
        user = databaseUtils.authenticate(request.form['user'], request.form['pwd'])
        if user:
            session['user'] = str(user)
            session['username'] = databaseUtils.get_user_by_id(user)['username']
            session['admin'] = databaseUtils.is_admin(str(user))
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=30)
            return redirect(url_for('root'))
        else:
            flash('Incorrect username or password')
            return redirect(url_for('login'))
    else:
        success = databaseUtils.create_user(request.form['user'], request.form['pwd'])
        if (success):
            session['user'] = str(success)
            session['username'] = databaseUtils.get_user_by_id(success)['username']
            session['admin'] = databaseUtils.is_admin(str(success))
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=30)
            return redirect(url_for('root'))
        else:
            flash('This username already exists!')
            return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
