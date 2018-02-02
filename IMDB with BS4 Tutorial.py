%reset -f

from requests import get
from bs4 import BeautifulSoup
import pandas as pd

# We will scrape IMDB ratings for movies top 200 movies with the most votes
#   in each of the last five years.

url = 'http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'

response = get(url)
response.status_code
html_req = response.text
html_req[:500]

html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

movie_containers = html_soup.find_all('div', class_ = 'lister-item-content')
print(type(movie_containers))
print(len(movie_containers))

# We are now going to extract:
    # The name of the movie
    # The year of release
    # The IMDB rating
    # The Metascore rating
    # The number of votes

first_movie = movie_containers[0]
first_movie
type(first_movie)

# Name
first_movie.h3
first_movie.h3.a
first_movie.h3.a.text
first_movie_name = first_movie.h3.a.text

# Year
first_movie_year = first_movie.h3.find('span', class_ = 'lister-item-year')
first_movie_year
first_movie_year = first_movie.h3.find('span', class_ = 'lister-item-year').text
first_movie_year # this can also come as (2017)(I) or (2017)(V)
first_movie_year = int(first_movie_year[-5:-1])
first_movie_year

# IMDB Rating
first_movie.find('div', class_="ratings-bar").find('div', class_="inline-block ratings-imdb-rating").strong.text # The long way
first_movie_imdb = float(first_movie.strong.text) # We are lucky that this works

# Metascore
first_movie_metascore = int(first_movie.find('span', class_="metascore").text)
first_movie_metascore

# The number of votes
first_movie_votes = first_movie.find('span', attrs = {'name':'nv'})
first_movie_votes
first_movie_votes = first_movie.find('span', attrs = {'name':'nv'}).text
first_movie_votes
first_movie_votes.replace(",","")
int(first_movie_votes.replace(",",""))
first_movie_votes = int(first_movie.find('span', attrs = {'name':'nv'}).text.replace(",",""))
first_movie_votes
# OR
first_movie_votes = first_movie.find('span', attrs = {'name':'nv'})
first_movie_votes = first_movie_votes['data-value']
first_movie_votes
first_movie_votes = int(first_movie.find('span', attrs = {'name':'nv'})['data-value'])
first_movie_votes

# Some movies do not have a Metascore rating
twentieth_movie_mscore = movie_containers[19].find('span', class_ = 'metascore')
type(twentieth_movie_mscore)


names = []
years = []
years_fixed = []
imdb_ratings = []
metascores = []
votes = []

# Extract data from individual movie container
for container in movie_containers:

    # If the movie has Metascore, then extract:
    if container.find('div', class_ = 'ratings-metascore') is not None:

        # The name
        name = container.h3.a.text
        names.append(name)

        # The year        
        year = container.h3.find('span', class_ = 'lister-item-year').text
        years.append(year)
        
        # Convert year to year_fixed
        year_fixed = int(year[-5:-1])
        years_fixed.append(year_fixed)


        # The IMDB rating
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)

        # The Metascore
        m_score = int(container.find('span', class_ = 'metascore').text)
        metascores.append(m_score)

        # The number of votes
        vote = int(container.find('span', attrs = {'name':'nv'})['data-value'])
        votes.append(vote)
        
page_one = pd.DataFrame({
        "movie": names,
        "year": years,
        "year_fixed": years_fixed,
        'imdb': imdb_ratings,
        'metascore': metascores,
        'votes': votes        
})


# Now we are going to repeat the process for the first 4 pages (200 ratings)
#     for each of the last five years  
pages = [str(i) for i in range(1,5)]
years_url = [str(i) for i in range(2013,2018)]

# If we make get requests to the site too quickly, it will suspect that we are not normal
#   human browser and may block our IP address. We need to be wary of this. We will
#   use the sleep() method from the time library to mimic normal human browsing. 
from time import sleep, time
from random import randint

for i in range(0,5):
    print('Blah')
    sleep(randint(1,4))
    
start_time = time()
requests = 0

for _ in range(5):
    # A request would go here
    requests += 1
    sleep(randint(1,3))
    elapsed_time = time() - start_time
    print('Request: {}; Frequency: {} requests per second'.format(requests, requests/elapsed_time))  


# We will use the warn() method to identify any unsuccessful get request (status code != 200)    
from warnings import warn
warn("Warning Simulation")



# Finally,
    # This is our final script:
        
# Redeclaring the lists to store data in
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
                
    
five_years.info()