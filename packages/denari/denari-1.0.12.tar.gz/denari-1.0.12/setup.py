from setuptools import setup

setup(
    name='denari',
    version='1.0.12',
    description='DenariAnalytics OpenSouce Business and Tax Tools',
    author='Fadil Karim',
    author_email='insights@denarianalytics.com',
    packages=['TaxTools','NarcoAnalytics','Montana'],
    install_requires=[
        'pandas',
        'numpy',
        'plotly',
        'dash'
    ],
    package_data={
        'denari': ['UK Tax Tables/*.csv'],
        'denari': ['UK Tax Tables/2020-2021/*.csv'],
        'denari': ['UK Tax Tables/2021-2022/*.csv'],
        'denari': ['UK Tax Tables/2022-2023/*.csv'],
        'denari': ['UK Tax Tables/2023-2024/*.csv']
    }
)