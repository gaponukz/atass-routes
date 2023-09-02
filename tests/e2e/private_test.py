import uuid
import requests

BASE_URL = "http://localhost:8000/api/routes"

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

def test_add_delete_routes():
    url = f"{BASE_URL}/add_routes"
    move_from_id = str(uuid.uuid4())
    move_to_id = str(uuid.uuid4())
    first_spot_id = str(uuid.uuid4())

    response = requests.post(url, json={
            "route_prototype": {
            "move_from": {
                    "place": {
                    "country": "StartCountry",
                    "city": "StartCity",
                    "street": "StartStreet"
                },
                "id": move_from_id
            },
            "move_to": {
                "place": {
                    "country": "DestinationCountry",
                    "city": "DestinationCity",
                    "street": "DestinationStreet"
                },
                "from_start": 5,
                "id": move_to_id
            },
            "sub_spots": [
                {
                "place": {
                    "country": "SubSpotCountry1",
                    "city": "SubSpotCity1",
                    "street": "SubSpotStreet1"
                },
                "from_start": 2,
                "id": first_spot_id
                },
            ],
            "passengers_number": 3,
            "description": {
                "ua": "Опис на українській",
                "en": "Description in English",
                "pl": "Opis po polsku"
            },
            "rules": {
                "ua": "Правила на українській",
                "en": "Rules in English",
                "pl": "Zasady po polsku"
            },
            "transportation_rules": {
                "ua": "Правила транспорту на українській",
                "en": "Transportation rules in English",
                "pl": "Zasady transportu po polsku"
            },
            "is_active": True,
            "prices": {
                move_from_id: {
                    first_spot_id: 500,
                    move_to_id: 1000
                },
                first_spot_id: {
                    move_to_id: 500
                }
            }
            },
            "departure_dates": [
                ["2024-08-14T12:00:00", "2024-08-15T12:00:00"],
                ["2024-08-15T13:30:00", "2024-08-16T13:30:00"]
            ]
        }
    )
    
    assert response.status_code == 200

    url = f"{BASE_URL}/get_routes_family?move_from_city=StartCity&move_to_city=DestinationCity"
    response = requests.get(url)
    data = response.json()

    assert len(data) == 2

    route = data[0]

    assert route['passengers_number'] == 3
    assert route['prices'][route['move_from']['id']][route['move_to']['id']] == 1000
    assert route['prices'][route['move_from']['id']][route['sub_spots'][0]['id']] == 500
    assert route['prices'][route['sub_spots'][0]['id']][route['move_to']['id']] == 500

    url = f"{BASE_URL}/route?route_id={route['id']}"
    response = requests.delete(url)

    assert response.status_code == 200

    url = f"{BASE_URL}/get_route_by_id?route_id={route['id']}"
    response = requests.get(url)
    
    assert response.status_code == 404

def test_update_route():
    url = f"{BASE_URL}/get_route_by_id?route_id=7c47bcb9-8179-49b5-93fd-089fafa793d3"
    response = requests.get(url)
    
    data = response.json()
    data['passengers_number'] = 20

    url = f"{BASE_URL}/route?route_id=7c47bcb9-8179-49b5-93fd-089fafa793d3"
    response = requests.put(url, json={'route': data})
    assert response.status_code == 200

    url = f"{BASE_URL}/get_route_by_id?route_id=7c47bcb9-8179-49b5-93fd-089fafa793d3"
    response = requests.get(url)
    
    assert response.status_code == 200

    data = response.json()

    assert data['passengers_number'] == 20
    
    data['passengers_number'] = 5
    url = f"{BASE_URL}/route?route_id=7c47bcb9-8179-49b5-93fd-089fafa793d3"
    response = requests.put(url, json={'route': data})
    assert response.status_code == 200

def test_change_places():
    response = requests.post(f"{BASE_URL}/add_passenger", json={
        "paymentId": "124",
        "routeId": "7c47bcb9-8179-49b5-93fd-089fafa793d3",
        "passenger": {
            "fullName": "Adam Qw",
            "phoneNumber": "832456932",
            "movingFromId": "c279d1f3-ddb9-4091-8408-d88bdcc0a040",
            "movingTowardsId": "dbca1b8a-0c26-48db-8497-ad103e0fd78c",
            "gmail": "test@gmail.com",
            "id": "123214oif21",
            "isAnonymous": True
        }
    })
    
    assert response.status_code == 200

    url = f"{BASE_URL}/get_route_by_id?route_id=7c47bcb9-8179-49b5-93fd-089fafa793d3"
    response = requests.get(url)

    data = response.json()

    assert data['passengers'][0]['id'] == "123214oif21"

    response = requests.delete(f"{BASE_URL}/passenger", json={
        "routeId": "7c47bcb9-8179-49b5-93fd-089fafa793d3",
        "moveFromId": "c279d1f3-ddb9-4091-8408-d88bdcc0a040",
        "moveToId": "dbca1b8a-0c26-48db-8497-ad103e0fd78c",
        "passengerId": "123214oif21",
    })
    
    assert response.status_code == 200

    url = f"{BASE_URL}/get_route_by_id?route_id=7c47bcb9-8179-49b5-93fd-089fafa793d3"
    response = requests.get(url)

    data = response.json()

    assert data['passengers'] == []
