import sqlite3
conn = sqlite3.connect("Stock Database")  # This connects to the database
c = conn.cursor()

# The below code creates the necessary tables within the database

c.execute('''CREATE TABLE IF NOT EXISTS Stock(
StockID varchar(30),
StockName varchar(100),
IndexID varchar(30),
PRIMARY KEY (StockID));''')

c.execute('''CREATE TABLE IF NOT EXISTS StockValues(
StockID varchar(30),
Date DATE,
ClosingPrice REAL,
TradingVolume int,
PRIMARY KEY (Date, StockID));''')

c.execute('''CREATE TABLE IF NOT EXISTS IndexValues(
IndexID varchar(30),
Date DATE,
IndexClosingPrice REAL,
PRIMARY KEY (IndexID, Date));''')

c.execute('''CREATE TABLE IF NOT EXISTS IndexTable(
IndexID varchar(30),
IndexName varchar(100),
PRIMARY KEY (IndexID));''')

c.execute('''CREATE TABLE IF NOT EXISTS Dividend(
StockID varchar(30),
Date DATE,
DividendPaid REAL,
PRIMARY KEY (Date, StockID));''')
