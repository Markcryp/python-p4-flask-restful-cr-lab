#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Initialize the API
api = Api(app)

# Plants Resource
class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        try:
            data = request.get_json()

            # Ensure required fields are present
            if 'name' not in data or 'image' not in data or 'price' not in data:
                return make_response(jsonify({"error": "Missing required fields"}), 400)

            new_plant = Plant(
                name=data['name'],
                image=data['image'],
                price=data['price'],
            )

            db.session.add(new_plant)
            db.session.commit()

            return make_response(new_plant.to_dict(), 201)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()

        # Check if plant exists
        if plant:
            return make_response(jsonify(plant.to_dict()), 200)
        else:
            return make_response(jsonify({"error": "Plant not found"}), 404)


# Add the resources to the API
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

# Run the app
if __name__ == '__main__':
    app.run(port=5555, debug=True)
