from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plants_dict_list = [p.to_dict() for p in plants]
        return make_response(jsonify(plants_dict_list), 200)
    
    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )
        db.session.add(new_plant)
        db.session.commit()
        
        return make_response(jsonify(new_plant.to_dict()), 201)

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return make_response(jsonify({'error': 'Not found'}), 404)
        return make_response(jsonify(plant.to_dict()), 200)

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
