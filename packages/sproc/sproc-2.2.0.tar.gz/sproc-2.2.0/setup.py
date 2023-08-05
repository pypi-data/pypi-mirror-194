# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sproc']
setup_kwargs = {
    'name': 'sproc',
    'version': '2.2.0',
    'description': '⛏ Subprocesseses for subhumanses ⛏',
    'long_description': 'Run a command in a subprocess and yield lines of text from `stdout` and\n`stderr` independently.\n\nUseful for handling long-running proceesses that write to both `stdout` and\n`stderr`.\n\n### Simple Example\n\n    import sproc\n\n    CMD = \'my-unix-command "My Cool File.txt" No-file.txt\'\n\n    for ok, line in sproc.Sub(CMD) as sp:\n        if ok:\n             print(\' \', line)\n        else:\n             print(\'!\', line)\n\n    if sp.returncode:\n        print(\'Error code\', sp.returncode)\n\n    # Return two lists of text lines and a returncode\n    out_lines, err_lines, returncode = sproc.run(CMD)\n\n    # Call callback functions with lines of text read from stdout and stderr\n    returncode = sproc.call(CMD, save_results, print_errors)\n\n    # Log stdout and stderr, with prefixes\n    returncode = sproc.log(CMD)\n\n\n### [API Documentation](https://rec.github.io/sproc#sproc--api-documentation)\n',
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
