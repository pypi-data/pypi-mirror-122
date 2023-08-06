'''
This script contains a class which creates an engine object which can store the f1 data into a database in the cloud.
The class uses AWS RDS as the service with the database type being POSTGRESQL
'''
from sqlalchemy import create_engine
import psycopg2
#creates the engine object which will be needed for the race data to be stored in an SQL database

class RDS_engine:
    '''
    This class creates the engine for the AWS RDS
        
        Attributes:
            DATABASE_TYPE (str): The type of database which is postgresql
            DBAPI (str): The type of api which is psycopg2
            DATABASE (str): Name of database which is postgres
            PORT (int): THe port for connecting which is 5432
    '''
    def __init__(self):
        self.DATABASE_TYPE = 'postgresql'
        self.DBAPI = 'psycopg2'
        self.DATABASE = 'postgres'
        self.PORT = 5432
        
    def get_endpoint(self): 
        '''
        This function asks the user and returns their endpoint of the database they want to connect to
            
            Returns:
                ENDPOINT (str): The endpoint of the users database

        '''
        print('What is the potgres AWS RDS endpoint you want to store your data in?')
        ENDPOINT = str(input('Enter your endpoint: '))
        return ENDPOINT
    
    def get_username(self):     
        '''
        This function asks the user and returns the username of the database they want to connect to
            
            Returns:
                USER (str): The username of the users database

        '''
        print('What is the username of your database?')
        USER = str(input('Enter your username: '))
        return USER

    def get_password(self):     
        '''
        This function asks the user and returns their password of the database they want to connect to
            
            Returns:
                PASSWORD (str): The password of the users database

        '''
        print('What is the password of your database?')
        PASSWORD = str(input('Enter your password: '))
        return PASSWORD

    def engine_creation(self, ENDPOINT, USER, PASSWORD):
        '''
        This function creates the engine for the AWS RDS
        
            Attributes:
                ENDPOINT (str): The endpoint of the users database
                USER (str): The username of the users database
                PASSWORD (str): The password of the users database
         '''           
        engine = create_engine(f"{self.DATABASE_TYPE}+{self.DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{self.PORT}/{self.DATABASE}")
        return engine