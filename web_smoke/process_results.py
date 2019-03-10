import os
import argparse
from collections import defaultdict
from jinja2 import Template

template_path = os.path.dirname(os.path.realpath(__file__))

def render_results(folder, results):
    template = None
    with open(os.path.join(template_path, 'index.html'), 'r') as f:
        template = f.read()

    template = Template(template)
    with open(os.path.join(folder, 'index.html'), 'w') as f:
        f.write(template.render(results))

def collect_results(folder):
    actual_results = os.path.join(folder, 'actual')
    tests = defaultdict(lambda : {'passed':True})
    for f in os.listdir(actual_results):
        if '-diff' in f:
            name = f.replace('-diff.png', '')
            tests[name]['diff'] = os.path.join('actual', f)
            tests[name]['passed'] = False
        else:
            name = f.replace('.png', '')
            tests[name]['name'] = name
            tests[name]['actual'] = os.path.join('actual', f)
            tests[name]['expected'] = os.path.join('expected', f)

    tests = tests.values()
    return {
        'total': {
            'all': len(tests),
            'failed': len(filter(lambda x: not x['passed'], tests))
        },
        'tests': tests
    }


def main():
    parser = argparse.ArgumentParser(description='this script creates a nice index.html page in your results folder.')
    parser.add_argument('folder', nargs=1, type=str, help='path to folder with test results')

    args = parser.parse_args()
    folder = args.folder.pop()
    render_results(folder, collect_results(folder))
