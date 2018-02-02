%reset -f

from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep, time
from random import randint
from warnings import warn

pages = [str(i) for i in range(1,5)]
years_url = [str(i) for i in range(2013,2018)]
        
# Declaring the lists to store data in
names = []
years = []
years_fixed = []
imdb_ratings = []
metascores = []
votes = []

# Preparing the monitoring of the loop
start_time = time()
requests = 0

# For every year in the interval found in years_url
for year_url in years_url:

    # For every page in the interval found in pages
    for page in pages:

        # Make a get request
        response = get('http://www.imdb.com/search/title?release_date=' + year_url + \
                       '&sort=num_votes,desc&page=' + page)

        # Pause the loop
        sleep(randint(8,15))

        # Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if requests > 20:
            warn('Number of requests was greater than expected.')  
            break 

        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')

        # Select all the 50 movie containers from a single page
        mv_containers = page_html.find_all('div', class_ = 'lister-item-content')

        # For every movie of these 50
        for container in mv_containers:
            # If the movie has a Metascore, then:
            if container.find('span', class_ = 'metascore') is not None:

                # Scrape the name
                name = container.h3.a.text
                names.append(name)

                # Scrape the year        
                year = container.h3.find('span', class_ = 'lister-item-year').text
                years.append(year)
        
                # Convert year to year_fixed
                year_fixed = int(year[-5:-1])
                years_fixed.append(year_fixed)

                # Scrape the IMDB rating
                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

                # Scrape the Metascore
                m_score = int(container.find('span', class_ = 'metascore').text)
                metascores.append(m_score)

                # Scrape the number of votes
                vote = int(container.find('span', attrs = {'name':'nv'})['data-value'])
                votes.append(vote)          
                
five_years = pd.DataFrame({
        "movie": names,
        "year": years,
        "year_fixed": years_fixed,
        'imdb': imdb_ratings,
        'metascore': metascores,
        'votes': votes        
})