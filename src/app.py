"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)



jackson_family = FamilyStructure("Jackson")

member1={
    "first_name": "john",
    "id": jackson_family._generateId(),
    "age":33,
    "lucky_numbers":[7, 13, 22]
    }

member2={
    "first_name": "Jane",
    "id": jackson_family._generateId(),
    "age":35,
    "lucky_numbers":[10, 14, 3]
    }

member3={
    "first_name": "Jimmy",
    "id": jackson_family._generateId(),
    "age":5,
    "lucky_numbers":[1]
    }

jackson_family.add_member(member1)
jackson_family.add_member(member2)
jackson_family.add_member(member3)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    
    if members is None:
        return jsonify({"msg" : "solicitud fallida"}),400
    

    return jsonify(members), 200



@app.route("/member/<int:id>", methods=['GET'])
def get_one_member(id):

   
   
    member = jackson_family.get_member(id)

    if member is not None:
        return jsonify(member),200
    
    return jsonify({"msg" : "solicitud fallida"}),400
    

@app.route("/member", methods=['POST'])
def add_one_member():

    member = request.get_json()
    jackson_family.add_member(member)
    return jsonify(member),200

    if members is None:
        return jsonify({"msg" : "solicitud fallida"}),400

@app.route("/member/<int:id>", methods=['DELETE'])
def _one_member(id):

    member = jackson_family.delete_member(id)
    
    return jsonify(member),200

    if members is None:
        return jsonify({"msg" : "solicitud fallida"}),400





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
