from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

import os

app = Flask(__name__)

if os.path.exists("env.py"):
    import env

# grab the enviornment variables
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
mongo = PyMongo(app)

if os.environ.get("DEBUG") == 'True':
    app.debug = True
else:
    app.debug = False

# blog data references the collection within mongo db atlas that holds the blog data
kitchen_collection = mongo.db.kitchen
volunteer_collection = mongo.db.volunteer

@app.route("/")
def index():
    return render_template("index.html", kitchens = kitchen_collection.find())

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/find_nearest")
def find_nearest():
    return render_template("find_nearest.html")

@app.route("/edit")
def edit():
    kitchenId=request.args.get("kitchenId", None)
    return render_template("edit.html", kitchen=kitchen_collection.find_one({ '_id': ObjectId(kitchenId)}))

@app.route("/delete")
def delete():
    kitchenId=request.args.get("kitchenId", None)
    kitchen_collection.remove({ "_id": ObjectId(kitchenId) })
    return redirect(url_for("index"))

@app.route("/delete_volunteer")
def delete_volunteer():
    volunteerId=request.args.get("volunteerId", None)
    volunteer_collection.remove({ "_id": ObjectId(volunteerId) })
    return redirect(url_for("index"))

@app.route("/all_volunteers")
def all_volunteers():
    return render_template("all_volunteers.html", volunteers = volunteer_collection.find())

@app.route("/create_kitchen", methods=["POST"])
def create_kitchen():
    kitchens=kitchen_collection
    kitchens.insert_one(request.form.to_dict())
    return redirect(url_for('index'))

@app.route("/volunteer_form")
def volunteer_form():
    return render_template("volunteer_form.html")

@app.route("/add_volunteer", methods=["POST"])
def add_volunteer():
    volunteers=volunteer_collection
    volunteers.insert_one(request.form.to_dict())
    return redirect(url_for('index'))

@app.route('/edit_kitchen', methods=["POST"])
def edit_kitchen():
    kitchenId=request.args.get('kitchenId', None)
    kitchens = kitchen_collection
    kitchens.update( {'_id': ObjectId(kitchenId)},
    {
        'title':request.form.get('title'),
        'text':request.form.get('text'),
    })
    return redirect(url_for('index'))

# a page for viewing a single blog on its own
@app.route("/dedicated")
def dedicated():
    kitchenId = request.args.get('kitchenId', None)
    return render_template("dedicated.html", kitchen=kitchen_collection.find_one({ '_id': ObjectId(kitchenId)}), volunteers = volunteer_collection.find())

if __name__ == '__main__':
    if app.debug:
        app.run(debug=True)
    else:
        app.run(debug=False)