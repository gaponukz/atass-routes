import json
from src.business.entities import HashId
from src.business.entities import Route
from src.business.errors import RouteNotFoundError

class RouteRepository:
    def __init__(self, filename: str):
        self._filename = filename

    def _read_file(self) -> list[dict]:
        try:
            with open(self._filename, 'r') as file:
                data = json.load(file)
        
        except FileNotFoundError:
            data = []
        
        return data

    def _write_file(self, data):
        with open(self._filename, 'w') as file:
            json.dump(data, file, indent=4, default=str)

    def create(self, route: Route):
        data = self._read_file()
        data.append(route.dict())
        self._write_file(data)

    def read_all(self) -> list[Route]:
        data = self._read_file()
        return [Route(**route_data) for route_data in data]

    def update(self, route: Route):
        data = self._read_file()

        for idx, route_data in enumerate(data):
            if route_data['id'] == route.id:
                data[idx] = route.copy()
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
