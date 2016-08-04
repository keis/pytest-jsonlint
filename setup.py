from setuptools import setup

setup(
    name='pytest-jsonlint',
    version='0.0.1',
    py_modules=['pytest_jsonlint'],
    entry_points={
        'pytest11': ['jsonlint = pytest_jsonlint']
    },
    install_requires=['demjson', 'pytest']
)
