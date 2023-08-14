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

## Private Endpoints

### Get unique routes

- URL: `/get_unique_routes`
- Method: `GET`
- Description: Return list of existing routes and count of copy
- Response example:
```json
[
  {
    "move_from": {
      "country": "Україна",
      "city": "Київ",
      "street": "Шевчнка 41",
      "map_url": null
  },
  "move_to": {
    "country": "Польща",
    "city": "Варшава",
    "street": "Житловий Targówek",
    "map_url": "https://goo.gl/maps/pJkRodQZbDwzNVhA7"
  },
  "count": 1
  }
]
```

### Get routes family

- URL: `/get_routes_family?move_from_city={cityName}&move_to_city={cityName}`
- Method: `GET`
- Description: Return list routes copy with the same city names
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
]
```

### Get route by id

- URL: `/get_route_by_id?route_id={id}`
- Method: `GET`
- Description: Return route by id
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

### Add new routes from prototype

- URL: `/get_route_by_id?route_id={id}`
- Method: `POST`
- Description: Create some routes from prototype
- Request example:
```json
{
  "dto" : {
    "route_prototype": {
      "move_from": {
        "place": {
          "country": "StartCountry",
          "city": "StartCity",
          "street": "StartStreet"
        },
        "id": "start_hash_id_value"
      },
      "move_to": {
        "place": {
          "country": "DestinationCountry",
          "city": "DestinationCity",
          "street": "DestinationStreet"
        },
        "from_start": 5,
        "id": "destination_hash_id_value"
      },
      "sub_spots": [
        {
          "place": {
            "country": "SubSpotCountry1",
            "city": "SubSpotCity1",
            "street": "SubSpotStreet1"
          },
          "from_start": 2,
          "id": "sub_spot1_hash_id_value"
        },
        {
          "place": {
            "country": "SubSpotCountry2",
            "city": "SubSpotCity2",
            "street": "SubSpotStreet2"
          },
          "from_start": 8,
          "id": "sub_spot2_hash_id_value"
        }
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
      "is_active": true,
      "prices": {
        "property1": 10,
        "property2": 20
      }
    },
    "departure_dates": [
      "2023-08-14T12:00:00",
      "2023-08-15T13:30:00"
    ]
  }
}
```
