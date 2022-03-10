from flask import Flask, jsonify, make_response, request
# from mock_data import recipes
import json
import os

app = Flask(__name__)

def get_recipe(recipe_name):
    for recipe in recipes["recipes"]:
        if recipe["name"] == recipe_name:
            return recipe #will end loop once recipe is found
    return 'None'

with open(os.path.join(os.path.dirname(__file__), "data.json")) as file:
    recipes = json.load(file)
    
@app.route("/recipes", methods=['GET'])
def get_all_recipes():
    return make_response(recipes, 200)

@app.route("/recipes/<recipe_name>", methods=['GET'])
def get_recipe_by_name(recipe_name):
    selected_recipe = get_recipe(recipe_name)
    if selected_recipe != 'None':
        return make_response(jsonify({'details': selected_recipe}), 200)
    else:
        return make_response(jsonify({'error': 'Recipe does not exist exists'}), 200)
    
@app.route("/recipes", methods=['POST'])
def add_recipe():
    new_recipe = json.loads(request.data)
    can_create = True
    
    for recipe in recipes["recipes"]:
        if recipe['name'] == new_recipe['name']:
            can_create = False
            break #ends loop if recipe is found
    
    if can_create == True:
        recipes["recipes"].append(new_recipe)
        return(recipes, 201)
    else:
        return(jsonify({'error': 'Recipe already exists'}), 400)

@app.route("/recipes/<recipe_name>", methods=['PUT'])
def update_recipe(recipe_name):
    selected_recipe = get_recipe(recipe_name)
    if selected_recipe != 'None':
        updated_recipe = json.loads(request.data)
        selected_recipe["name"] = updated_recipe["name"]
        selected_recipe["ingredients"] = updated_recipe["ingredients"]
        selected_recipe["instructions"] = updated_recipe["instructions"]
        return make_response(jsonify({'details': selected_recipe}), 204)
    else:
        return make_response(jsonify({'error': 'Recipe does not exist exists'}), 404)

@app.route("/recipes/<recipe_name>", methods=['DELETE'])
def delete_recipe(recipe_name):
    for recipe in recipes["recipes"]:
        if recipe['name'] == recipe_name:
            recipes["recipes"].remove(recipe)
            return make_response({}, 204) #ends loop if recipe is found
    return make_response(jsonify({'error': 'Recipe does not exist exists'}), 404)

if __name__ == '__main__':
    app.run(debug=True)

