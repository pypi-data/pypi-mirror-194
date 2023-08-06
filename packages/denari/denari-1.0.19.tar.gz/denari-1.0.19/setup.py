from setuptools import setup

setup(
    name='denari',
    version='1.0.19',
    description='DenariAnalytics OpenSouce Business and Tax Tools',
    author='Fadil Karim',
    author_email='insights@denarianalytics.com',
    packages=['denari'],
    install_requires=[
        'pandas',
        'numpy',
        'plotly',
        'dash'
    ],
    package_data={
    'TaxTools': ['UK Tax Tables/*.csv',
                 'UK Tax Tables/2020-2021/*.csv',
                 'UK Tax Tables/2021-2022/*.csv',
                 'UK Tax Tables/2022-2023/*.csv',
                 'UK Tax Tables/2023-2024/*.csv']
                 }

)