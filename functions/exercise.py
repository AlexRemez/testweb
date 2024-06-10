import json


def get_ex_dict(json_file, exercise_num):
    # Читаем содержимое JSON файла
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Номер упражнения, которое вы ищете
    exercise_number = exercise_num.split(' ')[1]

    # Поиск блока данных по номеру упражнения
    exercise_data = None
    for exercise in data:
        if exercise['ex_name'].endswith(str(exercise_number)):
            exercise_data = exercise
            break

    # Если упражнение найдено, выводим его значения в переменные
    if exercise_data:
        return exercise_data
    else:
        print("Exercise not found.")