# TODO: Create a shot class for these functions to live in
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


class BasketballShot:
    def __init__(self,
                 shot_start_x,
                 shot_start_y,
                 shot_distance,
                 shot_result,
                 game_id,
                 game_event_id,
                 subject):
        self.hoop_loc_x = 0
        self.hoop_loc_y = 52
        self.hoop_loc_z = 100
        self.shot_vertex_z = 0
        self.num_coordinates = 100
        self.shot_start_x = -1 * shot_start_x
        self.shot_start_y = shot_start_y + self.hoop_loc_y  # coordinates are relative to the center of the rim
        self.shot_start_z = 0  # all shots start on the floor
        self.shot_result = shot_result
        self.shot_result_string = 'shot made' if self.shot_result == 1 else 'shot miss'
        self.game_id = game_id
        self.game_event_id = game_event_id
        self.shot_id = str(self.game_id) + '_' + str(self.game_event_id)
        self.shot_distance = shot_distance
        self.shot_path_coordinates_df = pd.DataFrame()
        self.calculate_side_on = True
        self.shot_hoop_xy_slope = None
        self.shot_hoop_xy_y_intercept = None
        self.subject = subject


    @staticmethod
    def calculate_quadratic_values(a, b, c):
        '''
        Given values a, b, and c,
        the function returns the output of the quadratic formula
        '''
        x1 = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
        x2 = (-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)

        return x1, x2

    @staticmethod
    def calculate_vertex_quadratic_coefficients(x1, y1, x2, y2, k):
        # Given the 2D coordinates of the shot, the hoop, and shot height, the functions returns the coefficients of
        # the quadratic formula. The equations for a, b, and c are derived from using two parabola vertex form
        # equations to solve for h (vertex x_value)
        a = y2 - y1
        b = - 2 * x1 * (y2 - k) + 2 * x2 * (y1 - k)
        c = x1 ** 2 * (y2 - k) - x2 ** 2 * (y1 - k)

        return a, b, c

    @staticmethod
    def calculate_2d_parabola_coefficient_a(x, y, h, k):
        # Given an (x, y) pair of a parabola as well as the vertex (x, y) pair, return the 'a' coefficient of the
        # quadratic equation a is derived from the vertex form: y = a(x - h)**2 + k
        a = (y - k) / (x - h) ** 2

        return a


    def calculate_parabola_vertex(self, x1, y1, x2, y2, k):
        # calculate the a, b, and c coefficients for the parabola of the shot from the side view
        # if shot_start_y has the same value as the hoop_y, then we have a divide by 0 error
        a, b, c = self.calculate_vertex_quadratic_coefficients(x1, y1, x2, y2, k)

        # solve for possible vertex values based on quadratic equation
        shot_vertex_y1, shot_vertex_y2 = self.calculate_quadratic_values(a, b, c)

        # choose the shot_vertex_y that lies between shot_start_y and hoop_y
        if x1 <= shot_vertex_y1 <= x2 or x2 <= shot_vertex_y1 <= x1:
            shot_vertex_y = shot_vertex_y1
        else:
            shot_vertex_y = shot_vertex_y2

        return shot_vertex_y

    def calculate_shot_height(self):
        if self.shot_distance >= 24:  # 3 point territory
            self.shot_vertex_z = 170
        elif self.shot_distance >= 9:  # mid-range territory
            self.shot_vertex_z = 150
        else:  # in-the-paint/layup territory
            self.shot_vertex_z = 130

    def calculate_shot_to_basket_slope_intercept(self):
        x1, y1 = self.hoop_loc_x, self.hoop_loc_y
        x2, y2 = self.shot_start_x, self.shot_start_y
        self.shot_hoop_xy_slope = (y2 - y1)/(x2 - x1)
        self.shot_hoop_xy_y_intercept = y1 - self.shot_hoop_xy_slope * x1

    def change_shot_end_if_miss(self):
        # If it is a miss, change the hoop_loc_x and hoop_loc_y to the rim instead of the center of the hoop,
        # illustrating a miss that hits the rim

        # if the shot is on the same x-axis as the hoop, then just move
        # the hoop y coordinate up by the radius (7.5)
        if self.hoop_loc_x == self.shot_start_x:
            self.hoop_loc_y = self.hoop_loc_y + 7.5

        else:
            self.calculate_shot_to_basket_slope_intercept()

            m = self.shot_hoop_xy_slope
            b = self.shot_hoop_xy_y_intercept
            h = self.hoop_loc_x
            k = self.hoop_loc_y
            r = 7.5

            a_coefficient = m**2 + 1
            b_coefficient = (-2*h) + (2*m*b) - (2*m*k)
            c_coefficient = (h**2) + (b**2) - (2*b*k) + (k**2) - (r**2)
            x1, x2 = self.calculate_quadratic_values(a_coefficient, b_coefficient, c_coefficient)

            # set new x for trajectory end as the rim of the hoop
            self.hoop_loc_x = x1 if (self.shot_start_x < x1 < h) or (h < x1 < self.shot_start_x) else x2

            # calculate new y based on the new x
            new_x = self.hoop_loc_x
            self.hoop_loc_y = m*new_x + b

    def set_calculation_method(self):
        # default is to calculate the parabola of a shot from the court-side view
        # however, shots that are directly in-line will need to be calculated from the front-on view instead.

        if self.shot_start_y <= 100 and self.shot_start_x != 0:
            self.calculate_side_on = False

    def calculate_shot_hoop_overlap(self):
        """
        Calculate if the shot starts inside the cylindrical column of the hoop using the distance between two points
        equation: d = sqrt(xp - xc)**2 + (yp - yc)**2) where (xp, yp) is the shot start and (xc, yc) is the hoop center
        """

        d = ((self.shot_start_x - self.hoop_loc_x)**2 + (self.shot_start_y - self.hoop_loc_y)**2)**0.5
        if d <= 7.5:  # radius of the hoop
            return False
        return True


    def calculate_shot_path_coordinates(self):
        """
        Given a (x, y, z) coordinate of the start of a shot,
        the function returns 101 coordinates in 3D space that
        """

        # if the shot is not determined to be possible, return a dataframe with only the starting point of a shot
        shot_plot_possible = self.calculate_shot_hoop_overlap()

        # if the shot is within roughly the same y-plane as the hoop,
        # calculate the shot coordinates as a 2d parabola from the front-on view
        self.set_calculation_method()

        # if shot is inside the hoop column, only return one row,
        # the shot start location
        if not shot_plot_possible:
            shot_path_coordinates = [0,
                                     self.shot_start_x,
                                     self.shot_start_y,
                                     self.shot_start_z,
                                     self.shot_id,
                                     self.subject,
                                     self.shot_result_string]

            self.shot_path_coordinates_df = pd.DataFrame([shot_path_coordinates],
                                                         columns=['line_index',
                                                                  'x',
                                                                  'y',
                                                                  'z',
                                                                  'line_id',
                                                                  'subject',
                                                                  'shot_result'])
            return

        if self.shot_result == 0:
            self.change_shot_end_if_miss()

        # shot coordinate
        shot_start_x, shot_start_y, shot_start_z = self.shot_start_x, self.shot_start_y, self.shot_start_z

        # determine shot height for the shot.
        self.calculate_shot_height()
        shot_vertex_z = self.shot_vertex_z

        # hoop coordinate
        hoop_x, hoop_y, hoop_z = self.hoop_loc_x, self.hoop_loc_y, self.hoop_loc_z

        # limit to 100 coordinates per shot
        num_coordinates = self.num_coordinates
        shot_path_coordinates = []

        if not self.calculate_side_on:
            # calculate the y_coordinate of the shot vertex
            shot_vertex_x = self.calculate_parabola_vertex(shot_start_x,
                                                           shot_start_z,
                                                           hoop_x,
                                                           hoop_z,
                                                           shot_vertex_z)

            # calculate the 'a' value from the vertex form of a parabola
            a = self.calculate_2d_parabola_coefficient_a(shot_start_x,
                                                         shot_start_z,
                                                         shot_vertex_x,
                                                         shot_vertex_z)

            # now calculate y-values for all x-values between shot_start_x and hoop_x
            # as well as the horizontal shift between the hoop and the shot for the 3rd dimension (may not be necessary)

            y_shift = hoop_y - shot_start_y
            y_shift_per_coord = y_shift / num_coordinates

            for shot_index, x in enumerate(np.linspace(shot_start_x, hoop_x, num_coordinates + 1)):

                z = a * (x - shot_vertex_x) ** 2 + shot_vertex_z
                shot_path_coordinates.append([shot_index, x, shot_start_y + (y_shift_per_coord * shot_index), z])

        # calculate the shot coordinates as a 2d parabola from the side view
        else:
            # calculate the y_coordinate of the shot vertex
            shot_vertex_y = self.calculate_parabola_vertex(shot_start_y,
                                                           shot_start_z,
                                                           hoop_y,
                                                           hoop_z,
                                                           shot_vertex_z)

            # calculate the 'a' value from the vertex form of a parabola
            a = self.calculate_2d_parabola_coefficient_a(shot_start_y,
                                                         shot_start_z,
                                                         shot_vertex_y,
                                                         shot_vertex_z)

            # now calculate x-values for all y-values between shot_start_y and hoop_y
            # as well as the horizontal shift between the hoop and the shot for the 3rd dimension
            x_shift = hoop_x - shot_start_x
            x_shift_per_coord = x_shift / num_coordinates

            for shot_index, y in enumerate(np.linspace(shot_start_y, hoop_y, num_coordinates + 1)):
                z = a * (y - shot_vertex_y) ** 2 + shot_vertex_z
                shot_path_coordinates.append([shot_index, shot_start_x + (x_shift_per_coord * shot_index), y, z])

        # create shot path coordinates dataframe
        self.shot_path_coordinates_df = pd.DataFrame(shot_path_coordinates, columns=['line_index', 'x', 'y', 'z'])
        self.shot_path_coordinates_df['line_id'] = self.shot_id
        self.shot_path_coordinates_df['subject'] = self.subject
        self.shot_path_coordinates_df['shot_result'] = self.shot_result_string

    def get_shot_path_coordinates(self):
        self.calculate_shot_path_coordinates()

        return self.shot_path_coordinates_df