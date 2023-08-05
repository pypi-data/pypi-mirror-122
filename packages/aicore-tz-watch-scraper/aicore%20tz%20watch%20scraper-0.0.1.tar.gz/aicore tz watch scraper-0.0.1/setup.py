from setuptools import setup
from setuptools import find_packages

setup(
    name='aicore tz watch scraper',
    version='0.0.1',
    description='Aicore project that allows the user to scrape mens watch data from the gold smiths website',
    url='https://github.com/CrownedDev56',
    Author='Tafadzwa Zama',
    license='MIT',
    Packages=find_packages(),
    install_requires=['selenium', 'tqdm', 'sql', 'sqlalchemy', 'pandas'] 

)