def calculate_quadratic_values(a, b, c):
    '''
    Given values a, b, and c,
    the function returns the output of the quadratic formula
    '''
    x1 = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
    x2 = (-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)

    return x1, x2
