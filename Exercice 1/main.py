import numpy as np

def fill_map(map, enter):
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            map[i][j] = int(enter[i * map.shape[1] + j])
    return map

def print_map(map):
    for i in range(map.shape[0]):
        for j in range(cols):
            print(map[i][j], end=" ")
        print()

def get_position(map, number):
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i][j] == number:
                return (i, j)
    return None

def get_distance(map, begin, finish):
    if begin == finish:
        return 0
    else:
        position_begin = get_position(map, begin)
        position_finish = get_position(map, finish)
        if position_begin is None or position_finish is None:
            raise ValueError(f"One of the numbers {begin} or {finish} is not on the map")
        row_diff = abs(position_begin[0] - position_finish[0])
        col_diff = abs(position_begin[1] - position_finish[1])
        distance = max(row_diff, col_diff)
        print(f"Distance from {begin} to {finish}: {distance} (Positions: {position_begin} to {position_finish})")
        return distance

def get_total_distance(map, parkour):
    distance = 0
    for i in range(len(parkour) - 1):
        distance += get_distance(map, int(parkour[i]), int(parkour[i + 1]))
    return distance


if __name__ == "__main__":
    rows, cols = (3, 3)

    # Création d'un tableau de zéros
    map = np.zeros((rows, cols), dtype=int)
    print(map)

    try:
    # Saisie de la chaîne de 9 chiffres
        enter = "923857614"  
        if len(enter) != 9:
            raise ValueError("The string must have 9 numbers")
        if not enter.isdigit():
            raise ValueError("The string must have positive numbers")
    except ValueError as e:
        print(e)
        exit()

    parkour = "423692"  # Exemple fourni dans le PDF

    map = fill_map(map, enter)


    print("Clavier configuré :")
    print_map(map)


    try:
        distance = get_total_distance(map, parkour)
        print("Total distance :", distance)
    except ValueError as e:
        print(e)
