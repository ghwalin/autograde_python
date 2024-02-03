from pylint import lint
from pylint.reporters import CollectingReporter


def py_lint():
    pylint_opts = [
        'py_main.py'
    ]

    reporter = CollectingReporter()
    pylint_obj = lint.Run(pylint_opts, reporter=reporter, exit=False)
    results = {
        'category': 'pylint',
        'points': 0,
        'max': 10,
        'messages': []
    }
    for message in reporter.messages:
        output = {
            'category': message.category,
            'message': message.msg,
            'path': message.path,
            'line': message.line
        }
        results['messages'].append(output)

    results['points'] = pylint_obj.linter.stats.global_note

    print (results)
    return results


if __name__ == '__main__':
    pass