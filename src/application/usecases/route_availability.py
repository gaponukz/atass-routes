import typing
import datetime
from collections import defaultdict
from src.domain.entities import Route
from src.domain.entities import Path
from src.domain.entities import Spot
from src.domain.entities import Passenger
from src.domain.value_objects import HashId
from src.application.dto import GetAviableRoutesDTO

class ReadAbleDataBase(typing.Protocol):
    def read_all(self) -> list[Route]: ...

    def with_cities(self, move_from: str, move_to) -> list[Route]: ...

class RouteAvailabilityUseCase:
    def __init__(self, db: ReadAbleDataBase) -> None:
        self._db = db
    
    def generate_pathes(self, dto: GetAviableRoutesDTO) -> list[Path]:
        pathes = []
        routes = self._db.with_cities(dto.move_from_city, dto.move_to_city)

        for route in routes:
            for path in self._generating_aviable_pathes(route):
                if path.move_from.place.city.lower() != dto.move_from_city.lower():
                    continue

                if path.move_to.place.city.lower() != dto.move_to_city.lower():
                    continue
                
                if dto.date != "*":
                    if path.move_from.date.strftime("%d.%m.%Y") != dto.date:
                        continue

                pathes.append(path)
        
        return pathes
    
    def get_availability_graph(self) -> dict[str, list[str]]:
        routes = self._db.read_all()
        result: dict[str, list[str]] = {}

        for route in routes:
            for path in self._generating_aviable_pathes(route):
                if not result.get(path.move_from.place.city):
                    result[path.move_from.place.city] = []
                
                result[path.move_from.place.city].append(path.move_to.place.city)
        
        return result

    def _generating_aviable_pathes(self, route: Route) -> list[Path]:
        all_spots = self._get_routes_spots(route)
        results: list[Path] = []

        if not self._is_actual_route(route):
            return []
        
        sits: defaultdict[str, defaultdict[str, bool]] = defaultdict(defaultdict)

        for passenger in route.passengers:
            move_froms = list(filter(lambda s: s.id == passenger.moving_from_id, all_spots))
            if not move_froms:
                continue

            move_from = move_froms[0]

            move_tos = list(filter(lambda s: s.id == passenger.moving_towards_id, all_spots))
            if not move_tos:
                continue

            move_to = move_tos[0]

            passing_spots = filter(lambda s: move_from.date <= s.date < move_to.date, all_spots)

            for spot in passing_spots:
                sits[passenger.id][spot.id] = True
                            
        for start_spot, end_spot in self._iter_different_spots(all_spots):
            if not all((
                self._is_actual_spot(start_spot),
                route.prices.get(start_spot.id, {}).get(end_spot.id)
            )):
                continue

            path_spots = filter(lambda s: start_spot.date <= s.date < end_spot.date, all_spots)

            for spot in path_spots:
                count = 0
                for col in sits:
                    if not sits.get(col):
                        continue

                    if not sits[col].get(spot.id):
                        continue

                    count += 1

                if count >= route.passengers_number:                    
                    break
            
            else:
                results.append(Path(
                    move_from=start_spot,
                    move_to=end_spot,
                    price=route.prices[start_spot.id][end_spot.id],
                    root_route_id=route.id
                ))

        return results
    
    def _get_route_sits(self, all_spots: list[Spot], passengers: list[Passenger]) -> dict[HashId, dict[HashId, int]]:
        sits = {
            all_spots[i].id: {
                all_spots[j].id: 0 for j in range(len(all_spots))
            } for i in range(len(all_spots))
        }

        for passenger in passengers:
            move_from_date = list(filter(lambda s: s.id == passenger.moving_from_id, all_spots))[0].date
            move_to_date = list(filter(lambda s: s.id == passenger.moving_towards_id, all_spots))[0].date

            for spot in filter(lambda s: move_from_date <= s.date < move_to_date, all_spots):
                for sit in sits[spot.id]:
                    sits[sit][spot.id] += 1
        
        return sits
    
    def _iter_different_spots(self, all_spots: list[Spot]) -> typing.Iterator[tuple[Spot, Spot]]:
        for i in range(len(all_spots)-1):
            for j in range(i+1, len(all_spots)):
                yield (all_spots[i], all_spots[j])

    def _is_actual_spot(self, spot: Spot) -> bool:
        return spot.date > datetime.datetime.now()

    def _is_actual_route(self, route: Route) -> bool:
        return self._is_actual_spot(route.move_to if not route.sub_spots else route.sub_spots[-1])

    def _get_routes_spots(self, route: Route) -> list[Spot]:
        routes_spots = route.sub_spots.copy()
        routes_spots.insert(0, route.move_from)
        routes_spots.insert(-1, route.move_to)

        return sorted(routes_spots, key=lambda s: s.date)
