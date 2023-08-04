# Atass service for managing routes

## Public Endpoints
### Get aviable routes

- URL: `/available?move_from_city={cityname}&move_to_city={cityname}&date={dd.mm.yyyy}`
- Method: `GET`
- Description: Select available routes for date and place
- Response example:
```json
[
  {
    "move_from": {
      "place": {
        "country": "A",
        "city": "A",
        "street": "A",
        "map_url": "http//:...",
        "id": "..."
      },
      "date": "yyyy-mm-ddThh:mm:ss.ms",
      "is_active": true,
      "id": "..."
    },
    "move_to": {
      "place": {
        "country": "B",
        "city": "B",
        "street": "B",
        "map_url": "http//:...",
        "id": "..."
      },
      "date": "yyyy-mm-ddThh:mm:ss.ms",
      "is_active": true,
      "id": "..."
    },
    "price": 600,
    "root_route_id": "..."
  }
]
```

### Get route full info
- URL: `/get_path_info?route_id={routeid}&move_from={fromId}&move_to={toId}`
- Method: `GET`
- Description: Return route info by id
- Response example:
```json
{
    "move_from": {
      "place": {
        "country": "A",
        "city": "A",
        "street": "A",
        "map_url": "http//:...",
        "id": "..."
      },
      "date": "yyyy-mm-ddThh:mm:ss.ms",
      "is_active": true,
      "id": "..."
    },
    "move_to": {
      "place": {
        "country": "B",
        "city": "B",
        "street": "B",
        "map_url": "http//:...",
        "id": "..."
      },
      "date": "yyyy-mm-ddThh:mm:ss.ms",
      "is_active": true,
      "id": "..."
    },
    "price": 600,
    "root_route_id": "...",
    "description": {
        "ua": "Привіт",
        "en": "Hello",
        "pl": "Witam"
    },
    "rules": {
        "ua": "Не курити",
        "en": "Do not smoking",
        "pl": "nie palić"
    },
    "transportation_rules": {
        "ua": "Використовуйте контейнери",
        "en": "Use containers",
        "pl": "Użyj pojemników"
    }
}
```

### Get availability graph

- URL: `/availability_graph`
- Method: `GET`
- Description: Return graph of aviable pathes
- Response example:
```json
{
  "Київ": [
    "Львів",
    "Варшава"
  ],
    "Львів": [
    "Варшава"
  ]
}
```