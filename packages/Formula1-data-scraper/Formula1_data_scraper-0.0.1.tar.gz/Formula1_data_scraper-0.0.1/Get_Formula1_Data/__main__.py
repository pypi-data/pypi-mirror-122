import pandas as pd
import sys

sys.path.insert(0, './Scraper')
import F1_drivers_and_times_data

sys.path.insert(0, './AWS_rds_uploader')
import RDS_engine





#creates the engine object which will be needed for the race data to be stored in an SQL database
#DATABASE_TYPE = 'postgresql'
#DBAPI = 'psycopg2'
#HOST = 'localhost'
#USER = 'postgres'
#password is censored out for the github repo
#PASSWORD = '****'
#DATABASE = 'qualifying_and_practice_data'
#PORT = 5432
#engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
print('This scraper can collect and store practice and2 qualifying data from the 2006 Formula 1 season and onwards')
a = int(input('What season would you like to start scraping data from: '))
b = int(input('What is the final season you would like to stop scraping data on: '))
b = b+1

engine_instance = RDS_engine.RDS_engine()
ENDPOINT = engine_instance.get_endpoint()
USER = engine_instance.get_username()
PASSWORD = engine_instance.get_password()
engine = engine_instance.engine_creation(ENDPOINT, USER, PASSWORD)

'''inclusively iterates through the 2006 to 2020 formula 1 seasons'''
for x in range (a,b):
    
    #loads season of interest
    f1_season = F1_drivers_and_times_data.F1_season(x)
    driver = f1_season.load_season_data()
    
    #gets the numbers of races in the season
    races_in_season = f1_season.number_of_races(driver)
    
    '''
    iterates through every race within the season where each race the data is stored in a dictionary and then covertred to a pandas data frame
    and then sotred in an sql data base
    '''
    for z in range(1,races_in_season):  
        
        #uses methods from the class to create a dictionary which contains the race data
        f1_season.load_race(z,driver)
        f1_season.load_qualifying(driver)
        race_stuff = f1_season.get_qualifying_data(driver)
        p_session = f1_season.get_practice_page(1,driver)
        f1_season.get_practice_data(race_stuff,p_session,driver)
        p_session = f1_season.get_practice_page(2,driver)
        f1_season.get_practice_data(race_stuff,p_session,driver)
        p_session = f1_season.get_practice_page(3,driver)
        f1_season.get_practice_data(race_stuff,p_session,driver)
        
        #converts the dictionary to a pandas data frame and then stores in into an postgreSQL database in AWS RDS where each table represents one race
        data_table = pd.DataFrame.from_dict(race_stuff)    
        data_table.to_sql('race_' + str(z) + '_' + str(x), engine, if_exists = 'replace')
        
    driver.quit()
