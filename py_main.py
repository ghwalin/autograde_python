import requests

from py_lint import py_lint
from py_test import py_test


def collect_results() -> None:
    """
    collects the results from all grading modules
    :return:
    """
    result = {
        'points': 0.0,
        'max': 0.0,
        'feedback': ''
    }

    testresults = py_test()
    result['points'] += testresults['points']
    result['max'] += testresults['max']
    result['feedback'] += html_out(testresults['feedback'])

    testresults = py_lint()
    result['points'] += testresults['points']
    result['max'] += testresults['max']
    result['feedback'] += html_out(testresults['feedback'])

    print(result)
    update_moodle(result)


def html_out(results: dict) -> str:
    """
    creates a html table from the results
    :param results:
    :return:
    """
    first_line = True
    output = '<table>'
    thead = '<tr>'
    for result in results:
        row = '<tr>'
        for key, value in result.items():
            if first_line:
                thead += f'<th>{key}</th>'
            row += f'<td>{value}</td>'
        if first_line:
            output += f'{thead}</tr>'
            first_line = False
        output += f'{row}</tr>'
    output += '</table>'
    return output


def update_moodle(result: dict) -> None:
    """
    calls the webservice to update the assignment in moodle
    :param result:
    :return:
    """
    # http://localhost/moodle/webservice/rest/server.php
    moodle_url = 'https://moodle.it.bzz.ch/moodle'
    token = 'aef1c413c539c619c48895e6f6f2d120'
    url = f'{moodle_url}/webservice/rest/server.php/?wstoken={token}&wsfunction=mod_assignexternal_update_grade'
    payload = {
        'assignment_name': 'lu99-a99-test',
        'user_name': 'ghwalin',
        'points': result['points'],
        'max': result['max'],
        'externallink': 'https://github.com/ghwalin/autograde_python',
        'feedback': result['feedback']
    }
    response = requests.post(url=url, data=payload)
    print(response.status_code)


if __name__ == '__main__':
    collect_results()
