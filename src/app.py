"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#trae a la familia
@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#trae un familiar
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member is None:
            return jsonify ({"msg": "Member not found"}), 404
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#crea un familiar
@app.route('/members', methods=['POST'])
def add_member():
    try:
        body = request.get_json() 
        if not body:
            return jsonify ({"no se encontro familiar"}), 400
        required = ["first_name", "age", "lucky_numbers"]
        for r in required:
            if r not in body:
                return jsonify({"error": f"Missing field: {r}"}), 400
        new_member = jackson_family.add_member(body)
        return jsonify(new_member), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#elimina un familiar
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        deleted = jackson_family.delete_member(member_id)
        if not deleted:
            return jsonify ({"msg": "Member not found"}), 404
        return jsonify({"done" : True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
