from operator import index
from flask import Flask, jsonify, make_response, request
import json

app = Flask(__name__)
 
def get_recipe(recipe_name):
    json_file = open('data.json', 'r')
    recipes = json.load(json_file)

    for i in range(len(recipes["recipes"])):
        if recipes["recipes"][i]["name"] == recipe_name :
            return {'recipe': recipes["recipes"][i], 'index': i } #will end loop once recipe is found
    
    json_file.close()
    return 'None'
    
@app.route("/recipes", methods=['GET'])
def get_all_recipes():
    json_file = open('data.json', 'r')
    recipes = json.load(json_file)
    json_file.close()
    return make_response(recipes, 200)

@app.route("/recipes/<recipe_name>", methods=['GET'])
def get_recipe_by_name(recipe_name):
    selected_recipe = get_recipe(recipe_name)
    if selected_recipe != 'None':
        return make_response(jsonify({'details': selected_recipe['recipe']}), 200)
    else:
        return make_response(jsonify({'error': 'Recipe does not exist'}), 200)
    
@app.route("/recipes", methods=['POST'])
def add_recipe():
    new_recipe = json.loads(request.data)
    can_create = True
    
    json_file = open('data.json', 'r')
    recipes = json.load(json_file)
    
    for recipe in recipes["recipes"]:
        if recipe['name'] == new_recipe['name']:
            can_create = False
            break #ends loop if recipe is found
    
    if can_create == True:
        json_file = open('data.json', 'w')
        recipes["recipes"].append(new_recipe)
        json_file.write(json.dumps(recipes, indent=4)) #indent for formatting
        json_file.close()
        return(recipes, 201)
    else:
        return(jsonify({'error': 'Recipe already exists'}), 400)

@app.route("/recipes/<recipe_name>", methods=['PUT'])
def update_recipe(recipe_name):
    selected_recipe = get_recipe(recipe_name)
    json_file = open('data.json', 'r')
    recipes = json.load(json_file)

    if selected_recipe != 'None':
        updated_recipe = json.loads(request.data)
        json_file = open('data.json', 'w')
        recipes["recipes"][selected_recipe["index"]] = updated_recipe
        json_file.write(json.dumps(recipes, indent=4))
        json_file.close()
        return make_response(jsonify({'details': updated_recipe}), 204)
    else:
        return make_response(jsonify({'error': 'Recipe does not exist'}), 404)

@app.route("/recipes/<recipe_name>", methods=['DELETE'])
def delete_recipe(recipe_name):
    selected_recipe = get_recipe(recipe_name)
    json_file = open('data.json', 'r')
    recipes = json.load(json_file)
    
    if selected_recipe != 'None':
        json_file = open('data.json', 'w')
        recipes["recipes"].pop(selected_recipe['index'])
        json_file.write(json.dumps(recipes, indent=4))
        json_file.close()
        return make_response({}, 204) #ends loop if recipe is found
    else:
        return make_response(jsonify({'error': 'Recipe does not exist'}), 404)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'404 Not Found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)

