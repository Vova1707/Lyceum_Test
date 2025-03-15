from requests import get


def test_get_all():
    if get('http://localhost:8062/api/jobs/all').json() != []:
        return True
    return False


def test_get_one():
    if get('http://localhost:8062/api/jobs/2').json():
        return True
    return False


def test_add_job():
    if get('http://localhost:8062/api/jobs/2').json():
        return True
    return False

def test_delete_job():
    if get('http://localhost:8062/api/delete/2').json():
        return True
    return False


if __name__ == '__main__':
    tests = {'test_get_all': test_get_all(), 'test_get_one': test_get_one(), 'test_add_job': test_add_job(), 'test_delete_job': test_delete_job()}
    error = 0
    for test in tests:
        if not tests[test]:
            error = 1
            print(f'ОШИБКА В {test}')
    if not error:
        print('ОК')