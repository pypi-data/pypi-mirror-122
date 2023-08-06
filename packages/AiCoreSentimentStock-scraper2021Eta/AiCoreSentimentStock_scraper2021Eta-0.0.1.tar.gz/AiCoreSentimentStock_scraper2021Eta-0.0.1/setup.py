from os import path
from setuptools import setup
from setuptools import find_packages


setup(
    name='AiCoreSentimentStock_scraper2021Eta', ## This will be the name your package will be published with
    version='0.0.1', 
    description='scraping stock data',
    #url='https://github.com/IvanYingX/project_structure_pypi.git', # Add the URL of your github repo if published 
                                                                   # in GitHub
    author='Tamim Ehsan', # Your name
    license='MIT',
    
    packages=find_packages(), # This one is important to explain. See the notebook for a detailed explanation
    install_requires=['beautifulsoup4==4.9.3','bs4==0.0.1','certifi==2021.5.30','charset-normalizer==2.0.4','colorama==0.4.4','greenlet==1.1.1','idna==3.2','lxml==4.6.3','numpy==1.21.2','pandas==1.3.2','psycopg2==2.9.1','python-dateutil==2.8.2','pytz==2021.1','requests==2.26.0','six==1.16.0','soupsieve==2.2.1','SQLAlchemy==1.4.23','tqdm==4.62.2','urllib3==1.26.6','vaderSentiment==3.3.2'], # For this project we are using two external libraries
                                                     # Make sure to include all external libraries in this argument
)