import requests

BASE_URL = "http://localhost:8000"

def test_get_unique_routes():
    url = f"{BASE_URL}/get_unique_routes"
    response = requests.get(url)
    
    assert response.status_code == 200
    
    data = response.json()[0]

    assert data['count'] == 1
    assert data['move_from']['city'] == 'Київ'
    assert data['move_to']['city'] == 'Варшава'

def test_get_routes_family():
    url = f"{BASE_URL}/get_routes_family?move_from_city=Київ&move_to_city=Варшава"
    response = requests.get(url)
    
    assert response.status_code == 200

    data = response.json()[0]

    assert data['passengers_number'] == 5
    assert data['move_from']['place']['city'] == 'Київ'
    assert data['move_to']['place']['city'] == 'Варшава'
    assert data['sub_spots'][0]['place']['city'] == 'Львів'

    assert data['prices'][data['move_from']['id']][data['move_to']['id']] == 1000

def test_get_route_by_id():
    url = f"{BASE_URL}/get_route_by_id?route_id=7c47bcb9-8179-49b5-93fd-089fafa793d3"
    response = requests.get(url)
    
    assert response.status_code == 200

    data = response.json()

    assert data['passengers_number'] == 5
    assert data['move_from']['place']['city'] == 'Київ'
    assert data['move_to']['place']['city'] == 'Варшава'
    assert data['sub_spots'][0]['place']['city'] == 'Львів'

    assert data['prices'][data['move_from']['id']][data['move_to']['id']] == 1000
