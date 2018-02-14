%reset -f


########################################
####### How to use this function #######
########################################

# Run all code below the comment box that says "The Function"

# Search for the Airline you want reviews for at the URL below:
#   https://www.tripadvisor.com/Airlines

# Example 1:
# If you were to search for Delta Airlines, you would get the following URL:
# https://www.tripadvisor.com/Airline_Review-d8729060-Reviews-Cheap-Flights-Delta-Air-Lines#REVIEWS
# Notice that the URL above have two important parts:
#       a "dnumber": "d8729060"
#       a URL name: "Delta-Air-Lines"   

# Example 2:
# If you were to search for JetBlue, you would get the following URL:
# https://www.tripadvisor.com/Airline_Review-d8729099-Reviews-Cheap-Flights-JetBlue#REVIEWS
# Notice that the URL above have two important parts:
#       a "dnumber": "d8729099"
#       a URL name: "JetBlue"  

#!! Don't worry about whether or not the URL you received had "#REVIEWS" in it. It does not make a difference. !!

# Now, run the function, inputting the following arguments:
#   dnum: the dnumber from the URL. This will be a string. (Default = 'd8729060')
#   name: the URL name. This will be a string. (Default = 'Delta-Air-Lines')
#   num_rev: the number of reviews you want. Make sure this does not exceed the number that exists for that airline. This will be an integer. (Default = 10)
#   s1: the minimum number of seconds the crawler will wait before requesting the next page. This will be an integer. (Default = 8)
#   s2: the maximum number of seconds the crawler will wait before requesting the next page. This will be an integer. (Default = 15)
#   first_rev: the first review you want to scrape (Default = 1)

#The function will return a dataframe with the reviews. s1 = 8 and s2 = 15 is usually fine.


### Example 1 - 'Southwest Airlines' ###
# Search for 'Southwest Airlines' at the URL below:
#   https://www.tripadvisor.com/Airlines
# https://www.tripadvisor.com/Airline_Review-d8729156-Reviews-Cheap-Flights-Southwest-Airlines
Southwest = getReviews('d8729156','Southwest-Airlines')

### Example 2  - 'Air Asia - Thai AirAsia' ###
# Search for 'Air Asia - Thai AirAsia' at the URL below:
#   https://www.tripadvisor.com/Airlines
# https://www.tripadvisor.com/Airline_Review-d8728898-Reviews-Cheap-Flights-Air-Asia-Thai-AirAsia
ThaiAsia = getReviews('d8728898','Air-Asia-Thai-AirAsia',100,10,17,21)

# If you want to export your dataset to csv, simply write the following code:
import os
os.chdir('whatever_you_want_to_save_it') # Remember to include double backwards parens or single forward parens (i.e.)
ThaiAsia.to_csv('name_of_dataset.csv')

#################################################
########### You can do your work here ###########
#################################################

















####################################
########### The Function ###########
####################################
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep, time
from random import randint
from warnings import warn

def getReviews(dnum = 'd8729060', name = 'Delta-Air-Lines', num_rev = 10, s1 = 8, s2 = 15, first_rev = 1):
    ########################################################
    ########## Getting URLs for full-review pages ##########
    ########################################################
    begin_time = time()
    urls = []
    
    ###################
    arb_value = .1
    estimated_completion = ((s1 + s2) / 2 * 0.3 + (arb_value)) * num_rev    
    comp_hours = int(estimated_completion/3600)
    comp_minutes = int((estimated_completion - comp_hours*3600) / 60)
    comp_seconds = estimated_completion - comp_hours*3600 - comp_minutes*60
    est_completion = str(comp_hours) + ' hours, ' + str(comp_minutes) + ' minutes, and ' + str(comp_seconds) + ' seconds.'
    print('\n\nEstimated Completion Time: ' + est_completion)
    ###################
    
    pages = [str(i) for i in range(int(first_rev / 10), int( (first_rev + num_rev) / 10))]
    
    # Preparing the monitoring of the loop
    start_time = time()
    requests = 0
    
    # For every page in the interval found in pages
    for page in pages:
    
        # Make a get request
        if page == "0":
            response = get('https://www.tripadvisor.com/Airline_Review-' + dnum + '-Reviews-Cheap-Flights-' + name + '#REVIEWS')
        else:
            response = get('https://www.tripadvisor.com/Airline_Review-' + dnum + '-Reviews-Cheap-Flights-or' + page + '0-' + name + '#REVIEWS')
         # Pause the loop
        sleep(randint(int(s1),int(s2)))
    
        # Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print('Stage 1 Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    
        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Stage 1 Request: {}; Status code: {}'.format(requests, response.status_code))
    
        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')
    
        # Select all the 10 partial flight reviews from a single page
        url_containers = page_html.find_all('div', class_ = 'quote')
            
        for container in url_containers:
            # Scrape the url for the full flight reviews (each will have 5)
            url = container.a['href']
            urls.append(url)  
                
            
    #########################################################
    ########## Using URLs to retrieve full reviews ##########
    #########################################################        
    # Declaring the lists to store data in
    todays = []
    date_revs = []
    titles = []
    bodys = []
    seat_comforts = []
    cust_services = []
    cleanlinesss = []
    foods = []
    legrooms = []
    ents = []
    values = []
    check_ins = []
    
    
    
    # Getting urls for pages
    page_indices = [i for i in range(0,num_rev,5)]
    pages = []
    for page_num in page_indices:
        pages.append(urls[page_num])
    
    # Preparing the monitoring of the loop
    start_time = time()
    requests = 0
    j = -1
    
    # For every page in the interval found in pages
    for page in pages:
    
        # Make a get request
        response = get('https://www.tripadvisor.com' + page)
        
         # Pause the loop
        sleep(randint(int(s1),int(s2)))
    
        # Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print('Stage 2 Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    
        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Stage 2 Request: {}; Status code: {}'.format(requests, response.status_code))
    
        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')
    
        # Select all the 5 full flight reviews from a single page
        rev_containers = page_html.find_all('div', class_ = 'wrap')
        for i in range(len(rev_containers)):
            try:
                if len(rev_containers[i]["class"]) != 1:
                    del rev_containers[i];
            except:
                break
            
        for container in rev_containers:
    
            j += 1
            
            # Note the date data was scraped
            today = time()
            todays.append(today)
            
            # Scrape the date review was created
            date_rev = container.find('span', class_ = "ratingDate").text
            date_revs.append(date_rev)
    
            # Scrape the title
            title = container.find('div', class_ = 'quote').a.text
            titles.append(title)  
            
            # Scrape the body
            body = container.find('div', class_ = 'prw_rup').div.p.text
            bodys.append(body)
            
            ratings = container.find_all('li', class_ = 'recommend-answer')
            
            for rating in ratings:
    
                # Scrape the seat_comfort
                if rating.text == "Seat comfort":
                    seat_comfort = rating.div['class'][-1][-2]
                    seat_comforts.append(seat_comfort)
                
                # Scrape the cust_service
                elif rating.text == "Customer service (e.g. attitude, care, helpfulness)":
                    cust_service = rating.div['class'][-1][-2]
                    cust_services.append(cust_service)
                
                # Scrape the cleanliness
                elif rating.text == "Cleanliness":
                    cleanliness = rating.div['class'][-1][-2]
                    cleanlinesss.append(cleanliness)
                
                # Scrape the food
                elif rating.text == "Food and Beverage":
                    food = rating.div['class'][-1][-2]
                    foods.append(food)
    
                # Scrape the legroom
                elif rating.text == "Legroom":
                    legroom = rating.div['class'][-1][-2]
                    legrooms.append(legroom)
    
                # Scrape the ent
                elif rating.text == "In-flight entertainment (WiFi, TV, movies)":
                    ent = rating.div['class'][-1][-2]
                    ents.append(ent)
    
                # Scrape the value
                elif rating.text == "Value for money":
                    value = rating.div['class'][-1][-2]
                    values.append(value)
    
                # Scrape the check_in
                elif rating.text == "Check-in and Boarding (e.g. efficiency, service at gate)":
                    check_in = rating.div['class'][-1][-2]
                    check_ins.append(check_in)
    
            try:
                seat_comforts[j]
            except:
                seat_comforts += "N"
                
            try:
                cust_services[j]
            except:
                cust_services += "N"   
    
            try:
                cleanlinesss[j]
            except:
                cleanlinesss += "N"   
    
            try:
                foods[j]
            except:
                foods += "N"   
    
            try:
                legrooms[j]
            except:
                legrooms += "N"   
    
            try:
                ents[j]
            except:
                ents += "N"   
    
            try:
                values[j]
            except:
                values += "N"   
    
            try:
                check_ins[j]
            except:
                check_ins += "N"                
 
    Final = pd.DataFrame({
    "today": todays,
    "date_rev": date_revs,
    "title": titles,
    "body": bodys,
    "seat_comfort": seat_comforts,
    "cust_service": cust_services,
    "cleanliness": cleanlinesss,
    "food": foods,
    "legroom": legrooms,
    "ent": ents,
    "value": values,
    "check_in": check_ins      
    })     

    sleep(2)    
    
    e_time = time() - begin_time
    hours = int(e_time/3600)
    minutes = int((e_time - hours*3600) / 60)
    seconds = e_time - hours*3600 - minutes*60
    end_time = str(hours) + ' hours, ' + str(minutes) + ' minutes, and ' + str(seconds) + ' seconds.'
    print('\n\nCompleted in: ' + end_time)
    
    seconds_per_review = str(e_time / num_rev)
    print('\n\nSeconds per review: ' + seconds_per_review)
    
    print('\n\n' + name + ' is done!\n\n')
    
    return Final