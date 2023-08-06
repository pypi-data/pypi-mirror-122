'''
This script contains a class which can scrape qualifying and practice data for the 2006 to 2021 formula 1 seasons.
'''
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import time

class F1_season():

    ''' 
    This class is used to scrape the qualifying and practice data for a season of intetrest 
    
    Attributes:
        year (int): The year of the formula 1 season to be scraped from 
    '''
    def __init__(self,year):
        self.year=year
    
    def load_season_data(self):
        ''' 
        This method loads the formula 1 race results page for the intended season with the attribute from an intance of the class using selenium webdriver
        
        Returns:
            driver: The selenium web driver onject
        '''
        #driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME)
        #driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME, options = Options().add_argument('--headless'))   
        driver = webdriver.Chrome()
        current_year = self.year
        URL = 'https://www.formula1.com/en/results.html/' + str(current_year) + '/races.html'
        driver.maximize_window()
        driver.get(URL)
        time.sleep(1)
        
        #gets rid of the cookies that pops up with each new webdriver
        driver.find_element_by_xpath('//*[@id="truste-consent-button"]').click()
        
        time.sleep(1)
        return driver
    
    def number_of_races(self,web):   
        '''
        Function gets the number of races within the current f1 season

        Args:
            web (driver): The selenium web driver object

        Returns:
            races (int): The number of races within the season
        '''
        #finds the container with the races and gets its total length for the number of races
        race_container = web.find_element_by_xpath('/html/body/div[2]/main/article/div/div[2]/div[1]/div[3]/ul')
        races = len(race_container.find_elements_by_xpath('./li'))
        
        return races   

    def load_race(self,race_number,web):
        '''
        Function gets the data for the race weekend of interest and creates a dictionary for it so data can be stored

        Args:
            race_number (int): The race of inteterest within the season
            web (driver): The selenium web driver object
        '''
        web.find_element_by_xpath('/html/body/div[2]/main/article/div/div[2]/div[1]/div[3]/ul/li[' + str(race_number + 1) + ']').click()
        time.sleep(1)

    def load_qualifying(self,web):
        '''
        Function clicks onto the page with the qualifying data
        
        Args:
            web (driver): The selenium web driver object        
        ''' 
        time.sleep(3)
        web.find_element_by_xpath('/html/body/div[2]/main/article/div/div[2]/div[2]/div[2]/div[1]/ul/li[6]').click()
    
    def __qualifying_drivers(self,web):
        '''
        Function gets the total number of drivers within the qualifying session
        
        Args:
            web (driver): The selenium web driver object

        Returns:
            total_drivers: The number of drivers within qualifying
        
        '''

        time.sleep(3)
    
        #finds the container which contains all the drivers in qualifying
        drivers_qualifying = web.find_element_by_xpath('/html/body/div[2]/main/article/div/div[2]/div[2]/div[2]/div[2]/table/tbody')
        
        total_drivers = len(drivers_qualifying.find_elements_by_xpath('./tr'))
        return total_drivers

    
    
    def get_qualifying_data(self,web): 
        '''
        Function gets the qualifying data from the qualifying page and appends it to a dictionary

        Args:
            web (driver): The selenium web driver object 

        Returns:
            race_info (dictionary): Contains all the qualifying data from the race weekend

        '''

        time.sleep(1)
        total_drivers = self.__qualifying_drivers(web)
        time.sleep(2)
        
        #creates a dictionary for all the race data to be stored
        race_info = {'Overall Qualifying Result': [], 'Driver': [], 'Car': [], 'Q3 Lap Time': [], 'Q2 Lap Time': [], 'Q1 Lap Time': [], 'P3 Lap Time': [], 'P2 Lap Time': [], 'P1 Lap Time': []}
        
        time.sleep(3)
        
        for i in range (1,total_drivers + 1):
            
            #appends the driver, car and the associated overall qualifying result
            qualifying_result = web.find_element_by_xpath('/html/body/div[2]/main/article/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/td[2]').text
            race_info['Overall Qualifying Result'].append(qualifying_result)
            race_driver = web.find_element_by_xpath('/html/body/div[2]/main/article/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/td[4]').text
            race_info['Driver'].append(race_driver)
            car = web.find_element_by_xpath('/html/body/div[2]/main/article/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/td[5]').text
            race_info['Car'].append(car)
            
            q3 = web.find_element_by_xpath('/html/body/div[2]/main/article/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/td[8]').text        

            #converting the laptime strings into numerical floats
            if len(q3) == 8:
                minute_conversion = float(q3.split(':').pop(0))*60
                seconds = round(float(q3.split(':').pop(1)) + minute_conversion, 3)
                race_info['Q3 Lap Time'].append(seconds)            
            elif len(q3) == 6:
                seconds = float(q3)
                race_info['Q3 Lap Time'].append(seconds)     
            else:
                race_info['Q3 Lap Time'].append(q3)  

            q2 = web.find_element_by_xpath('/html/body/div[2]/main/article/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/td[7]').text     

            if len(q2) == 8:
                minute_conversion = float(q2.split(':').pop(0))*60
                seconds = round(float(q2.split(':').pop(1)) + minute_conversion, 3)
                race_info['Q2 Lap Time'].append(seconds)            
            elif len(q2) == 6:
                seconds = float(q2)
                race_info['Q2 Lap Time'].append(seconds)     
            else:
                race_info['Q2 Lap Time'].append(q2)

            q1 = web.find_element_by_xpath('/html/body/div[2]/main/article/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/td[6]').text     

            if len(q1) == 8:
                minute_conversion = float(q1.split(':').pop(0))*60
                seconds = round(float(q1.split(':').pop(1)) + minute_conversion, 3)
                race_info['Q1 Lap Time'].append(seconds)

            elif len(q1) == 6:
                seconds = float(q1)
                race_info['Q1 Lap Time'].append(seconds)     

            else:
                race_info['Q1 Lap Time'].append(q1)

            race_info['P1 Lap Time'].append(None)
            race_info['P2 Lap Time'].append(None)
            race_info['P3 Lap Time'].append(None)

        time.sleep(1)  
        return race_info    
    
    def get_practice_page(self,session,web):
        '''
        Function finds the intended page of practice by putting in a number from 1-3

        Args:
            session (int): Refers to the practice session
            web (driver):  The selenium web driver object 

        Returns:
            pratice_session (none): This is retuned if the target practice session didnt happen within the race weekend
            or
            p (string): This is the name of the target practice session if it exists
        '''

        self.session = session
        time.sleep(5)

        #try and except statements used as practice sessions have been cancelled in the past so in the case one is not available the practice times will remain empty in the table
        try:
            practice_session = web.find_element_by_xpath('/html/body/div[2]/main/article/div/div[2]/div[2]/div[2]/div[1]/ul/li[' + str(6 + self.session) + ']').text
            web.find_element_by_xpath('/html/body/div[2]/main/article/div/div[2]/div[2]/div[2]/div[1]/ul/li[' + str(6 + self.session) + ']').click()
        except:
            print('session doesent exist')
            practice_session = None   
            return practice_session
        if practice_session == 'PRACTICE 3':
            p = 'P3 Lap Time'
            return p
        elif practice_session == 'PRACTICE 2':
            p = 'P2 Lap Time'
            return p
        elif practice_session == 'PRACTICE 1':
            p = 'P1 Lap Time'    
            return p

        time.sleep(2)

    def get_practice_data(self,data,page,web):
        '''
        Function gets and appends the practice data from the intended practice page session into the dictionary created in the "get_qualifying_data" function
         
         Args:
            data (dictionary): The dictionary created in the "get_qualifying_data" function where the practice data of the intended session will be stored
            page ((none) or (string)): The result produced from the "get_practice_page" function
            web (driver):  The selenium web driver object 
        '''
        time.sleep(5)
        self.data = data
        self.page = page
        if self.page == None:
            print("page does not exist")

        else:

            practice_container = web.find_element_by_xpath('/html/body/div[2]/main/article/div/div[2]/div[2]/div[2]/div[2]/table/tbody')
            practice_drivers = practice_container.find_elements_by_xpath('./tr')

            for j in range (1,len(practice_drivers) + 1):

                #needed to store the practice lap time with the associated driver
                c = web.find_element_by_xpath('/html/body/div[2]/main/article/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[' + str(j) + ']/td[4]').text
                a = web.find_element_by_xpath('/html/body/div[2]/main/article/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr['+ str(j) +']/td[6]').text

                if len(a) == 8:
                    minute_conversion = float(a.split(':').pop(0))*60
                    a = round(float(a.split(':').pop(1)) + minute_conversion, 3)

                elif len(a) == 6:
                    a = float(a)

                try:
                    index = self.data['Driver'].index(c)
                    self.data[self.page][index] = a
                except:
                    print('driver not found')
        time.sleep(2)          