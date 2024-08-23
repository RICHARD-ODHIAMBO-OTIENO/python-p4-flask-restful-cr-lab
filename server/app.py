#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Resource for handling multiple plants
class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return [plant.to_dict() for plant in plants], 200

    def post(self):
        data = request.get_json()
        try:
            new_plant = Plant(
                name=data['name'],
                image=data['image'],
                price=data['price']
            )
            db.session.add(new_plant)
            db.session.commit()
            return new_plant.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 400

# Resource for handling a single plant by ID
class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get(plant_id)
        if plant:
            return plant.to_dict(), 200
        return {"error": "Plant not found"}, 404

    def patch(self, plant_id):
        plant = Plant.query.get(plant_id)
        if plant:
            data = request.get_json()
            if 'name' in data:
                plant.name = data['name']
            if 'image' in data:
                plant.image = data['image']
            if 'price' in data:
                plant.price = data['price']
            db.session.commit()
            return plant.to_dict(), 200
        return {"error": "Plant not found"}, 404

    def delete(self, plant_id):
        plant = Plant.query.get(plant_id)
        if plant:
            db.session.delete(plant)
            db.session.commit()
            return {"message": "Plant deleted successfully"}, 200
        return {"error": "Plant not found"}, 404

# Add the routes for the API
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
