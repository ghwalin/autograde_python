import os

import requests

from py_lint import py_lint
from py_test import py_test

def main():

    TARGET_URL = os.environ['TARGET_URL']
    TOKEN = os.getenv('TOKEN')
    FUNCTION = os.environ['FUNCTION']
    ASSIGNMENT = os.environ['ASSIGNMENT']
    USERNAME = os.environ['USERNAME']
    LINK = os.environ['LINK']

    print (f'TARGET_URL={TARGET_URL}, TOKEN={TOKEN}, FUNCTION={FUNCTION}, ASSIGNMENT={ASSIGNMENT}, USERNAME={USERNAME}, LINK={LINK}')

    result = collect_results()
    update_moodle(
        result=result,
        target_url='https://moodle.it.bzz.ch/moodle',
        token='aef1c413c539c619c48895e6f6f2d120',
        function='mod_assignexternal_update_grade',
        user_name='ghwalin',
        assignment='lu99-a99-test',
        external_link='https://github.com/ghwalin/autograde_python'
    )

def collect_results() -> dict:
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

    return result



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


def update_moodle(
        result: dict,
        target_url: str,
        token: str,
        function: str,
        user_name: str,
        assignment: str,
        external_link: str
) -> None:
    """
    calls the webservice to update the assignment in moodle
    :param result:
    :param target_url:
    :param token:
    :param function:
    :param user_name:
    :param assignment:
    :param external_link:
    :return:
    """
    url = f'{target_url}/webservice/rest/server.php/?wstoken={token}&wsfunction={function}'
    payload = {
        'assignment_name': assignment,
        'user_name': user_name,
        'points': result['points'],
        'max': result['max'],
        'externallink': external_link,
        'feedback': result['feedback']
    }
    # response = requests.post(url=url, data=payload, timeout=30)
    # print(response.status_code)


if __name__ == '__main__':
    main()
