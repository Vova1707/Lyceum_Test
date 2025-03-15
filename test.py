from requests import get


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


if __name__ == '__main__':
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