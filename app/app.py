\from flask import Flask, render_template, request,redirect

from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb+srv://709:709@cluster0.nihef.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client["Anime"]
collection = db['list']


@app.route('/')
def index():
    # retrieve all data from MongoDB collection
    users = collection.find()
    return render_template('index.html', users=users)


@app.route('/create', methods=['POST'])
def create():
    # extract user data from POST request
    driveId = request.form['driveId']
    driveId = driveId[driveId.rindex("/")+1:] if "/" in driveId else driveId
    animeLink = request.form['animeLink']
    animeLink = animeLink[animeLink.rindex("/")+1:] if "/" in animeLink else animeLink
    totalEpisodes = int(request.form['totalEpisodes'])

    # create new user document in MongoDB collection
    user = {"id": driveId, 'link': animeLink, "total": totalEpisodes}
    collection.insert_one(user)

    return redirect('/')


@app.route('/update', methods=['POST'])
def update():
    # extract user data from POST request
    _id = request.form['_id']
    driveId = request.form['driveId']
    animeLink = request.form['animeLink']
    totalEpisodes = int(request.form['totalEpisodes'])

    # update user document in MongoDB collection
    collection.update_one({'id': _id}, {"$set": {"id": driveId, 'link': animeLink, "total": totalEpisodes}})

    return redirect('/')


@app.route('/delete', methods=['POST'])
def delete():
    # extract user data from POST request
    _id = request.form['_id']

    # delete user document from MongoDB collection
    collection.delete_one({'id': _id})

    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7090)
