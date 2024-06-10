def calc_points(exercise: dict, result=None) -> float:
    points = 0
    tags = {
        'Level 1': 1,
        'Level 2': 1.2,
        'Level 3': 1.8,
        'Level 4': 2.6,
        'Level 5': 4.2,
        'Shotmaking': 1.4,
        'Position Play': 2.0,
        'Straight Stroke': 1.2,
        'Jumping': 1.8,
        'Masse Shots': 1.5,
        'Safety Play': 1.9,
        'Breaking': 1.4,
        'Banking': 2.0,
        'Kicking': 1.4,
    }

    if result is None:
        i = 2.0
    else:
        i = result

    for tag in exercise['ex_tags']:
        k = tags[tag]
        points += k * i
    return points
