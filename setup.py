from setuptools import setup

setup(
    name='laliga',
    version='0.1',
    py_modules=['laliga'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        laliga=laliga:cli
    ''',
)
