from requests import get, delete, post


def test_get_all():
    return get('http://localhost:8062/api/jobs').json()


def test_get_one():
    return get('http://localhost:8062/api/jobs/1').json()


def test_add_job():
    return get('http://127.0.0.1:8062/api/jobs/add')


def test_edit_job():
    return get('http://localhost:8062/api/jobs/edit/1')


def test_delete_job():
    return get('http://localhost:8062/api/jobs/delete/2')


def test_rest_api_get_one_user():
    return get('http://localhost:8062/api/v1/users/1').json()


def test_rest_api_add_user():
    return post('http://localhost:8062/api/v1/users').json()


def get_all_users():
    return get('http://localhost:8062/api/v1/users').json()


def test_rest_api_delete_user():
    return get('http://localhost:8062/api/v1/users/7').json()


if __name__ == '__main__':
    print('Тесты Rest-Api User:')
    tests = {'test_rest_api_get_one_user': test_rest_api_get_one_user(), 'test_rest_api_add_user': test_rest_api_add_user(), 'get_all_users': get_all_users(), 'test_rest_api_delete_user': test_rest_api_delete_user()}
    for test in tests:
        print(f'{test}: {tests[test]}')
    print('-' * 100)
    print('Какие-то тесты')
    ERROR = {'error': 'Not found'}
    tests = {'test_get_all': test_get_all(), 'test_get_one': test_get_one(), 'test_add_job': test_add_job(), 'test_edit_job': test_edit_job(), 'test_delete_job': test_delete_job()}
    error = 0
    for test in tests:
        if tests[test] == ERROR:
            error = 1
            print(f'ОШИБКА В {test}')
        else:
            print(f'{test}: {tests[test]}')
    if not error:
        print('ОК')
