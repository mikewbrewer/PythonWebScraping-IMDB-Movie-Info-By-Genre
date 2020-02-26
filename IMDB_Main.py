from time import time

from IMDB_ExtractData import extractDataFromIMDB
from IMDB_AddToSheets import addDataToSheets


if __name__ == '__main__':
    start_time = time()
    print ('\n\nExtracting Data From IMDB\n')
    extractDataFromIMDB()
    print ('\n\nAdding Data To Sheets\n')
    addDataToSheets()
    print ('\n\n- - Execution Time: ' + str(time() - start_time) + ' - -\n')
