import requests
import pandas

from time import sleep
from random import randint
from bs4 import BeautifulSoup

# Global variables
_genre_list = ['action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 'documentary', 'drama', 'family', 'fantasy', 'film-noir', 'history', 'horror', 'music', 'musical', 'mystery', 'romance', 'sci-fi', 'sport', 'thriller', 'war', 'western']

_movie_titles = []
_movie_certifications = []
_movie_runtimes = []
_movie_ratings = []
_movie_release_years = []
_movie_metascores = []


# reset everything for next genre, this is to be done after each genre is done
def resetArrays():
    print ('resetting arrays...')
    _movie_titles.clear()
    _movie_certifications.clear()
    _movie_runtimes.clear()
    _movie_ratings.clear()
    _movie_release_years.clear()
    _movie_metascores.clear()


# function: strips relevant data from the html object and returns a new Movie object with the info inputed.
def stripInfo(movie):
    title = movie.find(class_='lister-item-header')
    if title == None:
        title = ''
    else:
        title = title.a.get_text()

    year = movie.find(class_='lister-item-year text-muted unbold')
    if (year == None):
        year = ''
    else:
        year = year.get_text()[-5:-1]

    rating = movie.find(class_='inline-block ratings-imdb-rating')
    if (rating == None):
        rating = ''
    else:
        rating = rating.get_text().strip()

    cert = movie.find(class_='certificate')
    if (cert == None):
        cert = ''
    else:
        cert = cert.get_text()

    rtime = movie.find(class_='runtime')
    if (rtime == None):
        rtime = ''
    else:
        rtime = rtime.get_text().split()[0]

    metascore = movie.find(class_='inline-block ratings-metascore')
    if (metascore == None):
        metascore = ''
    else:
        metascore = metascore.get_text().split()[0]

    _movie_titles.append(title)
    _movie_certifications.append(cert)
    _movie_runtimes.append(rtime)
    _movie_ratings.append(rating)
    _movie_release_years.append(year)
    _movie_metascores.append(metascore)



# sets and returns the correct url to be used based on the genre and movie numbers
def getUrl(movie_count, genre):
    if (genre == 'documentary'):
        return ('https://www.imdb.com/search/title/?genres=documentary&start=' + str(movie_count) + '&explore=genres&ref_=adv_nxt')
    else:
        return ('https://www.imdb.com/search/title/?title_type=feature&genres=' + genre + '&start=' + str(movie_count) + '&explore=genres&ref_=adv_nxt')



# find and calculate the number of pages to iterate through based on the number of films in the list
def setMovieCountTotals(g):
    url_temp = getUrl(1, g)
    page = requests.get(url_temp)
    soup = BeautifulSoup(page.content, 'html.parser')
    temp = soup.find(class_='desc')

    temp = temp.span.get_text().split()[2]
    temp = temp.replace(',', '')
    print ('total movies: ' + temp)
    return int(temp)



# export the final csv file
def exportToCSV(filename):
    output_data = pandas.DataFrame(
        {
        'Movie Title': _movie_titles,
        'Certification': _movie_certifications,
        'Runtime': _movie_runtimes,
        'Rating': _movie_ratings,
        'Release Year': _movie_release_years,
        'Metascore': _movie_metascores
        })

    output_data.to_csv(filename)



# function: the main driving function of this whole thing. The loop iterates over various pages by genre and inputs the movies into different arrays by genre.
def extractDataFromIMDB():
    upper_limit = 10000
    for genre in _genre_list:
        print ('genre: ' + genre)

        movie_total_count = setMovieCountTotals(genre)
        num_pages = int(movie_total_count / 50)
        print ('num_pages: ' + str(num_pages))

        movie_count = 1

        for page in range(0, num_pages):
            url = getUrl(movie_count, genre)

            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            movies_list = soup.find(class_='article')
            movies_array = movies_list.findAll('div', {'class': 'lister-item mode-advanced'})

            for movie in movies_array:
                stripInfo(movie)

            if (movie_count < upper_limit):
                movie_count += 50
            else:
                break

        exportToCSV(genre + '.csv')
        resetArrays()



if __name__ == '__main__':
    extractDataFromIMDB()
