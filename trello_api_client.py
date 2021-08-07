import requests
import sys

auth_params = {
    'key': '3ef4502a5679f000ec0aae3cf27c9196',
    'token': '234d1150410383cd1002cd29e912c1cd72729be646c6cffdf26d2a0cbaf81a0b',
}

base_url = 'https://api.trello.com/1/{}'
board_id = '3D3dhPoA'


def read():
    column_data = requests.get(base_url.format(
        f'boards/{board_id}/lists'), params=auth_params).json()
    for column in column_data:
        print(column['name'])
        column_id = column['id']
        task_data = requests.get(base_url.format(
            f'lists/{column_id}/cards'), params=auth_params).json()
        if not task_data:
            print('\tНет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'])


def create(name, column_name):
    column_data = requests.get(base_url.format(
        f'boards/{board_id}/lists'), params=auth_params).json()

    for column in column_data:
        if column['name'] == column_name:
            requests.post(base_url.format('cards'), data={
                          'name': name, 'idList': column['id'], **auth_params})
            break


def move(name, column_name):
    column_data = requests.get(base_url.format(
        f'boards/{board_id}/lists'), params=auth_params).json()

    task_id = None
    for column in column_data:
        column_id = column['id']
        column_tasks = requests.get(base_url.format(
        f'lists/{column_id}/cards'), params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
        if task_id:
            break

    for column in column_data:
        if column['name'] == column_name:
            requests.put(base_url.format(f'cards/{task_id}/idList'), data={
                          'value': column['id'], **auth_params})
            break


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
