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
    "date": "",
    "price": 600,
    "root_route_id": "..."
  }
]
```

### Get route full info

- URL: `/get_route_info?route_id={routeid}`
- Method: `GET`
- Description: Return route info by id
- Response example:
```json
{
    "passengers_number": 5,
    "is_active": true,
    "prices": {
        "93b7f7ea-60f2-4524-82b9-a532721f2596": {
            "0f1363c7-9e74-45d7-8de3-29bbf3e07bc7": 5,
            "82ebef20-cde6-4b87-be3d-3030b8fe481d": 10
        },
        "0f1363c7-9e74-45d7-8de3-29bbf3e07bc7": {
            "82ebef20-cde6-4b87-be3d-3030b8fe481d": 5
        }
    },
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
    },
    "id": "7c47bcb9-8179-49b5-93fc-089fafa793d3",
    "move_from": {
        "place": {
            "country": "Ac",
            "city": "Ac",
            "street": "As",
            "map_url": null,
            "id": "6d9a98b0-c496-431b-942a-6c7f5c9bf211"
        },
        "date": "yyyy-mm-ddThh:mm:ss.ms",
        "is_active": true,
        "id": "93b7f7ea-60f2-4524-82b9-a532721f2596"
    },
    "move_to": {
        "place": {
            "country": "Bc",
            "city": "Bc",
            "street": "Bs",
            "map_url": null,
            "id": "b40b2e0d-b8da-4ae2-b9d6-d2cca49df391"
        },
        "date": "yyyy-mm-ddThh:mm:ss.ms",
        "is_active": true,
        "id": "82ebef20-cde6-4b87-be3d-3030b8fe481d"
    },
    "sub_spots": [
        {
            "place": {
                "country": "Cc",
                "city": "Cc",
                "street": "Cs",
                "map_url": null,
                "id": "34ea0425-ff38-4e2c-a7f1-3a8725533319"
            },
            "date": "yyyy-mm-ddThh:mm:ss.ms",
            "is_active": true,
            "id": "0f1363c7-9e74-45d7-8de3-29bbf3e07bc7"
        }
    ]
}
```
