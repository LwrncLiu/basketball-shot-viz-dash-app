# TODO: Create a shot class for these functions to live in
import numpy as np
from utils import calculate_quadratic_values

def calculate_vertex_quadratic_coefficients(x1, y1, x2, y2, k):
    '''
    Given the 2D coordinates of the shot, the hoop, and shot height,
    the functions returns the coefficients of the quadratic formula.
    The equations for a, b, and c are derived from using two parabola vertex form equations to solve for h (vertex x_value)
    '''
    a = y2 - y1
    b = - 2 * x1 * (y2 - k) + 2 * x2 * (y1 - k)
    c = x1 ** 2 * (y2 - k) - x2 ** 2 * (y1 - k)

    return a, b, c


def calculate_2d_parabola_coefficent_a(x, y, h, k):
    '''
    Given an (x, y) pair of a parabola as well as the vertex (x, y) pair, return the a coefficient of the quadratic equation
    a is derived from the vertex form: y = a(x - h)**2 + k
    '''
    a = (y - k) / (x - h) ** 2

    return a


def calculate_parabola_vertex(x1, y1, x2, y2, k):
    # calculate the a, b, and c coefficients for the parabola of the shot from the side view
    # todo, calculate the coefficients for the parabola from the face-on view
    # if shot_start_y has the same value as the hoop_y, then we have a divide by 0 error
    a, b, c = calculate_vertex_quadratic_coefficients(x1, y1, x2, y2, k)

    # solve for possible vertex values based on quadratic equation
    shot_vertex_y1, shot_vertex_y2 = calculate_quadratic_values(a, b, c)

    # choose the shot_vertex_y that lies between shot_start_y and hoop_y
    if x1 <= shot_vertex_y1 <= x2 or x2 <= shot_vertex_y1 <= x1:
        shot_vertex_y = shot_vertex_y1
    else:
        shot_vertex_y = shot_vertex_y2

    return shot_vertex_y


def calculate_shot_path_coordinates(shot_loc):
    '''
    Given a (x, y, z) coordinate of the start of a shot,
    the function returns 101 coordinates in 3D space that
    '''
    # shot coordinate
    shot_start_x, shot_start_y, shot_start_z = shot_loc

    # setting 17 feet as height of all shots
    shot_vertex_z = 170

    # hoop coordinate
    hoop_x, hoop_y, hoop_z = (0, 52, 100)

    # limit to 100 coordinates per shot
    num_coordinates = 100
    shot_path_coordinates = []

    # if the shot is within roughly the same y-plane as the hoop,
    # calculate the shot coordinates as a 2d parabola from the front-on view
    if shot_start_y <= 100:
        # calculate the y_coordinate of the shot vertex
        shot_vertex_x = calculate_parabola_vertex(shot_start_x,
                                                  shot_start_z,
                                                  hoop_x,
                                                  hoop_z,
                                                  shot_vertex_z)

        # calculate the a value from the vertex form of a parabola
        a = calculate_2d_parabola_coefficent_a(shot_start_x,
                                               shot_start_z,
                                               shot_vertex_x,
                                               shot_vertex_z)

        # now calculate y-values for all x-values between shot_start_x and hoop_x
        # as well as the horizontal shift between the hoop and the shot for the 3rd dimension (may not be necessary)
        x_shift = hoop_x - shot_start_x
        x_shift_per_coord = x_shift / num_coordinates

        y_shift = hoop_y - shot_start_y
        y_shift_per_coord = y_shift / (num_coordinates)

        for index, x in enumerate(np.arange(shot_start_x, hoop_x - 1, x_shift_per_coord)):
            z = a * (x - shot_vertex_x) ** 2 + shot_vertex_z
            shot_path_coordinates.append([x, shot_start_y + (y_shift_per_coord * index), z, index])

    # calculate the shot coordinates as a 2d parabola from the side view
    else:
        # calculate the y_coordinate of the shot vertex
        shot_vertex_y = calculate_parabola_vertex(shot_start_y,
                                                  shot_start_z,
                                                  hoop_y,
                                                  hoop_z,
                                                  shot_vertex_z)

        # calculate the a value from the vertex form of a parabola
        a = calculate_2d_parabola_coefficent_a(shot_start_y,
                                               shot_start_z,
                                               shot_vertex_y,
                                               shot_vertex_z)

        # now calculate x-values for all y-values between shot_start_y and hoop_y
        # as well as the horizontal shift between the hoop and the shot for the 3rd dimension
        x_shift = hoop_x - shot_start_x
        x_shift_per_coord = x_shift / num_coordinates

        y_shift = hoop_y - shot_start_y
        y_shift_per_coord = y_shift / (num_coordinates)

        for index, y in enumerate(np.arange(shot_start_y, hoop_y - 1, y_shift_per_coord)):
            z = a * (y - shot_vertex_y) ** 2 + shot_vertex_z
            shot_path_coordinates.append([shot_start_x + (x_shift_per_coord * index), y, z, index])

    return shot_path_coordinates