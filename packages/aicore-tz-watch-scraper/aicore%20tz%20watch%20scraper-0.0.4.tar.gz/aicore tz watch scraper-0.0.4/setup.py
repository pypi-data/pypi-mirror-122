from setuptools import setup
from setuptools import find_packages

setup(
    name='aicore tz watch scraper',
    version='0.0.4',
    description='Aicore project that allows the user to scrape mens watch data from the gold smiths website',
    url='https://github.com/CrownedDev56',
    author='Tafadzwa Zama',
    license='MIT',
    packages=find_packages(),
    install_requires=['selenium', 'tqdm', 'sql', 'sqlalchemy', 'pandas', 'boto3','psycopg2','sqlalchemy','dataclasses'] 

)