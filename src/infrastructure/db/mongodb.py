import dataclass_factory
from pymongo import MongoClient
from src.domain.value_objects import HashId
from src.domain.entities import Route
from src.domain.errors import RouteNotFoundError

class RouteRepository:
    def __init__(self, connection_string, collection: str):
        client = MongoClient(connection_string)
        db = client['Bus']
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

    def update(self, route: Route):
        route_dict = self.factory.dump(route)
        self.collection.update_one({"id": route.id}, {"$set": route_dict})

    def delete(self, route_id: HashId):
        result = self.collection.delete_one({"id": route_id})

        if result.deleted_count == 0:
            raise RouteNotFoundError(f"Route with id {route_id} not found")

    def clear(self):
        self.collection.delete_many({})
