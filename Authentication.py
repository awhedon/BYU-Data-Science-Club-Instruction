# LinkedIn

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from random import randint
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

br = webdriver.Chrome(r'C:\Users\alexa\Anaconda3\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe')
br.get("https://www.linkedin.com/m/login") 
br.switch_to_frame(br.find_element_by_tag_name("iframe"))

go_to_sign_in = br.find_element_by_class_name('sign-in-link')
go_to_sign_in.click()

email = br.find_element_by_id('session_key-login')
password = br.find_element_by_id("session_password-login")
email.send_keys("alexander.whedon@gmail.com")
password.send_keys("1Ajwguitar!")

login_attempt = br.find_element_by_xpath("//*[@type='submit']")
login_attempt.submit()

search = br.find_element_by_xpath('//input[@type="text"]')
search_submit = br.find_element_by_class_name('search-typeahead-v2__button')

search.send_keys('data science')
search_submit.click()

links = br.find_elements_by_class_name('search-result__result-link')
links[0].get_attribute('outerHTML')
links[0].click()
html = br.page_source
linkedin_soup = BeautifulSoup(html, 'html.parser')
name = linkedin_soup.find('h1',class_="pv-top-card-section__name").text
school = linkedin_soup.find('h3',class_="pv-entity__school-name").text

# Long way
search.send_keys('data science')
search_submit.click()
names = []
schools = []
for i in range(10):
    links = br.find_elements_by_class_name('search-result__result-link')
    print("The length of links is: " + str(len(links)))
    links[i].click()
    time.sleep(randint(5,8))
    html = br.page_source
    linkedin_soup = BeautifulSoup(html, 'html.parser')
    if linkedin_soup.find('h1',class_="pv-top-card-section__name") != None:
        name = linkedin_soup.find('h1',class_="pv-top-card-section__name").text
    else:
        name = "none"
        print("no name read")
    names.append(name)
    if linkedin_soup.find('h3',class_="pv-entity__school-name") != None:
        school = linkedin_soup.find('h3',class_="pv-entity__school-name").text    
    else:
        print("no school read")
        school = "none"
    schools.append(school)    
    search.send_keys('data science')
    search_submit.click()
    time.sleep(randint(3,5))  
    
# Short and better way
links_ = []
names2 = []
for link in links:
    linkHTML = link.get_attribute('outerHTML')
    link_ = "https://www.linkedin.com" + BeautifulSoup(linkHTML, 'html.parser').find('a')['href']
    links_.append(link_)
    if BeautifulSoup(linkHTML, 'html.parser').find('span', class_="actor-name") != None:
        name2 = BeautifulSoup(linkHTML, 'html.parser').find('span', class_="actor-name").text
        names2.append(name2)
html = br.page_source
links = BeautifulSoup(html, 'html.parser').find_all('a','search-result__result-link')
len(links)  
names2

links2 = list(set(links_))
    
linkedin_profiles = pd.DataFrame({
        "Name": names,
        "School": schools
        })


