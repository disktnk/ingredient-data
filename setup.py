from setuptools import setup


setup(
    name='ingredient-data',
    version='0.1.1',
    description='summarize ingredients tool',
    author='Daisuke Tanaka',
    author_email='duaipp@gmail.com',
    url='https://github.com/disktnk/ingredient-data',
    packages=['src'],
    entry_points={
        'console_scripts': ['ingred-data=src.show:main']
    },
    install_requires=[
        'texttable>=1.4.0',
        'zenhan>=0.5.2',
        'pandas>=0.23.4',
        'openpyxl>=2.5.9'
    ],
    test_require=[],
)
