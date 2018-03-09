%reset -f

class scraper:
    
    def __init__(self):     

        """This class has only one function:
            scrape."""
        
    def scrape(self, page_first = 1, page_last = 5, year_first = 2013, year_last = 2017, print_labels = True):
        
        """Arguments:
            page_first (default val. = 1)
            page_last (default val. = 5)
            year_first (default val. = 2013)
            year_last (default val. = 2018)
            print_labels (default val. = True).
            
            page_first and page_last dictate
            which pages will be scraped for
            each year. 
            
            year_first and year_last dictate
            which years will be scraped.
            
            If print_labels is True, the function 
            will print the scraping progress."""
            
        from requests import get
        from bs4 import BeautifulSoup
        import pandas as pd
        from time import sleep, time
        from random import randint
        from warnings import warn   

        if print_labels == True:
            print('Scraping pages ' + str(page_first) + ' to ' + str(page_last)  + \
                  ' for years ' + str(year_first) + ' to ' + str(year_last) + '.\n\n')         
    
        pages = [str(i) for i in range(page_first, page_last + 1)]
        years_url = [str(i) for i in range(year_first, year_last + 1)]
                
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
            
            if print_labels == True:
                print('\nScraping year ' + year_url + '.\n')                         
                        
            # For every page in the interval found in pages
            for page in pages:
                
                if print_labels == True:
                    print('\nScraping page ' + page + ' for year ' + year_url + '.\n') 
                        
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
    
test = scraper()    

test.scrape(page_first = 1, page_last = 2, year_first = 2013, year_last = 2014)
