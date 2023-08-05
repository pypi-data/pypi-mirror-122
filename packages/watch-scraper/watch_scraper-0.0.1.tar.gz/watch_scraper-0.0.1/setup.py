from setuptools import setup
from setuptools import find_packages

setup(
    name='watch_scraper',
    version='0.0.1',
    description='Aicore project that allows the user to scrape mens watch data from the gold smiths website',
    author='Tafadzwa Zama',
    license='MIT',
    packages=find_packages(),
    install_requires=['selenium', 'tqdm', 'sqlalchemy', 'pandas', 'boto3', 'psycopg2'] 
)