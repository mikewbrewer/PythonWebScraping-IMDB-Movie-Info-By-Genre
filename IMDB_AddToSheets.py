import gspread
import pandas
import math
import re

from time import sleep, time
from datetime import date
from oauth2client.service_account import ServiceAccountCredentials


_year_counts = {}
_runtime_averages = {}
_ratings = {}
_metascores = {}

_ratedMA = {}
_ratedR = {}
_ratedPG13 = {}
_ratedPG = {}
_ratedG = {}
_ratedOther = {}
_notRated = {}



scope = ["https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"]

# connect to google sheets
creds = ServiceAccountCredentials.from_json_keyfile_name("Google_Credentials.json", scope)
client = gspread.authorize(creds)

sh = client.open_by_url('https://docs.google.com/spreadsheets/d/1amCmLz-IIiWRV2hp5VBB2qIOAwoWHz_R8Rx9xMjfPHM/edit#gid=0')


def analyseData(worksheet_index):
    print ('Analyzing Data...')
    global sh

    global _year_counts
    global _runtime_averages
    global _ratings
    global _metascores

    global _ratedMA
    global _ratedR
    global _ratedPG13
    global _ratedPG
    global _ratedG
    global _ratedOther
    global _notRated

    row_index = 2
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

    client.login()
    worksheet = sh.get_worksheet(worksheet_index)

    #print (_year_counts)
    for year in _year_counts:
        new_row = []
        new_row.append(year)

        sleep(2)

        # total movies by year
        if year in _runtime_averages:
            new_row.append(str(round(_year_counts[year], 2)))
        else:
            new_row.append('-')

        # runtime_averages
        if year in _runtime_averages:
            new_row.append(str(round(_runtime_averages[year] / _year_counts[year], 2)))
        else:
            new_row.append('-')

        # ratings
        if year in _ratings:
            new_row.append(str(round(_ratings[year] / _year_counts[year], 2)))
        else:
            new_row.append('-')

        # metascores
        if year in _metascores:
            new_row.append(str(round(_metascores[year] / _year_counts[year], 2)))
        else:
            new_row.append('-')

        # Rated MA
        if year in _ratedMA:
            new_row.append(str(_ratedMA[year]))
        else:
            new_row.append('-')

        # Rated R
        if year in _ratedR:
            new_row.append(str(_ratedR[year]))
        else:
            new_row.append('-')

        # Rated PG-13
        if year in _ratedPG13:
            new_row.append(str(_ratedPG13[year]))
        else:
            new_row.append('-')

        # Rated PG
        if year in _ratedPG:
            new_row.append(str(_ratedPG[year]))
        else:
            new_row.append('-')

        # Rated G
        if year in _ratedG:
            new_row.append(str(_ratedG[year]))
        else:
            new_row.append('-')

        # Not Rated
        if year in _notRated:
            new_row.append(str(_notRated[year]))
        else:
            new_row.append('-')

        # Rated other
        if year in _ratedOther:
            new_row.append(str(_ratedOther[year]))
        else:
            new_row.append('-')

        worksheet.append_row(new_row, 2)





def addDataToSheets():
    global _year_counts
    global _runtime_averages
    global _ratings
    global _metascores

    global _ratedMA
    global _ratedR
    global _ratedPG13
    global _ratedPG
    global _ratedG
    global _ratedOther
    global _notRated


    csv_files = ['CSVs/action.csv', 'CSVs/adventure.csv', 'CSVs/animation.csv', 'CSVs/biography.csv', 'CSVs/comedy.csv', 'CSVs/crime.csv', 'CSVs/documentary.csv', 'CSVs/drama.csv', 'CSVs/family.csv', 'CSVs/fantasy.csv', 'CSVs/film-noir.csv', 'CSVs/history.csv', 'CSVs/horror.csv', 'CSVs/music.csv', 'CSVs/musical.csv', 'CSVs/mystery.csv', 'CSVs/romance.csv', 'CSVs/sci-fi.csv', 'CSVs/sport.csv', 'CSVs/thriller.csv', 'CSVs/war.csv', 'CSVs/western.csv']


    total_movies = 0
    sheet_num = 1

    for input_file in csv_files:
        df = pandas.read_csv(input_file)
        print ('Reading: ' + input_file)

        _year_counts = {}
        _runtime_averages = {}
        _ratings = {}
        _metascores = {}

        _ratedMA = {}
        _ratedR = {}
        _ratedPG13 = {}
        _ratedPG = {}
        _ratedG = {}
        _notRated = {}
        _ratedOther = {}


        for index, row in df.iterrows():
            total_movies += 1

            if not (re.search("^[1-2][0-9][0-9][0-9]", str(row['Release Year']))):
                #print ('pass option 1')
                pass
            elif math.isnan(float(row['Release Year'])):
                #print ("pass option 2")
                pass
            else:
                year = str(int(row['Release Year']))

                # year dictionary
                if year in _year_counts:
                    if not(year == ''):
                        _year_counts[year] += 1
                else:
                    if not(year == ''):
                        _year_counts[year] = 1

                # metascore dictionary
                if year in _metascores:
                    if not(row['Metascore'] == ''):
                        if not(math.isnan(row['Metascore'])):
                            _metascores[year] += int(row['Metascore'])
                else:
                    if not(row['Metascore'] == ''):
                        if not(math.isnan(row['Metascore'])):
                            _metascores[year] = int(row['Metascore'])

                # ratings dictionary
                if year in _ratings:
                    if not(row['Rating'] == ''):
                        if not(math.isnan(row['Rating'])):
                            _ratings[year] += int(row['Rating'])
                else:
                    if not(row['Rating'] == ''):
                        if not(math.isnan(row['Rating'])):
                            _ratings[year] = int(row['Rating'])

                # runtime_averages dictionary
                if year in _runtime_averages:
                    if not(row['Runtime'] == ''):
                        temp_ = row['Runtime']
                        if isinstance(temp_, str):
                            temp_ = temp_.replace(',', '')
                        if not(math.isnan(float(temp_))):
                            _runtime_averages[year] += int(temp_)
                else:
                    if not(row['Runtime'] == ''):
                        if not(math.isnan(float(row['Runtime']))):
                            _runtime_averages[year] = int(row['Runtime'])

                # certification dictionary
                if not(row['Certification'] == ''):
                    # rated MA
                    if row['Certification'] == 'TV-MA' or row['Certification'] == 'X' or row['Certification'] == 'M' or row['Certification'] == 'AO':
                        if not(year in _ratedMA):
                            _ratedMA[year] = 1
                        else:
                            _ratedMA[year] += 1
                    # rated R
                    elif row['Certification'] == 'R' or row['Certification'] == 'NC-17' or row['Certification'] == 'C':
                        if not(year in _ratedR):
                            _ratedR[year] = 1
                        else:
                            _ratedR[year] += 1
                    # rated pg-13
                    elif row['Certification'] == 'PG-13':
                        if not(year in _ratedPG13):
                            _ratedPG13[year] = 1
                        else:
                            _ratedPG13[year] += 1
                    # rated PG
                    elif row['Certification'] == 'PG' or row['Certification'] == 'TV-PG':
                        if not(year in _ratedPG):
                            _ratedPG[year] = 1
                        else:
                            _ratedPG[year] += 1
                    # rated G
                    elif row['Certification'] == 'G' or row['Certification'] == 'TV-G':
                        if not(year in _ratedG):
                            _ratedG[year] = 1
                        else:
                            _ratedG[year] += 1
                    # rated Not Rated
                    elif row['Certification'] == 'Not Rated':
                        if not(year in _notRated):
                            _notRated[year] = 1
                        else:
                            _notRated[year] += 1
                    else:
                        if not(year in _ratedOther):
                            _ratedOther[year] = 1
                        else:
                            _ratedOther[year] += 1

        analyseData(sheet_num)
        sheet_num += 1




if __name__ == '__main__':
    start_time = time()
    addDataToSheets()
    print ('- - Execution Time: ' + str(time() - start_time) + ' - -')
