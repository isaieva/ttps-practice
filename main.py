from country import *
from city import *
from operator import and_
import os


class Main:

    INPUT_ARGS_NUMBER = 5

    def __init__(self):
        self.grid = []
        self.countries = []
        self.errors = []
        self.cases_count = 0
        self.countries_amount = 0
        self.days = 0
        self.case_is_correct = True
        self.grid_length = 0
        self.grid_height = 0

    def process(self, name):
        with open(name, 'r') as file_obj:
            country_number = 0
            line_number = 0
            case_is_started = False

            for line in file_obj:
                line_number += 1

                if not line.strip():
                    continue
                if case_is_started:
                    country_number += 1

                    if self.case_is_correct:
                        args = line.split()

                        if self.check_line_correct(args, line_number):
                            try:
                                xl, yl, xh, yh = int(args[1]), int(args[2]), int(args[3]), int(args[4])
                            except (ValueError, TypeError):
                                self.errors.append(
                                    {'case': self.cases_count, 'text': f'Incorrect argument. Line {line_number}'}
                                )
                                self.case_is_correct = False
                                return False

                            country = Country(
                                name=args[0],
                                xl=xl,
                                yl=yl,
                                xh=xh,
                                yh=yh
                            )

                            self.grid_length = max(self.grid_length, xl + 1, xh + 1)
                            self.grid_height = max(self.grid_height, yl + 1, yh + 1)

                            self.countries.append(country)

                    if country_number == self.countries_amount:
                        case_is_started = False

                else:
                    # Check if we ended reading case or it's just the beginning of file_obj
                    if self.cases_count > 0:

                        if self.case_is_correct:
                            self.create_grid()

                            if self.case_is_correct:
                                self.count_days()

                        self.print_count()
                        self.clear()

                    try:
                        country_number = 0
                        self.cases_count += 1

                        self.countries_amount = int(line)

                        if self.countries_amount == 0:
                            break
                        elif self.countries_amount < 0:
                            raise ValueError

                        case_is_started = True

                    except ValueError:
                        self.errors.append({'case': self.cases_count, 'text': f'Error in line {line_number}'})
                        self.case_is_correct = False

    def check_line_correct(self, args, line_number):
        if len(args) != self.INPUT_ARGS_NUMBER:
            self.errors.append(
                {'case': self.cases_count, 'text': f'Incorrect number of arguments in line: {line_number}'}
            )
            self.case_is_correct = False
            return False
        else:
            if not args[0].isalpha():
                self.errors.append({'case': self.cases_count,
                                    'text': f'Country name should contain letters only. Line {line_number}'})
                self.case_is_correct = False
                return False
            elif len(args[0]) > 25:
                self.errors.append({'case': self.cases_count,
                                    'text': f'Country name should be at most 25 chars. Line {line_number}'})
                self.case_is_correct = False
                return False

            for i in range(1, self.INPUT_ARGS_NUMBER):
                try:
                    if int(args[i]) < 0:
                        self.errors.append(
                            {
                                'case': self.cases_count,
                                'text': f'Coordinate should be positive number. Line {line_number}'
                            }
                        )
                        self.case_is_correct = False
                        return False

                except ValueError:
                    self.errors.append(
                        {'case': self.cases_count, 'text': f'Incorrect value. Line {line_number}'}
                    )
                    self.case_is_correct = False
                    return False
        return True

    def count_days(self):

        while not self.is_complete():

            self.days += 1

            for i in range(self.grid_length):
                for j in range(self.grid_height):
                    current_city = self.grid[i][j]

                    if current_city != 0:
                        current_city.change_balance()

            for country in self.countries:
                country.update_balance()

    def check_countries_connected(self, country, country_list=None):
        #country_list = country_list

        if country_list is None:
            country_list = []
        if country in country_list:
            return
        else:
            country_list.append(country)

        for neighbor in country.neighbors:
            # recursively get neighbors
            self.check_countries_connected(neighbor, country_list)

        if len(country_list) == len(self.countries):
            return True

        return False

    def check_countries_unique(self):
        country_names = []

        for country in self.countries:
            if country.name not in country_names:
                country_names.append(country.name)
            else:
                return False

        return True

    def is_complete(self):
        result = True

        for country in self.countries:
            result = and_(country.is_complete(self.countries_amount, self.days), result)
        return result

    def create_grid(self):
        if not self.check_countries_unique():
            self.errors.append(
                {'case': self.cases_count, 'text': 'Countries names should be unique'}
            )
            self.case_is_correct = False
            return

        for i in range(self.grid_length):
            cities = []
            for j in range(self.grid_height):
                cities.append(0)
            self.grid.append(cities)

        for country in self.countries:
            for city in country.cities:
                if self.grid[city.x][city.y] == 0:
                    self.grid[city.x][city.y] = city
                else:
                    self.errors.append({'case': self.cases_count,
                                        'text': 'Multiple cities should have different coordinates'})
                    self.case_is_correct = False
                    return

        for country in self.countries:
            country.get_neighbor_cities(self.grid, self.countries)

        if not self.check_countries_connected(self.countries[0], []):
            self.errors.append({'case': self.cases_count, 'text': 'Countries not connected'})
            self.case_is_correct = False

    def clear(self):
        self.grid = []
        self.countries = []
        self.countries_amount = 0
        self.days = 0
        self.grid_length = 0
        self.grid_height = 0
        self.case_is_correct = True

    def print_count(self):
        print(f'Case: {self.cases_count}')

        if self.case_is_correct:
            countries = sorted(self.countries, key=lambda c: (c.complete_day, c.name))

            for country in countries:
                print(country.name, country.complete_day)
        else:
            for error in self.errors:
                if error['case'] == self.cases_count:
                    print(f"Error: {error['text']}")
        print()


FILE_PATH = os.path.join('.', 'test1.txt')

count = Main()
count.process(FILE_PATH)
