import sqlite3
from Matrix import Matrix2d, MatrixAny, LinearRegressionAny, LinearRegression2d

filePath = "C:/Users/2441/Computer Science NEA code/"
conn = sqlite3.connect(filePath + "Stock Database")
c = conn.cursor()

def checkValidDate(date):
    '''
    This function checks if the date inputted is a valid date, if it
     is then the function returns true and if it isn't the function
     returns false instead
    :param date: string
        This will be a string of the date in the form yyyy-mm-dd
    :return validDate: bool
        This will be true if the date is valid and false if it is invalid
    '''
    validDate = True
    try:
        if len(date) != 10: # If the date is not of length 10 that means it isn't valid as it is then not in the correct format
            validDate = False
        elif int(date[0:4]) < 0:  # If years value is negative then the date is not valid
            validDate = False
        elif int(date[5:7]) <= 0 or int(date[5:7]) > 12:  # If the month value is less than or equal to 0 or more than 12 we know the date isn't valid
            validDate = False
        elif dateConversion(date) < 0:  # If the total number of days the date corresponds to is negative the date isn't valid
            validDate = False
        elif int(date[8:10]) <= 0:  # If the day value is negative the date isn't valid
            validDate = False
        elif int(date[8:10]) > 31:  # If the day value is greater than 31 then it isn't valid
            validDate = False
        elif int(date[8:10]) > 30 and (
                int(date[5:7]) == 2 or int(date[5:7]) == 4 or int(date[5:7]) == 6 or int(date[5:7]) == 9 or int(
                date[5:7]) == 11):  # If the day value is greater than 30 and one of the specified months then it isn't valid
            validDate = False
        elif int(date[8:10]) > 29 and int(date[5:7]) == 2 and int(date[0:4]) % 4 == 0:  # If the day value is greater
            # than 29 and it is february on a leap year then the date isn't valid
            validDate = False
        elif int(date[8:10]) > 28 and int(date[5:7]) == 2 and int(date[0:4]) % 4 != 0:  #  If the day value is greater than 28
            # and it is february and not a leap year then the date isn't valid
            validDate = False

    except ValueError:  # If any of the statements cause an error when checking then the date must not be valid
        validDate = False

    return validDate

def dateConversion(date):
    '''
    This converts date into a total number of days, as the linear
    regression model needs an integer value not a string value.
    :param date: string
        A string representing the date in the form "yyyy-mm-dd"
    :return dayCount: int
        The number of days that date value corresponds to AD
    '''
    # Below are two dictionaries which contain the values for the number of days there have been in a year up to a certain month
    monthDaysNormal = {
        0 : 0,
        1 : 31,
        2 : 59,
        3 : 90,
        4 : 120,
        5 : 151,
        6 : 181,
        7 : 212,
        8 : 243,
        9 : 273,
        10 : 304,
        11 : 334,
        12 : 365
    }
    monthDaysLeap = {
        0 : 0,
        1 : 31,
        2 : 60,
        3 : 91,
        4 : 121,
        5 : 152,
        6 : 182,
        7 : 213,
        8 : 244,
        9 : 274,
        10 : 305,
        11 : 335,
        12 : 366
    }
    dayCount = 0

    #add days from years, days from leap years must be counted separately to normal years
    # as leap years have a different number of days to normal years
    leapYearCount = (int(date[0:4]) - 1) // 4
    leapYearDays = leapYearCount * 366
    normalYearCount = int(date[0:4]) - 1 - leapYearCount
    normalYearDays = normalYearCount * 365
    dayCount += leapYearDays
    dayCount += normalYearDays

    #add days from days
    dayCount += int(date[8:])

    # add days from months
    if int(date[0:4]) % 4 == 0:
        dayCount += monthDaysLeap[int(date[5:7]) -1]
    else:
        dayCount += monthDaysNormal[int(date[5:7]) - 1]

    return(dayCount)

def fillYMatrix(stockName):
    '''
    This function returns the price values for the stock that is requested in a matrix in a 2 by 2 list format
    :param stockName: string
        The name of stock that data is being searched for
    :return yMatrixValues: list
        The price values for the stock requested in 2 by 2 list format, price in each list
    '''
    yMatrixValues = []
    closingPrice = 0
    c.execute('''SELECT StockValues.ClosingPrice FROM StockValues, Stock WHERE StockValues.StockID = Stock.StockID AND Stock.StockName = ?;''', [stockName])
    closingPrice = c.fetchall() # This will be a 2d list of all the closing price values
    for i in closingPrice: # This puts the price values into 2 by 2 list format
        list = [i[0]]
        yMatrixValues.append(list)

    return(yMatrixValues)

def fillXMatrixFully(stockName, indexName, firstDate):
    '''
    This function returns a matrix that contains the values for the stock
    for date, trading volume, its indexes price, dividend.
    :param stockName: string
        The name of stock that data is being requested for
    :param indexName: string
        The name of the index that the stock that is having data requested for is in.
    :param firstDate: string
        The first measured date is needed to allow the date values to be normalised
    :return xMatrixValues: list
        A matrix containing the values for the stock requested in 2d list format.
    '''
    xMatrixValues = []
    c.execute(
        '''SELECT Dividend.DividendPaid FROM Stock, Dividend WHERE Dividend.StockID = Stock.StockID AND Stock.StockName = ?;''',
        [stockName])
    dividendValues = c.fetchall()
    c.execute(
        '''SELECT StockValues.Date FROM Stock, StockValues WHERE StockValues.StockID = Stock.StockID AND Stock.StockName = ?;''',
        [stockName])
    dateValues = c.fetchall()
    c.execute(
        '''SELECT IndexValues.IndexClosingPrice FROM Stock, IndexValues, IndexTable WHERE IndexTable.IndexID = IndexValues.IndexID 
        AND Stock.IndexID = IndexTable.IndexID AND Stock.StockName = ? AND IndexTable.IndexName = ?;''',
        [stockName, indexName])
    indexPriceValues = c.fetchall()
    c.execute(
        '''SELECT StockValues.TradingVolume FROM Stock, StockValues WHERE StockValues.StockID = Stock.StockID AND Stock.StockName = ?;''',
        [stockName])
    tradingVolumeValues = c.fetchall()
    # Can just do a for loop as all of the tuples are the same length
    for i in range(0,len(dateValues)): # A 2d list must be made for the linear regression algorithm to work
        # All of the temporary values are 2d lists full of the data
        dividendTemp = dividendValues[i][0]
        indexPriceTemp = indexPriceValues[i][0]
        dateTemp = dateConversion(dateValues[i][0])
        dateTemp = dateTemp - dateConversion(firstDate)  # Normalised values to improve linear regression algorithms
        tradingVolumeTemp = tradingVolumeValues[i][0]
        xMatrixValuesTemp = [dividendTemp, dateTemp, tradingVolumeTemp, indexPriceTemp]
        xMatrixValues.append(xMatrixValuesTemp)

    return(xMatrixValues)

def fillXMatrixOneVar(stockName, variable, firstDate):
    '''
    This function returns a matrix that contains the values for the stock
    for the factor requested for example trading volume.
    :param stockName: string
        The name of stock that data is being requested for.
    :param indexName: string
        The name of the index that the stock that is having data requested for is in.
    :param variable: string
        The variable that data is being requested for.
    :param firstDate: string
        The first measured date is needed to allow the date values to be normalised
    :return xMatrixValues: list
        A matrix containing the values for the stock requested in 2d list format.
    '''
    xMatrixValues = []
    if variable.upper() == "TRADINGVOLUME":
        c.execute(
            '''SELECT StockValues.TradingVolume FROM Stock, StockValues WHERE StockValues.StockID = Stock.StockID AND Stock.StockName = ?;''',
            [stockName])
        values = c.fetchall()

    elif variable.upper() == "DATE":
        c.execute(
            '''SELECT StockValues.Date FROM Stock, StockValues WHERE StockValues.StockID = Stock.StockID AND Stock.StockName = ?;''',
            [stockName])
        values = c.fetchall()

    elif variable == "DIVIDEND":
        c.execute(
            '''SELECT Dividend.DividendPaid FROM Stock, Dividend WHERE Dividend.StockID = Stock.StockID AND Stock.StockName = ?;''',
            [stockName])
        values = c.fetchall()
    if variable.upper() == "DATE":
        for i in values:
            xValueTemp = dateConversion(i[0]) # It must be made into a 2d list for the linear regression algorithm to work
            xValueTemp = [xValueTemp - dateConversion(firstDate)] # The data is normalised to make the algorithm run better
            xMatrixValues.append(xValueTemp)
    else:
        for i in values:  # Values must be put into 2d list format for the linear regression algorithm to work
            xValueTemp = [i[0]]  # Value returned must be extracted
            xMatrixValues.append(xValueTemp)

    return(xMatrixValues)

def fillXMatrixIndex(indexName, firstDate):
    '''
    This function returns a matrix in 2d list format of date values(converted to a number of days)
    for the specific index
    :param indexName: string
        This is the name of the index data is being requested for
    :param firstDate: string
        This is the first date that data is collected for allowing the date values to be normalised
    :return xMatrixValues: list
        A matrix in 2d list format containing date values for the index
    '''
    xMatrixValues = []
    c.execute(
        '''SELECT IndexValues.Date FROM IndexValues, IndexTable WHERE IndexTable.IndexID = IndexValues.IndexID AND IndexTable.IndexName = ?;''',
        [indexName])
    values = c.fetchall()
    for i in values:  # The values are put into 2d list format so the algorithm works
        xValuesTemp = dateConversion(i[0])  # The value must be converted into a number of days and extracted from the list
        xValuesTemp = [xValuesTemp - dateConversion(firstDate)]  # Data is normalised to improve the algorithm
        xMatrixValues.append(xValuesTemp)
    return(xMatrixValues)

def fillYMatrixIndex(indexName):
    '''
    This function returns a matrix in 2d list format of closing
    price values for the specific index
    :param indexName: string
        This is the name of the index data is being requested for
    :return yMatrixValues: list
        A matrix in 2d list format containing closing price values for the index
    '''
    yMatrixValues = []
    c.execute(
        '''SELECT IndexValues.IndexClosingPrice FROM IndexValues, IndexTable WHERE IndexTable.IndexID = IndexValues.IndexID AND IndexTable.IndexName = ?;''',
        [indexName])
    values = c.fetchall()
    for i in values:  # Values are put into 2d list format so the algorithm works
        yValuesTemp = [i[0]]  # Value returned must be extracted
        yMatrixValues.append(yValuesTemp)
    return(yMatrixValues)


def twoDRegressionIndex(indexName, firstDate):
    '''
        This function returns an object of the matrix class which holds
        within it the coefficients for the linear regression algorithm
        :param indexName: string
            The name of the index that the stock which is having the algorithm run on it belongs in.
        :param firstDate: string
            This will be the first date that data is collected for to allow date values to be normalised improving the algorithm
        :return: Matrix class
            A matrix containing the coefficients resulting from the linear regression algorithm.
        '''
    yValues = fillYMatrixIndex(indexName)
    yMatrix = Matrix2d(yValues)  # A matrix is created full of closing price values for the index
    xValues = fillXMatrixIndex(indexName, firstDate)
    xMatrix = Matrix2d(xValues)  # A matrix is created full of date values for the index
    return(LinearRegression2d(yMatrix, xMatrix))  # The linear regression algorithm is called and the coefficients are returned


def twoDRegression(stockName, otherFactor, firstDate):
    '''
    This function returns an object of the matrix class which holds
    within it the coefficients for the linear regression algorithm
    :param stockName: string
        The name of stock that the algorithm is being run on.
    :param otherFactor: string
        The name of the other factor that price is being compared to.
    :param firstDate: string
            This will be the first date that data is collected for to allow date values to be normalised improving the algorithm
    :return: Matrix class
        A matrix containing the coefficients resulting from the linear regression algorithm.
    '''
    yValues = fillYMatrix(stockName)
    yMatrix = Matrix2d(yValues)  # A matrix is created full of closing price values for the stock
    xValues = fillXMatrixOneVar(stockName, otherFactor, firstDate)
    xMatrix = Matrix2d(xValues)  # A matrix is created full of values corresponding to the closing price values for the stock
    # The values are either for date, dividend, trading volume.
    return(LinearRegression2d(yMatrix, xMatrix)) # The linear regression algorithm is called and the coefficients are returned

def twoDRegressionStockIndex(stockName, indexName):
    '''
        This function returns an object of the matrix class which holds
        within it the coefficients for the linear regression algorithm.
        This is just for doing the stock price against index price.
        :param stockName: string
            The name of stock that the algorithm is being run on.
        :param indexName: string
            The name of the index the stock belongs to
        :return: Matrix class
            A matrix containing the coefficients resulting from the linear regression algorithm.
        '''
    yValues = fillYMatrix(stockName)
    yMatrix = Matrix2d(yValues)  # A matrix is created full of closing price values for the stock
    xValues = fillYMatrixIndex(indexName)
    xMatrix = Matrix2d(xValues)  # A matrix is created full of values for the index's closing price
    return (LinearRegression2d(yMatrix, xMatrix)) # The linear regression algorithm is called and the coefficients are returned

def fiveDRegression(stockName, indexName, firstDate):
    '''
    This function returns an object of the matrix class which holds
    within it the coefficients for the linear regression algorithm.
    The order of coefficients in the list will be the y intercept,
    then the dividend, then the date, trading volume, index closing price.
    :param stockName: string
        The name of stock that the algorithm is being run on.
    :param indexName: string
        The name of the index that the stock which is having the algorithm run on it belongs in.
    :param firstDate: string
            This will be the first date that data is collected for to allow date values to be normalised improving the algorithm
    :return: Matrix class
        A matrix containing the coefficients resulting from the linear regression algorithm.
    '''
    yValues = fillYMatrix(stockName)
    yMatrix = MatrixAny(yValues)  # A matrix is created full of closing price values for the stock
    xValues = fillXMatrixFully(stockName, indexName, firstDate)
    xMatrix = MatrixAny(xValues)  # A matrix is created full of values corresponding to the closing price values for the stock
    # The values are for date, dividend, trading volume and the closing price of the index the stock is in.
    return(LinearRegressionAny(yMatrix,xMatrix)) # The linear regression algorithm is called and the coefficients are returned