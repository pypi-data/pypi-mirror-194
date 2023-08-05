from setuptools import setup, find_packages

setup(
    name='denari',
    version='1.0.6',
    description='DenariAnalytics open souce Business Tools',
    author='Fadil Karim',
    author_email='insights@denarianalytics.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'plotly',
        'dash'
    ],
)
