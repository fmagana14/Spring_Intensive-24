from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['trip_database']
all_trips = db['trips']

@app.route('/')
def index():
    trips = all_trips.find()
    print(trips)
    return render_template('index.html', trips=trips)
# Routes
# @app.route('/<sort_order>')
# def index(sort_order):
#     # Check if sorting order is specified in the query parameters
    
#     trips = all_trips.find()
#     print(sort_order)
#     # Sort the trips based on the specified order
#     # trips.sort("arrival_date", 1)

#     if sort_order == 'oldest':
#         trips = all_trips.find().sort('arrival_date', 1)  # Sort oldest to newest
#     elif sort_order == 'newest':
#         trips = all_trips.find().sort('arrival_date', -1)  # Sort newest to oldest
#     else:
#         # Default sorting order (no sorting)
#         trips = all_trips.find()
#     print(trips[0]["arrival_date"], trips[1]["arrival_date"], trips[2]["arrival_date"])
#     return render_template('index.html', trips=trips)

@app.route('/add_trip', methods=['POST'])
def add_trip():
    # Retrieve trip data from the form
    location = request.form['location']
    arrival_date = request.form['arrival_date']
    departure_date = request.form['departure_date']
    adults = int(request.form['adults'])
    children = int(request.form['children'])
    rating = int(request.form['rating'])

    # Create a dictionary to store trip data
    trip_data = {
        'location': location,
        'arrival_date': arrival_date,
        'departure_date': departure_date,
        'adults': adults,
        'children': children,
        'rating': rating,
    }

    # Insert the trip data into the MongoDB collection
    all_trips.insert_one(trip_data)

    # Redirect to the index route after adding the trip
    return redirect(url_for('index'))

@app.route('/delete_trip/<trip_id>', methods=['POST', 'DELETE'])
def delete_trip(trip_id):
    # Check if the request method is either POST or DELETE
    if request.method in ['POST', 'DELETE']:
        # Delete the trip from the MongoDB collection using its ObjectId
        all_trips.delete_one({'_id': ObjectId(trip_id)})
        # all_trips.find
        print(trip_id)
    # Redirect to the index route after deleting the trip
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Run the Flask application
    app.run(host="0.0.0.0", port=8000, debug=True)
