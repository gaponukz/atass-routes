import json
import dataclass_factory
from src.domain.entities import Route

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

    def read_all(self) -> list[Route]:
        data = self._read_file()
        return [self._factory.load(route_data, Route) for route_data in data]
