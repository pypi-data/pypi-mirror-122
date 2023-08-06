from setuptools import setup
from setuptools import find_packages

setup(
    name='Formula1_data_scraper',
    version='0.0.6',    
    description='Package that allows you to collect and store into an AWS postgreSQL RDS, the qualifying and practice data from any formula 1 race weekend from 2006 onwards',
    url='https://github.com/ishtyaq123/Webscraper_Formula_1_Practice_And_Qualifying_Data.git',
    author='Ishtyaq Nabi',
    license='MIT',
    packages=['Scraper','AWS_rds_uploader'],
    install_requires=['SQLAlchemy', 'psycopg2-binary', 'selenium', 'pandas'],
)
