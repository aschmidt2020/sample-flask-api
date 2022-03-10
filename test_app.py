import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

#checks that you are getting right kinds of http response code and MIME type back from JSON API server
def test_json_with_proper_mimetype(client):
    response = client.get('/recipes')
    assert response.status_code == 200
    assert response.content_type == 'application/json'

#tests get all endpoint PRIOR to any changes being made
def test_recipes(client):
    response = client.get('/recipes')
    json = response.get_json()
    assert len(json['recipes']) == 4

#tests get single recipe by name endpoint
def test_single_recipe(client):
    response = client.get('/recipes/garlicPasta')
    json = response.get_json()
    assert json['details']['name'] == 'garlicPasta'

def test_not_real_single_recipe(client):
    response = client.get('/recipes/notRealDish')
    json = response.get_json()
    assert json['error'] == 'Recipe does not exist'
#def test 404 error
def test_not_found(client):
    response = client.get('/notRealUrl')
    json = response.get_json()
    assert response.status_code == 404
    assert json['error'] == '404 Not Found'