import pandas as pd
import numpy as np
from utils import calculate_quadratic_values


class CourtCoordinates:
    def __init__(self):
        self.hoop_loc_x = 0
        self.hoop_loc_y = 52
        self.hoop_loc_z = 100
        self.court_perimeter_coordinates = []
        self.three_point_line_coordinates = []
        self.backboard_coordinates = []
        self.hoop_coordinates = []
        self.court_lines_coordinates = []

    def calculate_court_perimeter_coordinates(self):
        # half court lines
        # x goes from 250 to -250 (50 feet wide)
        # y should go from 0 to 470 (full court is 94 feet long, half court is 47 feet)
        court_perimeter_bounds = [[-250, 0, 0], [250, 0, 0], [250, 470, 0], [-250, 470, 0], [-250, 0, 0]]

        self.court_perimeter_coordinates = court_perimeter_bounds

    def calculate_three_point_line_coordinates(self):
        # 3point line left side coordinates
        line_coordinates = [[-220, 0, 0], [-220, 140, 0]]

        # 3point line arc
        hoop_loc_x, hoop_loc_y = self.hoop_loc_x, self.hoop_loc_y
        a = 1
        b = -2 * 52
        d = 237.5  # the arc is 23ft and 9inches from the center of the hoop
        for x_coord in range(-218, 220, 2):
            c = hoop_loc_y ** 2 + (hoop_loc_x - x_coord) ** 2 - (d) ** 2
            y_coord = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
            line_coordinates.append([x_coord, y_coord, 0])

        # 3point line right side coordinates
        line_coordinates.append([220, 140, 0])
        line_coordinates.append([220, 0, 0])

        self.three_point_line_coordinates = line_coordinates

    def calculate_backboard_coordinates(self):
        backboard_coordinates = [[30, 40, 90], [30, 40, 130], [-30, 40, 130], [-30, 40, 90], [30, 40, 90]]

        self.backboard_coordinates = backboard_coordinates

    def calculate_hoop_coordinates(self):
        hoop_coordinates_top_half = []
        hoop_coordinates_bottom_half = []

        hoop_center_x, hoop_center_y, hoop_center_z = (self.hoop_loc_x, self.hoop_loc_y, self.hoop_loc_z)
        hoop_min_x, hoop_max_x = (-7.5, 7.5)
        hoop_radius = 7.5

        a = 1
        b = -2 * hoop_center_y
        for hoop_coord_x in np.arange(hoop_min_x, hoop_max_x, 0.5):
            c = hoop_center_y ** 2 + (hoop_center_x - hoop_coord_x) ** 2 - hoop_radius ** 2
            hoop_coord_y1, hoop_coord_y2 = calculate_quadratic_values(a, b, c)

            hoop_coordinates_top_half.append([hoop_coord_x, hoop_coord_y1, hoop_center_z])
            hoop_coordinates_bottom_half.append([hoop_coord_x, hoop_coord_y2, hoop_center_z])

        self.hoop_coordinates = hoop_coordinates_top_half + hoop_coordinates_bottom_half[::-1]

    def calculate_court_lines_coordinates(self):
        self.calculate_court_perimeter_coordinates()
        court_df = pd.DataFrame(self.court_perimeter_coordinates, columns=['x', 'y', 'z'])
        court_df['line_id'] = 'outside_perimeter'

        self.calculate_three_point_line_coordinates()
        three_point_line_df = pd.DataFrame(self.three_point_line_coordinates, columns=['x', 'y', 'z'])
        three_point_line_df['line_id'] = 'three_point_line'

        self.calculate_backboard_coordinates()
        backboard_df = pd.DataFrame(self.backboard_coordinates, columns=['x', 'y', 'z'])
        backboard_df['line_id'] = 'backboard'

        self.calculate_hoop_coordinates()
        hoop_df = pd.DataFrame(self.hoop_coordinates, columns=['x', 'y', 'z'])
        hoop_df['line_id'] = 'hoop'

        self.court_lines_coordinates = pd.concat([court_df, three_point_line_df, backboard_df, hoop_df], ignore_index = True, axis=0)

    def get_court_lines_coordinates(self):
        self.calculate_court_lines_coordinates()
        return self.court_lines_coordinates
