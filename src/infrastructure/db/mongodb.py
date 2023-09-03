import dataclass_factory
from pymongo import MongoClient
from pymongo.database import Database
from src.domain.value_objects import HashId
from src.domain.entities import Route
from src.domain.errors import RouteNotFoundError

class RouteRepository:
    def __init__(self, connection_string, collection: str):
        client: MongoClient = MongoClient(connection_string)
        db: Database = client['Bus']
        self.collection = db[collection]
        self.factory = dataclass_factory.Factory()

    def create(self, route: Route):
        route_dict = self.factory.dump(route)
        self.collection.insert_one(route_dict)

    def read_all(self) -> list[Route]:
        routes = []

        for route_dict in self.collection.find():
            route = self.factory.load(route_dict, Route)
            routes.append(route)
        
        return routes

    def by_cities(self, move_from: str, move_to: str) -> list[Route]:
        query = {
            "move_from": {
                "place": {"city": move_from.capitalize()}
            },
            "move_to": {
                "place": {"city": move_to.capitalize()}
            }
        }
        
        return [self.factory.load(route_dict, Route) for route_dict in self.collection.find(query)]

    def by_id(self, route_id: HashId) -> Route:
        route = self.collection.find_one({"id": route_id})

        if not route:
            raise RouteNotFoundError(route_id)
    
        return self.factory.load(route, Route)

    def update(self, route: Route):
        route_dict = self.factory.dump(route)
        self.collection.update_one({"id": route.id}, {"$set": route_dict})

    def delete(self, route_id: HashId):
        result = self.collection.delete_one({"id": route_id})

        if result.deleted_count == 0:
            raise RouteNotFoundError(route_id)

    def clear(self):
        self.collection.delete_many({})
