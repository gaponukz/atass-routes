import json
from src.business.entities import Route
from src.business.errors import RouteNotFoundError

class RouteRepository:
    def __init__(self, filename: str):
        self._filename = filename

    def _read_file(self):
        try:
            with open(self._filename, 'r') as file:
                data = json.load(file)
        
        except FileNotFoundError:
            data = []
        
        return data

    def _write_file(self, data):
        with open(self._filename, 'w') as file:
            json.dump(data, file)

    def create(self, route: Route):
        data = self._read_file()
        data.append(route.model_dump())
        self._write_file(data)

    def read_all(self) -> list[Route]:
        data = self._read_file()
        return [Route(**route_data) for route_data in data]

    def update(self, route: Route):
        data = self._read_file()

        for idx, route_data in enumerate(data):
            if route_data['id'] == route.id:
                data[idx] = route.model_dump()
                break
        else:
            raise RouteNotFoundError(route.id)

        self._write_file(data)
