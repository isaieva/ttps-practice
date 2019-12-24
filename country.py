from city import City


class Country:
    def __init__(self, name, xl, yl, xh, yh):
        self.name = name
        self.xl = xl
        self.yl = yl
        self.xh = xh
        self.yh = yh
        self.cities = []
        self.neighbors = []
        self.complete_day = 0

        for i in range(xl, xh + 1):
            for j in range(yl, yh + 1):
                city = City(i, j, self.name)
                self.cities.append(city)

    def is_complete(self, countries_amount, complete_day):
        for city in self.cities:
            if len(city.country_coins_mapping) != countries_amount:
                return False

        if self.complete_day != 0:
            return True
        # Check if this country was completed earlier or not
        elif self.complete_day == 0:
            self.complete_day = complete_day

        return True

    def update_balance(self):
        for city in self.cities:
            city.update_balance()

    def get_neighbor_cities(self, grid, countries):
        neighbors_names = []

        for city in self.cities:
            city.get_neighbor_cities(grid)

        for city in self.cities:
            for neighbor in city.neighbor_cities:
                # If country name of neighbor city is different, add it to neighbor country names list
                if neighbor.country_name != self.name:
                    neighbors_names.append(neighbor.country_name)

        for country in countries:
            for name in neighbors_names:
                if country.name == name:
                    self.neighbors.append(country)
