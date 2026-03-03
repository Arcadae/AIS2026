from City import City
from typing import Optional, Union, NoReturn 

class Map:
    cities: list[City]

    def __init__(self, cities: Optional[list[City]] = None) -> None:
        if isinstance(cities, list):
            self.cities = cities
            return
        self.cities = []
    
    def append(self, city: City) -> Union[list[City], NoReturn]:
        if isinstance(city, City):
            return self.cities.append(city)
        raise ValueError("Это не экземпляр класса City")
    
    def __iter__(self):
        for city in self.cities:
            yield city
    
    def __len__(self) -> int:
        return len(self.cities)