from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)



client = MongoClient('mongodb://localhost:27017/')
db = client['trip_database']
all_trips = db['trips']

# Routes
@app.route('/')
def index():
    trips = all_trips.find()
    print(trips)
    return render_template('index.html', trips=trips)

@app.route('/add_trip', methods=['POST'])
def add_trip():
    location = request.form['location']
    arrival_date = request.form['arrival_date']
    departure_date = request.form['departure_date']
    adults = int(request.form['adults'])
    children = int(request.form['children'])
    rating = int(request.form['rating'])


    trip_data = {
        'location': location,
        'arrival_date': arrival_date,
        'departure_date': departure_date,
        'adults': adults,
        'children': children,
        'rating': rating,
    }
    all_trips.insert_one(trip_data)

    return redirect(url_for('index'))

@app.route('/delete_trip/<trip_id>', methods=['POST', 'DELETE'])
def delete_trip(trip_id):
    if request.method == 'POST' or request.method == 'DELETE':
        all_trips.delete_one({'_id': ObjectId(trip_id)})
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)