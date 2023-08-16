import json
import dataclass_factory
from src.domain.value_objects import HashId
from src.domain.entities import Route
from src.domain.errors import RouteNotFoundError

class RouteRepository:
    def __init__(self, filename: str):
        self._filename = filename
        self._factory = dataclass_factory.Factory()

    def _read_file(self) -> list[dict]:
        try:
            with open(self._filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        
        except FileNotFoundError:
            with open(self._filename, 'w', encoding='utf-8') as out:
                out.write("[]")
            
            data = []
        
        return data

    def _write_file(self, data):
        with open(self._filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, default=str)

    def create(self, route: Route):
        data = self._read_file()
        data.append(self._factory.dump(route))
        self._write_file(data)

    def read_all(self) -> list[Route]:
        data = self._read_file()
        return [self._factory.load(route_data, Route) for route_data in data]

    def update(self, route: Route):
        data = self._read_file()

        for idx, route_data in enumerate(data):
            if route_data['id'] == route.id:
                data[idx] = self._factory.dump(route)
                break
        else:
            raise RouteNotFoundError(route.id)

        self._write_file(data)

    def delete(self, route_id: HashId):
        data = self._read_file()
        filtered_data = list(filter(lambda r: r['id'] != route_id, data))

        if len(filtered_data) == len(data):
            raise RouteNotFoundError(route_id)
        
        self._write_file(filtered_data)
