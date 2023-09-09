import pymongo
import dataclass_factory
from pymongo.database import Database
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from src.domain.value_objects import HashId
from src.domain.entities import Route
from src.domain.errors import RouteNotFoundError

class RouteRepository:
    def __init__(self, connection_string, collection: str):
        self.client: pymongo.MongoClient = pymongo.MongoClient(connection_string)
        db: Database = self.client['Bus']
        self.collection = db[collection]
        self.factory = dataclass_factory.Factory()

        self.collection.create_index([("move_from.place.city", pymongo.ASCENDING)])
        self.collection.create_index([("move_to.place.city", pymongo.ASCENDING)])

        self.collection.create_indexes([
            pymongo.IndexModel([("move_from.place.city", pymongo.ASCENDING)]),
            pymongo.IndexModel([("move_to.place.city", pymongo.ASCENDING)])
        ])

    def create(self, route: Route):
        route_dict = self.factory.dump(route)
        self.collection.insert_one(route_dict)

    def read_all(self) -> list[Route]:
        return [self.factory.load(route_dict, Route) for route_dict in self.collection.find()]

    def by_cities(self, move_from: str, move_to: str) -> list[Route]:
        query = {
            "$and": [
                {"move_from.place.city": move_from},
                {"move_to.place.city": move_to}
            ]
        }
        
        return [self.factory.load(route_dict, Route) for route_dict in self.collection.find(query)]

    def with_cities(self, move_from: str, move_to) -> list[Route]:
        query = {
            "$or": [
                {"$and": [
                    {"move_from.place.city": move_from},
                    {"move_to.place.city": move_to},
                ]},
                {"$and": [
                    {"move_from.place.city": move_from},
                    {"sub_spots.place.city": {"$regex": move_to, "$options": "i"}}
                ]},
                {"$and": [
                    {"sub_spots.place.city": {"$regex": move_from, "$options": "i"}},
                    {"sub_spots.place.city": {"$regex": move_to, "$options": "i"}}
                ]},
                {"$and": [
                    {"sub_spots.place.city": {"$regex": move_from, "$options": "i"}},
                    {"sub_spots.place.city": {"$regex": move_to, "$options": "i"}}
                ]},
            ]
        }

        return [self.factory.load(route_dict, Route) for route_dict in self.collection.find(query)]
    
    def by_id(self, route_id: HashId) -> Route:
        route = self.collection.find_one({"id": route_id})

        if not route:
            raise RouteNotFoundError(route_id)
    
        return self.factory.load(route, Route)

    def update(self, route: Route):
        with self.client.start_session() as session:
            with session.start_transaction(read_concern=ReadConcern("majority"), write_concern=WriteConcern("majority")):
                route_dict = self.factory.dump(route)
                self.collection.update_one({"id": route.id}, {"$set": route_dict})

    def delete(self, route_id: HashId):
        with self.client.start_session() as session:
            with session.start_transaction(read_concern=ReadConcern("majority"), write_concern=WriteConcern("majority")):
                result = self.collection.delete_one({"id": route_id})

                if result.deleted_count == 0:
                    raise RouteNotFoundError(route_id)

    def clear(self):
        self.collection.delete_many({})
