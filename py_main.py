from py_lint import py_lint
from py_test import py_test


def collect_results():
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


def html_out(results):
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


if __name__ == '__main__':
    collect_results()
