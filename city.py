from copy import deepcopy


class City:

    MIN_SHARE_COUNT = 1000
    NEIGHBORS_COORD = ((-1, 0), (0, -1), (1, 0), (0, 1))

    def __init__(self, x, y, country_name):
        self.country_name = country_name
        self.x = x
        self.y = y
        self.neighbor_cities = []
        self.country_coins_mapping = [
            {'country_name': country_name, 'amount': 1000000}
        ]
        self.temp_mapping = [
            {'country_name': country_name, 'amount': 0}
        ]

    def change_balance(self):
        for i in range(len(self.country_coins_mapping)):
            if self.country_coins_mapping[i]['amount'] >= self.MIN_SHARE_COUNT:

                partition = self.country_coins_mapping[i]['amount'] // 1000

                for neighbor in self.neighbor_cities:
                    neighbor.add_other_countries_coins(self.country_coins_mapping[i]['country_name'], partition)

                self.temp_mapping[i]['amount'] -= partition * len(self.neighbor_cities)

    def add_other_countries_coins(self, country_name, amount):
        for coins in self.temp_mapping:
            # Check if city already has coins of this country
            if coins['country_name'] == country_name:
                # Prepare amount of coins from other country to add
                coins['amount'] += amount
                return

        self.temp_mapping.append({'country_name': country_name, 'amount': amount})

    def update_balance(self):
        for i in range(len(self.temp_mapping)):
            try:
                self.country_coins_mapping[i]['amount'] += self.temp_mapping[i]['amount']
            except IndexError:
                self.country_coins_mapping.append(deepcopy(self.temp_mapping[i]))

            # Reset temporary value
            self.temp_mapping[i]['amount'] = 0

    def get_neighbor_cities(self, grid):
        for i in self.NEIGHBORS_COORD:
            n_x, n_y = self.x + i[0], self.y + i[1]
            try:
                if grid[n_x][n_y] != 0:
                    self.neighbor_cities.append(grid[n_x][n_y])
            except IndexError:
                continue
