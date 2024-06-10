import json


def get_ex_dict(json_file, ex_name):
    # Читаем содержимое JSON файла
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Поиск блока данных по номеру упражнения
    exercise_data = None
    for exercise in data:
        if exercise['ex_name'].endswith(str(ex_name)):
            exercise_data = exercise
            break

    # Если упражнение найдено, выводим его значения в переменные
    if exercise_data:
        return exercise_data
    else:
        print("Exercise not found.")