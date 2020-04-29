from flask import current_app
import pytest
    
def test_app_exist(test_app):
    assert current_app is not None

def test_app_is_testing(test_app):
    assert current_app.config['TESTING'] == True

def test_404_error(test_app):
    response = test_app.test_client().get('/foo')
    data = response.get_data(as_text=True)
    assert response.status_code == 404
    assert '404' in data

def test_home_page(test_app):
    response = test_app.test_client().get('/')
    data = response.get_data(as_text=True)
    assert response.status_code == 200
    assert 'First Heading' in data
