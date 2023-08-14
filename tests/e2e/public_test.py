import requests

BASE_URL = "http://localhost:8000"

def test_get_available_routes():
    url = f"{BASE_URL}/available?move_from_city=Київ&move_to_city=Варшава&date=*"
    response = requests.get(url)
    
    assert response.status_code == 200
    
    data = response.json()

    assert data[0]['move_from']['place']['city'] == "Київ"
    assert data[0]['move_to']['place']['city'] == "Варшава"

    assert data[0]['price'] == 1000
    assert data[0]['root_route_id'] == "7c47bcb9-8179-49b5-93fd-089fafa793d3"

def test_get_availability_graph():
    url = f"{BASE_URL}/availability_graph"
    response = requests.get(url)
    
    assert response.status_code == 200
    
    data = response.json()

    assert data == {"Київ": ["Львів", "Варшава"], "Львів": ["Варшава"]}

def test_get_path_info():
    routeid = "7c47bcb9-8179-49b5-93fd-089fafa793d3"
    from_id = "c279d1f3-ddb9-4091-8408-d88bdcc0a040"
    to_id = "dbca1b8a-0c26-48db-8497-ad103e0fd78c"

    url = f"{BASE_URL}/get_path_info?route_id={routeid}&move_from={from_id}&move_to={to_id}"
    response = requests.get(url)
    
    assert response.status_code == 200

    data = response.json()

    assert data['move_from']['place']['city'] == "Київ"
    assert data['move_to']['place']['city'] == "Львів"

    assert data['root_route_id'] == routeid
