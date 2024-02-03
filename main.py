from py_lint import py_lint
from py_test import py_test


def main():
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


def html_out(results):
    output = '<table><tr><th>name</th><th>message</th><th>expected</th><th>actual</th><th>points</th><th>max</th></tr>'
    for result in results:
        line = f'<tr><td>{result.name}</td><td>{result.message}</td><td>{result.expected}</td><td>{result.actual}</td><td>{result.points}</td><td>{result.max}</td></tr>'
        output += line
    output += '</table>'
    return output


if __name__ == '__main__':
    main()
