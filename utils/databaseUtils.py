from _sha256 import sha256
from bson import ObjectId
#from google.cloud import storage
import pymongo as pymongo
import base64
import gridfs

client = pymongo.MongoClient("mongodb+srv://admin:pass@cluster0.unvko.gcp.mongodb.net/FreeBird?retryWrites=true&w=majority")
db = client.FreeBird
users = db.users
jobs = db.jobs
classes = db.classes
houses = db.houses
reports = db.reports
messages = db.messages
fs = gridfs.GridFS(db)

"""
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

    return "https://storage.cloud.google.com/freebird-images/" + destination_blob_name
"""

# creates a user in the database with a username, password, and post id
def create_user(username, password):
    if get_user_by_name(username) is None:
        user = users.insert_one({
            "username": username,
            "password": hash_password(username, password),
            "watchList": [],
            "certifications": [],
            "applicationIDs" : [],
            "admin" : False
            })

        return user.inserted_id
    return None


# gets the username of a user
def get_user_by_name(username):
    return users.find_one({"username": username})


def get_house_by_image(imagePath):
    return houses.find_one({"img": imagePath})


# gets the id of a user
def get_user_by_id(userid):
    return users.find_one({"_id": ObjectId(userid)})


def apply(userid, jobid):
    user = get_user_by_id(userid)

    print(user)

    if user['applicationIDs'] is None:
        user['applicationIDs'] = [jobid]
    else:
        user['applicationIDs'] += [jobid]

    new_value = {"$set": {"applicationIDs": user['applicationIDs']}}
    users.update_one(get_user_by_id(userid), new_value)

# returns a list of all the job listings
def get_jobs():
    return jobs.find({})


def get_job_by_id(jobid):
    return jobs.find_one({"_id": ObjectId(jobid)})


# adds a job to the database
def add_job(position, company, term, requirements, location, salary, description):
    job = jobs.insert_one\
        ({
            "position": position,
            "company": company,
            "term": term,
            "requirements": requirements,
            "location": location,
            "salary": salary,
            "description": description
        })
    return job.inserted_id


# returns a list of all the house listings
def get_houses():
    return houses.find({})


def get_house_by_id(houseid):
    return houses.find_one({"_id": ObjectId(houseid)})


def add_house(price, location, term, owner, img):
    house = houses.insert_one\
        ({
            "price": price,
            "location": location,
            "term": term,
            "owner": owner,
            "img": img
        })
    return house.inserted_id


def add_to_watchlist(userid, houseid):
    user = get_user_by_id(userid)

    if user['watchList'] is None:
        user['watchList'] = [houseid]
    else:
        user['watchList'].append(houseid)

    new_value = {"$set": {"watchList": user['watchList']}}
    users.update_one(get_user_by_id(userid), new_value)


def get_watchlist(userid):
    user = get_user_by_id(userid)
    watchlist = []
    for houseid in user['watchList']:
        watchlist.append(houseid)
    
    return watchlist


# returns a list of all the class listings
def get_classes():
    return classes.find({})


def get_class_by_id(classid):
    return classes.find_one({"_id": ObjectId(classid)})


def complete_class(userid, classid):
    user = get_user_by_id(userid)

    if user['certifications'] is None:
        user['certifications'] = [classid]
    else:
        user['certifications'].append(classid)

    new_value = {"$set": {"certifications": user['certifications']}}
    users.update_one(get_user_by_id(userid), new_value)


def get_certifications(userid):
    user = get_user_by_id(userid)
    certifications = []
    for classid in user['certifications']:
        certifications.append(classid)

    return certifications


# creates a class and adds it to the database
def add_class(title, prerequisites, description, pages, creator):
    new_class = {
        "creator": creator,
        "title": title,
        "prerequisites": prerequisites,
        "description": description,
        "content": []
    }

    for page in pages:
        new_class['content'].append(page)

    classes.insert_one(new_class)
    return classes.inserted_id


# constructs the value for a password key
def hash_password(username, password):
    return sha256(str(username+password).encode('utf-8')).hexdigest()


# provides the information needed for a user to sign in
def authenticate(username, password):
    user = get_user_by_name(username)
    if user is None:
        return
    if hash_password(username, password) != user["password"]:
        return
    return user["_id"]


# adds a new report to the database
def add_report(report):
    (print(report))
    reports.insert_one({"description": report})


# upgrades a normal user to an admin
def user_admin(userid):
    get_user_by_id(userid)["admin"] = True
    return None


def is_admin(userid):
    return get_user_by_id(userid)['admin']


# returns a picture (image file)
def get_picture(picture):
    return fs.get(picture).read()


def send_message(senderid, receiverid, subject, message):
    messages.insert_one({
        "sender": senderid,
        "receiver": receiverid,
        "subject": subject,
        "message": message
    })


def get_messages_by_user(userid):
    allMessages = messages.find({})
    userMessages = []
    for message in allMessages:
        if(message['receiver'] == userid):
            userMessages.append(message)

    return userMessages