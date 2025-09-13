import sqlite3
import copy
from LinearRegression import dateConversion
'''
Sometimes some stocks do not have a dividend. In this case the value of zero will 
be entered into the table instead for its dividend value at all the dates. These stocks
are AMD and amazon
'''

filePath = "C:/Users/2441/Computer Science NEA code/"

conn = sqlite3.connect(filePath + "Stock Database")

c = conn.cursor()

nasdaqFilePath = filePath + "Nasdaq.csv"

appleFilePath = filePath + "AAPL.csv"
amdFilePath = filePath + "AMD.csv"
amazonFilePath = filePath + "AMZN.csv"
intelFilePath = filePath + "INTC.csv"
microsoftFilePath = filePath + "MSFT.csv"
nvidiaFilePath = filePath + "NVDA (2).csv"


nvidiaDividendFilePath = filePath + "NVDA.Dividend.csv"
appleDividendFilePath = filePath + "AAPL.Dividend.csv"
microsoftDividendFilePath = filePath + "MSFT.Dividend.csv"
intelDividendFilePath = filePath + "INTC.Dividend.csv"

nasdaqFile = open(nasdaqFilePath, "r", encoding="utf8")

appleFile = open(appleFilePath, "r", encoding="utf8")
amdFile = open(amdFilePath, "r", encoding="utf8")
amazonFile = open(amazonFilePath, "r", encoding="utf8")
intelFile = open(intelFilePath, "r", encoding="utf8")
microsoftFile = open(microsoftFilePath, "r", encoding="utf8")
nvidiaFile = open(nvidiaFilePath, "r", encoding="utf8")

nvidiaDividendFile = open(nvidiaDividendFilePath, "r", encoding ="utf8")
appleDividendFile = open(appleDividendFilePath, "r", encoding="utf8")
microsoftDividendFile = open(microsoftDividendFilePath, "r", encoding="utf8")
intelDividendFile = open(intelDividendFilePath, "r", encoding="utf8")


firstDate = "2019-09-05"
lastDate = "2024-09-04"

def dateProcessing(date):
    '''
    This takes a date as an input then returns the next date chronologically
    :param date: string
        The string of a date in the format "yyyy-mm-dd"
    :return nextDate: string
        The string of the day after the date that was passed in, in the format "yyyy-mm-dd"
    '''
    # The following if statements check if it is the last date of the month, if so the month value must be increased by one and the day value set to 1.
    if date[5:] == "01-31":
        nextDate = date[:4] + "-02-01"
    elif date[5:] == "02-29" and int(date[:4]) % 4 == 0:
        nextDate = date[:4] + "-03-01"
    elif date[5:] == "02-28" and int(date[:4]) % 4 != 0:
        nextDate = date[:4] + "-03-01"
    elif date[5:] == "03-31":
        nextDate = date[:4] + "-04-01"
    elif date[5:] == "04-30":
        nextDate = date[:4] + "-05-01"
    elif date[5:] == "05-31":
        nextDate = date[:4] + "-06-01"
    elif date[5:] == "06-30":
        nextDate = date[:4] + "-07-01"
    elif date[5:] == "07-31":
        nextDate = date[:4] + "-08-01"
    elif date[5:] == "08-31":
        nextDate = date[:4] + "-09-01"
    elif date[5:] == "09-30":
        nextDate = date[:4] + "-10-01"
    elif date[5:] == "10-31":
        nextDate = date[:4] + "-11-01"
    elif date[5:] == "11-30":
        nextDate = date[:4] + "-12-01"
    elif date[5:] == "12-31":  # This if statement checks if the day is the last day of the year, if it is the year value is increased by one and the day and month value is set to 1
        nextYear = int(date[:4]) + 1
        nextDate = str(nextYear) + "-01-01"
    else:  #If it isn't the last day of the month or day of the year then only the day value is increased by one.
        nextDate = date[0:8]
        nextDay = int(date[8:10]) + 1
        if nextDay <= 9:  # If the next day is not 10 or more then the day value must have a 0 in front of it to keep the date in the correct format
            nextDay = "0" + str(nextDay)
        else:
            nextDay = str(nextDay)
        nextDate += nextDay  # The day is always the last part of the string therefore the day can be appended to the end of the string
    return(nextDate)


# For different stocks you need to change the index ID and the index name and the stock name and the stock ID. The rest of it the program does for you. You also need to change the files used.
# To input data you must then call these functions with the correct values inputted

def stockInsertion(stockID, indexID, stockName):
    '''
    This procedure puts values into the stock table of the database for StockID, stock name and IndexID
    :param stockID: int
        The stockID as an integer
    :param indexID: int
        The indexID as an integer
    :param stockName: string
        The name of the stock that is having its values put in the table
    '''
    c.execute('''INSERT INTO Stock (StockID, StockName, IndexID)
                VALUES (?, ?, ?);''', (stockID, stockName, indexID))
    conn.commit()

def indexInsertion(indexID, indexName):
    '''
    This procedure puts values into the indexTable table of the database for IndexID and Index Name
    :param indexID: int
        The indexID as an integer
    :param indexName:
        The name of the index that is having its values put in the table
    '''
    c.execute('''INSERT INTO IndexTable (IndexId, IndexName)
                VALUES (?, ?);''', (indexID, indexName))
    conn.commit()


def indexValuesInsertion(file, indexID, firstDate, lastDate):
    '''
    This procedure puts values into the indexValues table of the database for IndexID, date and index closing price.
    Data processing is done here which is discussed at the bottom of the file.
    :param file: string
        This is the csv file containing the data
    :param indexID: int
        The indexID as an integer
    :param firstDate: string
        This is the start date that data was collected from, needed for data processing
    :param lastDate: string
        This is the last date that data was collected from, needed for data processing
    '''
    start = True  # This variable denotes if it is the first line containing data in the file.
    first = True  # This variable denotes if it is the first line in the csv file. This just contains column headings
    previousList = []
    for i in file:  # This iterates through every line in the csv file which contains the data
        if first != True:  # If it is the first, then you don't put something into the database as the first line is not full of data, it is the column titles
            i = i.strip("\n")
            list = i.split(",")
            valuesStartDate = list[0]  # Values start date will be the value that data points have their date starting at.
            if start == True and list[0] != firstDate:  # If the first data point doesnt have the same date value as the first date needed
                # then this if statement is entered
                list[0] = firstDate  # The date is then set to be equal to the first date that data is needed for and data is entered into the database
                # for this date but the values used are for the first date that we have values for
                c.execute('''INSERT INTO IndexValues (IndexID, Date, IndexClosingPrice)
                                                   VALUES (?, ?, ?);''', (indexID, list[0], list[4]))
                while list[0] != valuesStartDate:  # This while loop inserts data into the tables for all the dates that do
                    # not have values up until the first date with values in the csv file. It increases the date using date processing,
                    # inserting values into the database. The values other than date will all be the same as the values for the first
                    # data point in the csv file.
                    nextDate = dateProcessing(list[0])
                    list[0] = nextDate  # The new increased date values is put into the list
                    if list[0] != valuesStartDate:
                        c.execute('''INSERT INTO IndexValues (IndexID, Date, IndexClosingPrice)
                                                           VALUES (?, ?, ?);''', (indexID, list[0], list[4]))
            if start != True:  # If it is not the first value in the list then we can work out what the date we should now be on.
                # This is by using the previous data points date and checking what the next date is chronologically.
                nextDate = dateProcessing(previousList[0])
            else:  # If it is the first value in the list then there will be no previous list, therefore we don't
                # have a value for what the date "should be", therefore next date is set to no
                nextDate = "No"

            if nextDate == list[0] or start == True:  # If we either have chronologically increased date by one from the last insertion
                # or if we are using the first data point then value are inserted into the list as normal. We know by this point that
                # the first data point is on the next chronological date as the previous dates have already been added and if next date
                # is equal to the date in the list then we are on the next chronological date therefore the value can be inserted normally
                c.execute('''INSERT INTO IndexValues (IndexID, Date, IndexClosingPrice)
                                   VALUES (?, ?, ?);''', (indexID, list[0], list[4]))
                previousList = copy.deepcopy(list)  # A previous list is saved to allow us to check that the next date is one day chronologically forward
            else:  # If we are not one day chronologically onwards then this else statement is entered
                goAgain = True
                while goAgain == True:  # This loop continues inserting values into the database if the next date isn't one day chronologically onwards.
                    # The values will be the values of the last data point that was used.
                    if nextDate != list[0]:  # If the day we inserting a value for doesnt match the day of the datapoint in the list
                        # then we use the data from the last datapoint and insert that in for the specific day
                        c.execute('''INSERT INTO IndexValues (IndexID, Date, IndexClosingPrice)
                                                           VALUES (?, ?, ?);''', (indexID, nextDate, previousList[4]))
                        previousList[0] = nextDate  # The list with the last data point used has its date set to be equal to next date, which is now the date
                        # value which has just been added into the database
                    else:  # If the date value that should be inserted has a value within the csv file then we stop the loop and the values from the csv
                        # file are inserted into the database
                        goAgain = False
                        previousList[0] = nextDate
                    nextDate = dateProcessing(previousList[0])  # The new value for the next date is calculated by increasing the last inserted date by one
                c.execute('''INSERT INTO IndexValues (IndexID, Date, IndexClosingPrice)
                                                   VALUES (?, ?, ?);''', (indexID, list[0], list[4]))


            start = False   # We know that by this point in the code the first data point from the csv file has been used and
            # we are now no longer on line one therefore start can be set to false
        first = False  # We know that the we are no longer on the first line by this point as right after this the next iteration of the
        # loop occurs setting us to the next line, therefore first can be set to false

    # This last part puts values in up to the last date needed if we don't have data points up to the last date
    i = i.strip("\n")  # i will be the last line in the csv file as that is the line that the loop will end on
    list = i.split(",")
    while list[0] != lastDate:  # If we have data for the last date then we don't need to enter this loop
        nextDate = dateProcessing(list[0])
        list[0] = nextDate  # The list is updated so its date is now one day onwards from it.
        c.execute('''INSERT INTO IndexValues (IndexID, Date, IndexClosingPrice)
                                           VALUES (?, ?, ?);''', (indexID, list[0], list[4]))
        # The last data points values are then used for the next dates values as we don't have a value for it.
        # This therefore inserts data into the database for all the values form the last date with data value up until the
        # last date that we need values for as it iterates up to it, each time checking if the date we are inserting for
        # is at the last date we need a value for and when it is, the program inserts a value for it and then stops inserting
        # any more values

    conn.commit()  # This commits the changes to the database

def dividendInsertion(file, stockID, firstDate, lastDate):
    '''
        This procedure puts values into the dividend table of the database for stock ID, Date and dividend.
        Data processing is done here which is discussed at the bottom of the file.
        :param file: string
            This is the csv file containing the data
        :param stockID: int
            The stockID as an integer
        :param firstDate: string
            This is the start date that data was collected from, needed for data processing
        :param lastDate: string
            This is the last date that data was collected from, needed for data processing
    '''
    start = True  # This variable denotes if it is the first line containing data in the file.
    first = True  # This variable denotes if it is the first line in the csv file. This just contains column headings
    previousList = []
    for i in file:  # This iterates through every line in the csv file which contains the data
        if first != True:  # If it is the first, then you don't put something into the database as the first line is not full of data, it is the column titles
            i = i.strip("\n")
            list = i.split(",")
            valuesStartDate = list[0]  # Values start date will be the value that data points have their date starting at.
            if start == True and list[0] != firstDate:  # If the first data point doesnt have the same date value as the first date needed
                # then this if statement is entered
                list[0] = firstDate  # The date is then set to be equal to the first date that data is needed for and data is entered into the database
                # for this date but the values used are for the first date that we have values for
                c.execute('''INSERT INTO Dividend (StockID, Date, DividendPaid)
                                                                                                                        VALUES (?, ?, ?);''',
                          (stockID, list[0], list[1]))
                while list[0] != valuesStartDate:  # This while loop inserts data into the tables for all the dates that do
                    # not have values up until the first date with values in the csv file. It increases the date using date processing,
                    # inserting values into the database. The values other than date will all be the same as the values for the first
                    # data point in the csv file.
                    nextDate = dateProcessing(list[0])
                    list[0] = nextDate  # The new increased date values is put into the list
                    if list[0] != valuesStartDate:
                        c.execute('''INSERT INTO Dividend (StockID, Date, DividendPaid)
                                                                                        VALUES (?, ?, ?);''',
                                  (stockID, list[0], list[1]))
            if start != True:  # If it is not the first value in the list then we can work out what the date we should now be on.
                # This is by using the previous data points date and checking what the next date is chronologically.
                nextDate = dateProcessing(previousList[0])
            else:  # If it is the first value in the list then there will be no previous list, therefore we don't
                # have a value for what the date "should be", therefore next date is set to no
                nextDate = "No"

            if nextDate == list[0] or start == True:  # If we either have chronologically increased date by one from the last insertion
                # or if we are using the first data point then value are inserted into the list as normal. We know by this point that
                # the first data point is on the next chronological date as the previous dates have already been added and if next date
                # is equal to the date in the list then we are on the next chronological date therefore the value can be inserted normally
                c.execute('''INSERT INTO Dividend (StockID, Date, DividendPaid)
                                                        VALUES (?, ?, ?);''', (stockID, list[0], list[1]))
                previousList = copy.deepcopy(list)  # A previous list is saved to allow us to check that the next date is one day chronologically forward
            else:  # If we are not one day chronologically onwards then this else statement is entered
                goAgain = True
                while goAgain == True:  # This loop continues inserting values into the database if the next date isn't one day chronologically onwards.
                    # The values will be the values of the last data point that was used.
                    if nextDate != list[0]:  # If the day we inserting a value for doesnt match the day of the datapoint in the list
                        # then we use the data from the last datapoint and insert that in for the specific day
                        c.execute('''INSERT INTO Dividend (StockID, Date, DividendPaid)
                                                                                    VALUES (?, ?, ?);''',
                                  (stockID, nextDate, previousList[1]))
                        previousList[0] = nextDate  # The list with the last data point used has its date set to be equal to next date, which is now the date
                        # value which has just been added into the database
                    else:  # If the date value that should be inserted has a value within the csv file then we stop the loop and the values from the csv
                        # file are inserted into the database
                        goAgain = False
                        previousList[0] = nextDate
                    nextDate = dateProcessing(previousList[0])  # The new value for the next date is calculated by increasing the last inserted date by one
                c.execute('''INSERT INTO Dividend (StockID, Date, DividendPaid)
                                                                        VALUES (?, ?, ?);''',
                          (stockID, list[0], list[1]))


            start = False   # We know that by this point in the code the first data point from the csv file has been used and
            # we are now no longer on line one therefore start can be set to false
        first = False  # We know that the we are no longer on the first line by this point as right after this the next iteration of the
        # loop occurs setting us to the next line, therefore first can be set to false

    # This last part puts values in up to the last date needed if we don't have data points up to the last date
    i = i.strip("\n")
    list = i.split(",")
    while list[0] != lastDate:  # If we have data for the last date then we don't need to enter this loop
        nextDate = dateProcessing(list[0])
        list[0] = nextDate  # The list is updated so its date is now one day onwards from it.
        c.execute('''INSERT INTO Dividend (StockID, Date, DividendPaid)
                                                                        VALUES (?, ?, ?);''',
                  (stockID, list[0], list[1]))
        # The last data points values are then used for the next dates values as we don't have a value for it.
        # This therefore inserts data into the database for all the values form the last date with data value up until the
        # last date that we need values for as it iterates up to it, each time checking if the date we are inserting for
        # is at the last date we need a value for and when it is, the program inserts a value for it and then stops inserting
        # any more values

    conn.commit()  # This commits the changes to the database

def stockValuesInsertion(file, stockID, firstDate, lastDate):
    '''
        This procedure puts values into the stockValues table of the database for StockId, date, closing price and trading volume.
        Data processing is done here which is discussed at the bottom of the file.
        :param file: string
            This is the csv file containing the data
        :param stockID: int
            The stockID as an integer
        :param firstDate: string
            This is the start date that data was collected from, needed for data processing
        :param lastDate: string
            This is the last date that data was collected from, needed for data processing
    '''
    start = True  # This variable denotes if it is the first line containing data in the file.
    first = True  # This variable denotes if it is the first line in the csv file. This just contains column headings
    previousList = []
    for i in file:  # This iterates through every line in the csv file which contains the data
        if first != True:  # If it is the first, then you don't put something into the database as the first line is not full of data, it is the column titles
            i = i.strip("\n")
            list = i.split(",")
            valuesStartDate = list[0]  # Values start date will be the value that data points have their date starting at.
            if start == True and list[0] != firstDate:  # If the first data point doesnt have the same date value as the first date needed
                # then this if statement is entered
                list[0] = firstDate  # The date is then set to be equal to the first date that data is needed for and data is entered into the database
                # for this date but the values used are for the first date that we have values for
                c.execute('''INSERT INTO StockValues (StockID, Date, ClosingPrice, TradingVolume)
                                                                        VALUES (?, ?, ?, ?);''',
                          (stockID, list[0], list[4], list[6]))
                while list[0] != valuesStartDate:  # This while loop inserts data into the tables for all the dates that do
                    # not have values up until the first date with values in the csv file. It increases the date using date processing,
                    # inserting values into the database. The values other than date will all be the same as the values for the first
                    # data point in the csv file.
                    nextDate = dateProcessing(list[0])
                    list[0] = nextDate  # The new increased date values is put into the list
                    if list[0] != valuesStartDate:
                        c.execute('''INSERT INTO StockValues (StockID, Date, ClosingPrice, TradingVolume)
                                                                                        VALUES (?, ?, ?, ?);''',
                                  (stockID, list[0], list[4], list[6]))
            if start != True:  # If it is not the first value in the list then we can work out what the date we should now be on.
                # This is by using the previous data points date and checking what the next date is chronologically.
                nextDate = dateProcessing(previousList[0])
            else:  # If it is the first value in the list then there will be no previous list, therefore we don't
                # have a value for what the date "should be", therefore next date is set to no
                nextDate = "No"

            if nextDate == list[0] or start == True:  # If we either have chronologically increased date by one from the last insertion
                # or if we are using the first data point then value are inserted into the list as normal. We know by this point that
                # the first data point is on the next chronological date as the previous dates have already been added and if next date
                # is equal to the date in the list then we are on the next chronological date therefore the value can be inserted normally
                c.execute('''INSERT INTO StockValues (StockID, Date, ClosingPrice, TradingVolume)
                                                        VALUES (?, ?, ?, ?);''', (stockID, list[0], list[4], list[6]))
                previousList = copy.deepcopy(list)  # A previous list is saved to allow us to check that the next date is one day chronologically forward
            else:  # If we are not one day chronologically onwards then this else statement is entered
                goAgain = True
                while goAgain == True:  # This loop continues inserting values into the database if the next date isn't one day chronologically onwards.
                    # The values will be the values of the last data point that was used.
                    if nextDate != list[0]:  # If the day we inserting a value for doesnt match the day of the datapoint in the list
                        # then we use the data from the last datapoint and insert that in for the specific day
                        c.execute('''INSERT INTO StockValues (StockID, Date, ClosingPrice, TradingVolume)
                                                                                    VALUES (?, ?, ?, ?);''',
                                  (stockID, nextDate, previousList[4], previousList[6]))
                        previousList[0] = nextDate  # The list with the last data point used has its date set to be equal to next date, which is now the date
                        # value which has just been added into the database
                    else:  # If the date value that should be inserted has a value within the csv file then we stop the loop and the values from the csv
                        # file are inserted into the database
                        goAgain = False
                        previousList[0] = nextDate
                    nextDate = dateProcessing(previousList[0])  # The new value for the next date is calculated by increasing the last inserted date by one
                c.execute('''INSERT INTO StockValues (StockID, Date, ClosingPrice, TradingVolume)
                                                                        VALUES (?, ?, ?, ?);''',
                          (stockID, list[0], list[4], list[6]))


            start = False   # We know that by this point in the code the first data point from the csv file has been used and
            # we are now no longer on line one therefore start can be set to false
        first = False  # We know that the we are no longer on the first line by this point as right after this the next iteration of the
        # loop occurs setting us to the next line, therefore first can be set to false

    # This last part puts values in up to the last date needed if we don't have data points up to the last date
    i = i.strip("\n")
    list = i.split(",")
    while list[0] != lastDate:  # If we have data for the last date then we don't need to enter this loop
        nextDate = dateProcessing(list[0])
        list[0] = nextDate  # The list is updated so its date is now one day onwards from it.
        c.execute('''INSERT INTO StockValues (StockID, Date, ClosingPrice, TradingVolume)
                                                                                VALUES (?, ?, ?, ?);''',
                  (stockID, list[0], list[4], list[6]))
        # The last data points values are then used for the next dates values as we don't have a value for it.
        # This therefore inserts data into the database for all the values form the last date with data value up until the
        # last date that we need values for as it iterates up to it, each time checking if the date we are inserting for
        # is at the last date we need a value for and when it is, the program inserts a value for it and then stops inserting
        # any more values

    conn.commit()  # This commits the changes to the database

def dividendInsertionForZero(stockID, firstDate, lastDate):
    '''
        This procedure fills the database of dividend values when there is no dividend, putting values in for StockID, date and dividend.
        A value of 0 is inserted for the dividend
        :param stockID: int
            The stockID as an integer
        :param firstDate: string
            This is the start date that data was collected from, needed for data processing
        :param lastDate: string
            This is the last date that data was collected from, needed for data processing
    '''
    iterations = dateConversion(lastDate) - dateConversion(firstDate) +1 # This works out the number of values that are needed as there must be a value for each day between the first and last date
    c.execute('''INSERT INTO Dividend (StockID, Date, DividendPaid)
                                                    VALUES (?, ?, ?);''',
              (stockID, firstDate, 0))
    date = firstDate
    for i in range(iterations):
        date = dateProcessing(date)  # This increases the date by one for each iteration therefore there is a value for each date
        c.execute('''INSERT INTO Dividend (StockID, Date, DividendPaid)
                                                    VALUES (?, ?, ?);''',
                  (stockID, date,0))
    conn.commit()
    
'''
These functions are used to input the data into the stock database
'''

'''
The data must be processed to ensure there are values in all categories every day. This is to ensure
that the algorithm works as the algorithm needs a value in each category if it has a value in one category.
Therefore if there is no value for the next day then the previous days value is normally used. This occurs both at the end 
where if the data doesn't go on long enough then the last days value is used for all the days up to the last day but 
also for values in between where there isn't a value for the day. Data must also be taken from the first measured day
if there is no value for the first days. The first days data value is used for all the days up to that first measured day. This 
therefore means that there are values for every day between the start and the end date meaning the algorithm can work.
'''

# All the text files are closed below
nasdaqFile.close()
appleFile.close()
amdFile.close()
amazonFile.close()
intelFile.close()
microsoftFile.close()
nvidiaFile.close()
nvidiaDividendFile.close()
appleDividendFile.close()
microsoftDividendFile.close()
intelDividendFile.close()

