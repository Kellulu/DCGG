import os
from os import abort
import shutil
from tokenize import String
from wsgiref.util import request_uri
from flask import Flask, redirect, url_for, render_template, session, request, flash, send_file
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import timedelta
import datetime

import image_rename
#import jyserver.Flask as jsf
UPLOAD_FOLDER = os.getcwd() + '/static/images/upload'


app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'zip'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usrac.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=60)

app.secret_key = "HOHOHOHOHOHO!!!"

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id",db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    passcode = db.Column(db.String(100))
    dataset_name = 'na'     #[0] renamed filename; [1] original filename
    dataset = 'empty'
    dataset_bot_type = 'JetBot'
    dataset_length = ''
    dataset_date_time = ''
    index = 0
    current_path = ''
    dataset_fullpath = ''
    dataset_output_zip = ''


    def __init__(self, name, passcode, dataset_name, dataset, dataset_bot_type, dataset_length, dataset_date_time , index, current_path, dataset_fullpath, dataset_output_zip):
        self.name = name
        self.passcode = passcode
        self.dataset_name = dataset_name
        self.dataset = dataset
        self.dataset_bot_type = dataset_bot_type
        self.dataset_length = dataset_length
        self.dataset_date_time = dataset_date_time
        self.index = index
        self.current_path = current_path
        self.dataset_fullpath = dataset_fullpath
        self.dataset_output_zip = dataset_output_zip


'''
@jsf.use(app)
class App:
    def __init__(self):
        pass

    def image_update(self):
        self.js.document.getElementById('peter').innerHTML = 'puuuu'
'''

html_index = "index.html"
html_login = "login.html"
html_DCGG = "operation.html"
html_admin = "admin.html"
html_upload = "upload.html"

message_login = "Welcome back"
message_login_alredy = "Hey there."
message_logout = "Logged out, BYE BYE~"
message_not_loggeg_in = "DUDEEE, you're not logged in"

@app.route("/")
def home():
    return render_template(html_index)

@app.route("/admin")
def admin():
    return render_template(html_admin, values=users.query.all())
    


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["usr_id"]
        passcode = request.form["usr_pw"]
        if user == "" and passcode == "":
            flash('Incorrect User ID / Password!')
            return render_template("login.html")
        else:
            found_user = users.query.filter_by(name=user).first()
            if found_user == None:
                flash('Incorrect User ID / Password!')
                return render_template("login.html")
            else:
                if found_user.passcode  == passcode:
                    session["user"] = user
                    return redirect(url_for("dcgg"))
                else:
                    flash('Incorrect User ID / Password!')
                    return render_template("login.html")
    else:
        if "user" in session:
            return redirect(url_for("dcgg"))

        return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        user = request.form["usr_id"]
        passcode = request.form["usr_pw"]

        user_name_check = users.query.filter_by(name=user).first()
        
        if user_name_check != None:
            flash("User name has been registerEDDDDDD. PleasE Lah.")
            return render_template("register.html")
        else:
            usr = users(user, passcode, 'na', 'empty', '', '', '', 0, '','','')
            db.session.add(usr, passcode)
            db.session.commit()
            return redirect(url_for("login"))
    return render_template("register.html")

###################

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

###################

#@app.route("/upload", methods=["POST", "GET"])
def upload_zip():
    print('allowed file check')
    if request.method == "POST":
        if request.files:
            zip_file = request.files["zippy"]
            print(zip_file)

            if zip_file.filename == "":
                flash('No File')
                return redirect(request.url)
            if allowed_file(zip_file.filename):
                filename = str(session["user"])+"_"+ datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+"_"+ secure_filename(zip_file.filename)
                USR_FOLDER = UPLOAD_FOLDER + "/" + str(session["user"])
                app.config['USR_FOLDER'] = USR_FOLDER
                
                if os.path.exists(USR_FOLDER) != True:
                    os.makedirs(USR_FOLDER)
                else:                               # remove all old files in the user file
                    for file_object in os.listdir(USR_FOLDER):
                        file_object_path = os.path.join(USR_FOLDER, file_object)
                        if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
                            os.unlink(file_object_path)
                        else:
                            shutil.rmtree(file_object_path)
                    
                zip_file.save(os.path.join(app.config['USR_FOLDER'], filename))
                print('-- Update: Zip file is saved.\t Filename: ', filename)

                ## unzip files and add data into user account
                temp = image_rename.unzip(USR_FOLDER, filename)
                users.dataset_name = temp[0]
                users.dataset = temp[1]
                users.index = 0
                users.dataset_date_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                return redirect(url_for("dcgg"))
            else:
                print("Please upload a 'zip' file.")
                return redirect(request.url)

    #return render_template(dcgg)

def dataset2html(dataset_name, dataset,index, bot_type, dataset_date_time):
    if type(dataset) == list:
        html_output = "<p class='main_browser_p'>Source File Name:</p>"
        html_output = html_output + "<li class='main_browser_li'>"+ dataset_name[1] +"</li>"
        html_output = html_output + "<p class='main_browser_p'>Upload Date/Time:</p>"
        html_output = html_output + "<li class='main_browser_li'>"+ dataset_date_time+"</li>"
        html_output = html_output + "<p class='main_browser_p'>Robot Type:</p>"
        html_output = html_output + "<li class='main_browser_li'>"+ bot_type+"</li>"
        html_output = html_output + "<p class='main_browser_p'>Image Count:</p>"
        html_output = html_output + "<li class='main_browser_li'>"+ str(len(dataset))+" images</li>"
        html_output = html_output + "<p class='main_browser_p'>Current Image:</p>"
        html_output = html_output + "<li class='main_browser_li'>"+ str(index + 1) +"</li>"
    else:
        html_output = dataset
    return html_output

def dataset2path(user, dataset_name, dataset, bot_type):
    if bot_type == "JetRacer":
        users.dataset_fullpath = UPLOAD_FOLDER + "/" + user + "/" + dataset_name[0][:-4] + "/apex/"
        image_path_prefix = 'images/upload/' + user + "/" + dataset_name[0][:-4] + "/dataset/"
    else:
        users.dataset_fullpath = UPLOAD_FOLDER + "/" + user + "/" + dataset_name[0][:-4] + "/"
        image_path_prefix = 'images/upload/' + user + "/" + dataset_name[0][:-4] + "/"
    image_path = []

    for i in dataset:
        append_obj = image_path_prefix + i
        image_path.append(append_obj)
    
    users.current_path = image_path_prefix

    return image_path

def load_dataset(user):
    print(type(users.dataset))
    if type(users.dataset) == list:
        image_path = dataset2path(user, users.dataset_name, users.dataset, users.dataset_bot_type)
        image_path = url_for('static' ,filename = image_path[users.index])
        users.dataset_length = len(users.dataset)
        print("=================load_dataset================")
        print("User: ", user, "\tIndex: ", users.index + 1 , "/" , users.dataset_length)
        print("=============================================")
        img_name = users.dataset[users.index].split("/")
        img_name = img_name[len(img_name)-1]
    else:
        image_path = ""
        image_path = url_for('static' ,filename = image_path)
        img_name = "NULL NULL chuuuuuu~"
    
    return image_path, img_name

@app.route("/dcgg", methods=["POST", "GET"])
def dcgg():
    if "user" in session:
        user = session["user"]
        output_msg = message_login +", "+ user
        flash(output_msg)

        upload_zip()

        ##### Button action
        if "prev" in request.form and request.method == "POST":
            if users.index != 0:
                users.index = users.index -1
            else:
                users.index = 0
        elif "next" in request.form:
            if users.index != len(users.dataset) -1:
                users.index = users.index +1
            else:
                users.index = len(users.dataset) -1
        elif "zip" in request.form:
            output_filename = "new_" + datetime.datetime.now().strftime("%Y%m%d") + "_dataset"
            output_filename = UPLOAD_FOLDER + "/" + user + "/" + output_filename
            
            users.dataset_output_zip = shutil.make_archive(output_filename, 'zip', users.dataset_fullpath)
            print("=====================")
            print("Zipped")
            print("Zip Filename: ", output_filename)
            print(users.dataset_output_zip)
            print("=====================")
            return send_file(users.dataset_output_zip, as_attachment=True)
        #####

        #### Save action
        if "save" in request.form and request.method == "POST":
            x_cor = request.form["x_cor"]
            y_cor = request.form["y_cor"]
            users.dataset_bot_type = request.form["bot_type"]
            print(x_cor,y_cor, users.dataset_bot_type)

            users.dataset[users.index] = image_rename.rename(x_cor, y_cor, users.dataset_bot_type, users.dataset[users.index], users.current_path)

        image_details = load_dataset(user)
        
        return render_template(html_DCGG, user=user, img_path = image_details[0] , \
            dataset = dataset2html(users.dataset_name,users.dataset, users.index, \
            users.dataset_bot_type, users.dataset_date_time), img_name = image_details[1], \
            bot_type = users.dataset_bot_type, img_count = users.dataset_length, img_index = users.index )
    else:
        flash(message_not_loggeg_in, "warning")
        return redirect(url_for("login"))

###################


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash(message_logout, "info")
    return redirect(url_for("login"))

'''
@app.route("/admin")
def admin():
    return redirect(url_for("user", name="Admin!"))
'''

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

'''
    ## command to delete user
    #found_user = users.query.filter_by(name=user).delete()
    for user in found_user:
        user.delete()
'''
