from flask import Flask, jsonify, make_response, request
from mock_data import recipes

app = Flask(__name__)

def get_recipe(recipe_name):
    for recipe in recipes:
        if recipe["name"] == recipe_name:
            return recipe #will end loop once recipe is found
    return 'None'

@app.route("/recipes", methods=['GET'])
def get_all_recipes():
    return make_response(jsonify({'recipes': recipes}), 200)

@app.route("/recipes/<recipe_name>", methods=['GET'])
def get_recipe_by_name(recipe_name):
    selected_recipe = get_recipe(recipe_name)
    if selected_recipe != 'None':
        return make_response(jsonify({'details': selected_recipe}), 200)
    else:
        return make_response(jsonify({'error': 'Recipe does not exist exists'}), 200)
    
@app.route("/recipes", methods=['POST'])
def add_recipe():
    new_recipe = request.get_json()
    can_create = True
    
    for recipe in recipes:
        if recipe['name'] == new_recipe['name']:
            can_create = False
            break #ends loop if recipe is found
    
    if can_create == True:
        recipes.append(new_recipe)
        return(jsonify({'recipes': recipes}), 201)
    else:
        return(jsonify({'error': 'Recipe already exists'}), 400)

@app.route("/recipes/<recipe_name>", methods=['PUT'])
def update_recipe(recipe_name):
    selected_recipe = get_recipe(recipe_name)
    if selected_recipe != 'None':
        updated_recipe = request.get_json()
        selected_recipe["name"] = updated_recipe["name"]
        selected_recipe["ingredients"] = updated_recipe["ingredients"]
        selected_recipe["instructions"] = updated_recipe["instructions"]
        return make_response(jsonify({'details': selected_recipe}), 204)
    else:
        return make_response(jsonify({'error': 'Recipe does not exist exists'}), 404)

@app.route("/recipes/<recipe_name>", methods=['DELETE'])
def delete_recipe(recipe_name):
    for recipe in recipes:
        if recipe['name'] == recipe_name:
            recipes.remove(recipe)
            return make_response({}, 204)
            break #ends loop if recipe is found
    return make_response(jsonify({'error': 'Recipe does not exist exists'}), 404)

if __name__ == '__main__':
    app.run(debug=True)

