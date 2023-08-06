from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='inspector-python',
    version='0.1.14',
    description='Real-time Code Execution Monitoring of Python applications.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Inspector',
    author_email='support@inspector.dev',
    url='https://inspector.dev/',
    project_urls={
        'Documentation': 'https://docs.inspector.dev/guides/python/',
        'Source Code': 'https://github.com/inspector-apm/inspector-python',
        'Issue Tracker': 'https://github.com/inspector-apm/inspector-python/issues',
    },
    extras_require=dict(tests=['pytest']),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    license='MIT'
)
