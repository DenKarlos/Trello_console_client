import requests
import sys
import config  # перед использованием текущего модуля необходимо указать данные в config.py

auth_params = {
    'key': config.trello_key,
    'token': config.trello_token
}

base_url = 'https://api.trello.com/1/{}'
board_id = config.board_id


def read():
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format(
        f'boards/{board_id}/lists'), params=auth_params).json()

    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        column_id = column['id']
        # Получим данные всех задач в колонке и перечислим все названия
        task_data = requests.get(base_url.format(
            f'lists/{column_id}/cards'), params=auth_params).json()
        # вместе с названием колонки выводим количество задач в ней
        print(column['name'], f'- {len(task_data)}')
        if not task_data:
            print('\tНет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'])


def create(name, column_name):
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format(
        f'boards/{board_id}/lists'), params=auth_params).json()

    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    for column in column_data:
        if column['name'] == column_name:
            # Создадим задачу с именем _name_ в найденной колонке
            requests.post(base_url.format('cards'), data={
                          'name': name, 'idList': column['id'], **auth_params})
            break


def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format(
        f'boards/{board_id}/lists'), params=auth_params).json()

    # Среди всех колонок нужно найти задачу по имени и получить её id
    # Необходимую информацию храним в списке _reply_task_ в виде кортежей,
    # где 1-ый элемент - имя колонки в которой хранится задача,
    # а 2-ой элемент - id этой задачи
    reply_task = []
    for column in column_data:
        column_id = column['id']
        column_tasks = requests.get(base_url.format(
            f'lists/{column_id}/cards'), params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                reply_task.append((column['name'], task['id']))

    if len(reply_task) > 1:  # если есть задачи с одинаковыми именами
        print('У вас несколько задач с таким именем. Выберете номер (№) задачи которую вы хотите перенести:')
        print(f'Задача - "{name}"')
        # смотрите описание функции ниже
        task_id = input_validation(reply_task)
    elif reply_task:  # если только одна задача с заданным именем
        task_id = reply_task[0][1]
    else:
        print('Данного названия задачи не существует')
        return -1

    # Переберём данные во всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    for column in column_data:
        if column['name'] == column_name:
            # И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format(f'cards/{task_id}/idList'), data={
                'value': column['id'], **auth_params})
            break


def input_validation(arr):
    '''Вывод задач с одинаковыми именами, где каждая нумеруется.
    Затем предоставляется пользователю ввести номер необходимой задачи, которую нужно переместить.
    Если ввёденные данные будут некорректны, то запрос на ввод данных от пользователя будет повторяться.
    Затем происходит возврат id необходимой задачи.'''
    for i, j in enumerate(arr):
        print(f'№ {i+1}. id - {j[1]}. Колонка - "{j[0]}"')
    while True:
        try:
            n = int(input('Введите № -> '))
            if n <= 0:
                raise Exception
            return arr[n-1][1]
        except Exception:
            print('Вы что-то неправильно ввели! Попробуйте снова ...')


def new_column(column_name):
    'Добавляет новый список задач в конец всех списков'
    requests.post(base_url.format(f'boards/{board_id}/lists'), data={
                  'name': column_name, 'idBoard': board_id, 'pos': 'bottom', **auth_params})


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'new_column':
        new_column(sys.argv[2])
