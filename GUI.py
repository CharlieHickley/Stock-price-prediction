import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from LinearRegression import twoDRegression, fiveDRegression, fillXMatrixOneVar, fillYMatrix, twoDRegressionIndex, fillXMatrixIndex, fillYMatrixIndex, dateConversion, checkValidDate, twoDRegressionStockIndex

#These values are needed for normalisation of data purposes to improve the algorithm
firstDate = "2019-09-05"
lastDate = "2024-09-04"

def graphPlot(xname, master, x, y, m, c,):
    '''
    This plots a graph of a factor for example trading volume on the x axis against the price on the y axis
    :param xname: string
        This is the name of the factor that is being plotted against price
    :param master:
        This links the graph to the GUI
    :param x: list
        The x values for the graph
    :param y: list
        The y values for the graph, this will be price
    :param m: float
        The gradient of the graph
    :param c: float
        The y intercept of the graph
    '''

    fig = plt.Figure(figsize=(10,6))
    graph = fig.add_subplot(111)

    graph.scatter(x, y)
    graph.set_ylabel("Price")
    graph.set_xlabel(xname)

    if m > 0: # If the gradient is positive the line must be plotted in a different way to if the gradient is negative
        # to ensure the line is long enough
        yMax = 1.6 * max(y)[0]  # This works out what the limit of the graphs y axis should be

        xMax = (yMax - c) / m  # This works out what the limit of the graphs x axis should be

        xGraphValues = [0, xMax]  # This is the range of values plotted on the x axis for the graph
        yGraphValues = [c, yMax]  # This is the range of values plotted on the y axis for the graph

    else:
        xMax = 1.2 * max(x)[0]

        yMax = (xMax * m)+ c

        xGraphValues = [0, xMax]  # This is the range of values plotted on the x axis for the graph
        yGraphValues = [c, yMax]  # This is the range of values plotted on the y axis for the graph

    labelValue = "y = " + str(m) + "x + " + str(c)

    graph.plot(xGraphValues, yGraphValues, label=labelValue)


    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0,column=0)

class GUI(tk.Tk):
    def __init__(self, firstDate):
        '''
        This initialises the GUI class which composes all of the separate pages together
        :param firstDate: string
            This is the first date that there is data for, this value is used to normalise the linear
            regression to make it work more effectively.
        '''
        super().__init__()
        self.title("Stock price prediction software")
        self.geometry("1000x1000")
        # The below lines instantiate the different pages
        self.welcomePage = welcomePage(self)
        self.optionPage = optionPage(self)
        self.indexGraphPage = indexGraphPage(self, firstDate)
        self.stockOptionPage = stockOptionPage(self)
        self.stockGraphPage = stockGraphPage(self, firstDate)
        self.stockValuePage = stockValuesPage(self, firstDate)
        self.pages = [self.welcomePage, self.optionPage, self.indexGraphPage,
                      self.stockOptionPage, self.stockGraphPage, self.stockValuePage]
        self.showWelcomePage()
        self.firstDate = firstDate


    def hide_pages(self):
        '''
        This procedure stops all the other pages from showing
        '''
        for page in self.pages:
            page.grid_forget()

    # All the show Page methods display that certain page

    def showWelcomePage(self):
        self.hide_pages()
        self.welcomePage.grid(row=0,column=0)

    def showOptionPage(self):
        self.hide_pages()
        self.optionPage.grid(row=0,column=0)

    def showIndexGraphPage(self):
        self.hide_pages()
        self.indexGraphPage.grid(row=0,column=0)
        self.indexGraphPage.getIndex("NASDAQ")
        self.indexGraphPage.plotIndexGraph()

    def showStockOptionPage(self, stock, index):
        self.hide_pages()
        self.stockOptionPage.grid(row=0,column=0)
        self.stockOptionPage.get_Stock(stock)
        self.stockOptionPage.getIndex(index)
        self.stockOptionPage.reset_info()

    def showStockGraphPage(self, choice, stock, index):
        if (stock == "AMD" or stock == "AMAZON") and choice == "DIVIDEND": # There is no dividend for amd or amazon so the graph page cannot be made
            self.stockOptionPage.show_info()
        else:  # If it is possible the graph page is shown with the correct graph displayed and the old page is hidden
            self.hide_pages()
            self.stockGraphPage.grid(row=0, column=0)
            self.stockGraphPage.resetGraphInfo()
            self.stockGraphPage.getStock(stock)  # Gets the name of the name of the stock for the graph
            self.stockGraphPage.getChoice(choice)  # Gets the type of graph needed
            self.stockGraphPage.getIndex(index)  # Gets teh index of the stock for the graph
            self.stockGraphPage.showStockGraph()  # Plots the graph on the page
            if choice.upper() == "DATE":  # If the graph page is date then extra data must be shown
                self.stockGraphPage.showGraphInfo()

    def showStockValuePage(self, stock, index):
        self.hide_pages()
        self.stockValuePage.grid(row=0,column=0)
        self.stockValuePage.getStock(stock)
        self.stockValuePage.getIndex(index)
        self.stockValuePage.resetLabel()

# All of the page classes below simply initialise that certain page allowing it to be displayed
class welcomePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = tk.Label(self, text="Welcome!")
        self.label.grid(row=0, column=1)

        self.button = tk.Button(self, text="RUN", command= master.showOptionPage)
        self.button.grid(row=1, column=1)

        #These two lines change the sizes of the label and the button
        self.button.config(height="10", width = "70")
        self.label.config(height="10", width="70")



class optionPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.back_button = tk.Button(self, text="Back", command=master.showWelcomePage)
        self.back_button.grid(row=0, column=3)

        self.index_button = tk.Button(self, text="NASDAQ", command=master.showIndexGraphPage)
        self.index_button.grid(row=1, column=2)

        self.grid_rowconfigure(2, weight=1)  # These lines put the pages widgets in the correct places
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.nvidia_button = tk.Button(self, text="NVIDIA", command=lambda: master.showStockOptionPage("NVIDIA", "NASDAQ"))
        self.nvidia_button.grid(row=2, column=1)
        self.amd_button = tk.Button(self, text="AMD", command=lambda: master.showStockOptionPage("AMD", "NASDAQ"))
        self.amd_button.grid(row=2, column=2)
        self.apple_button = tk.Button(self, text="APPLE", command=lambda: master.showStockOptionPage("APPLE", "NASDAQ"))
        self.apple_button.grid(row=2,column=3)
        self.microsoft_button = tk.Button(self, text="MICROSOFT", command=lambda: master.showStockOptionPage("MICROSOFT", "NASDAQ"))
        self.microsoft_button.grid(row=3, column=1)
        self.amazon_button = tk.Button(self,text="AMAZON", command=lambda: master.showStockOptionPage("AMAZON", "NASDAQ"))
        self.amazon_button.grid(row=3, column=2)
        self.intel_button = tk.Button(self, text="INTEL", command=lambda: master.showStockOptionPage("INTEL", "NASDAQ"))
        self.intel_button.grid(row=3, column=3)

        self.button_list = [self.intel_button, self.amazon_button, self.microsoft_button,
                            self.amd_button, self.nvidia_button, self.apple_button,
                            self.index_button, self.back_button]

        for i in self.button_list:
            i.config(height="12", width="35")  # This changes the size of each button


class indexGraphPage(tk.Frame,):
    def __init__(self, master, firstDate):
        super().__init__(master)
        self.index = ""
        self.firstDate = firstDate

        self.back_button = tk.Button(self, text="Back", command=master.showOptionPage)
        self.back_button.grid(row=0,column=3)

        self.frame = tk.Frame(self)
        self.frame.grid(row=1, column=0)

        self.info = tk.Label(self, text="The date information is done as a number of days since the first date that values have been measured from therefore from " + self.firstDate)
        self.info.grid(row=2, column=0)

        self.description = tk.Label(self, text="The line is the predicted values and the points are the actual measured values")
        self.description.grid(row=3, column=0)

    def plotIndexGraph(self):
        '''
        This procedure plots a graph on the page when the page is created
        '''
        y = fillYMatrixIndex(self.index)  # This gets values for the index closing price
        x = fillXMatrixIndex(self.index, self.firstDate)  # This gets values for the index's date at the corresponding closing price
        coefficients = twoDRegressionIndex("NASDAQ", firstDate)
        graphPlot("Date", self.frame, x, y, coefficients[1][0], coefficients[0][0])


    def getIndex(self, index):
        self.index = index

class stockOptionPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.stock = ""
        self.index = ""

        self.back_button = tk.Button(self, text="Back", command=master.showOptionPage)
        self.back_button.grid(row=0, column=3)

        self.dividend_button = tk.Button(self, text="DIVIDEND GRAPH", command= lambda: master.showStockGraphPage("DIVIDEND",self.stock, self.index))
        self.dividend_button.grid(row=1, column=1)
        self.tradingVolume_button = tk.Button(self, text="TRADING VOLUME GRAPH", command= lambda: master.showStockGraphPage("TRADINGVOLUME", self.stock, self.index))
        self.tradingVolume_button.grid(row=1, column=2)
        self.date_button = tk.Button(self, text="DATE GRAPH", command= lambda: master.showStockGraphPage("DATE", self.stock, self.index))
        self.date_button.grid(row=2, column=1)
        self.index_button = tk.Button(self, text="INDEX CLOSING PRICE GRAPH", command= lambda: master.showStockGraphPage("INDEX", self.stock, self.index))
        self.index_button.grid(row=2, column=2)

        self.value_button = tk.Button(self, text="Calculate a price at certain values", command= lambda: master.showStockValuePage(self.stock, self.index))
        self.value_button.grid(row=0,column=1)

        self.info = tk.Label(self, text="")
        self.info.grid(row=3, column=0)

    def get_Stock(self, stock):
        self.stock = stock

    def getIndex(self, index):
        self.index = index

    def show_info(self):
        self.info.config(text="AMD stocks and Amazon stocks do not have dividends so dividend graphs cannot be predicted on them")

    def reset_info(self):
        self.info.config(text="")

class stockValuesPage(tk.Frame):
    def __init__(self, master, firstDate):
        super().__init__(master)
        self.stock = ""
        self.dividend = None
        self.indexPrice = None
        self.date = None
        self.tradingVolume = None
        self.firstDate = firstDate
        self.index = ""


        self.back_button = tk.Button(self, text="Back", command= lambda: master.showStockOptionPage(self.stock, self.index))
        self.back_button.grid(row=0,column=5)

        self.dividend_input = tk.Entry(self)
        self.dividend_input.grid(row=1,column=1)
        self.dividend_description = tk.Label(self, text="Please input a value for dividend")
        self.dividend_description.grid(row=0,column=1)

        self.date_input = tk.Entry(self)
        self.date_input.grid(row=1, column=2)
        self.date_description = tk.Label(self, text="Please input a value for date in the form yyyy-mm-dd")
        self.date_description.grid(row=0, column=2)

        self.tradingVolume_input = tk.Entry(self)
        self.tradingVolume_input.grid(row=1, column=3)
        self.tradingVolume_description = tk.Label(self, text="Please input a value for the trading volume")
        self.tradingVolume_description.grid(row=0, column=3)

        self.indexPrice_input = tk.Entry(self)
        self.indexPrice_input.grid(row=1, column=4)
        self.indexPrice_description = tk.Label(self, text="Please input a value for the index's closing price")
        self.indexPrice_description.grid(row=0, column=4)

        self.calculate_button = tk.Button(self, text="Calculate predicted price", command=self.calculatePrice)
        self.calculate_button.grid(row=1,column=5)

        self.output_label = tk.Label(self, text="No calculations made yet")
        self.output_label.grid(row=2,column=1)

    def getStock(self, stock):
        self.stock = stock

    def getIndex(self, index):
        self.index = index

    def resetLabel(self):
        self.output_label.config(text="No calculations made yet")

    def calculatePrice(self):
        '''
        This function calculates the predicted price at certain values and then puts that onto the page.
        '''
        self.resetLabel()
        self.dividend = self.dividend_input.get()
        self.indexPrice = self.indexPrice_input.get()
        self.tradingVolume = self.tradingVolume_input.get()
        self.date = self.date_input.get()
        if self.dividend == "" or self.date == "" or self.tradingVolume == "" or self.indexPrice == "":  # Checks all inputs are full
            self.output_label.config(
                text="Not all of the factors have a value for them therefore you cannot predict a price")
        else:
            validDate = checkValidDate(self.date)  # Checks the date is valid
            if validDate == False:
                self.output_label.config(text="You have inputted an invalid date therefore the algorithm will not work")

            else:
                self.date = dateConversion(self.date)
                self.date = self.date - dateConversion(self.firstDate)
                # The below try and except statements try to convert the values to floats which will check if the values are numbers which they must be
                try:
                    self.dividend = float(self.dividend)
                except ValueError:
                    self.output_label.config(text="You have inputted an invalid dividend therefore the algorithm will not work")
                try:
                    self.indexPrice = float(self.indexPrice)
                except ValueError:
                    self.output_label.config(
                        text="You have inputted an invalid index closing price therefore the algorithm will not work")
                try:
                    self.tradingVolume = float(self.tradingVolume)
                except ValueError:
                    self.output_label.config(
                        text="You have inputted an invalid trading volume therefore the algorithm will not work")
                try:  # This tries to run the algorithm. If the algorithm doesnt work then we know that error values must have been inputted
                    coefficients = fiveDRegression(self.stock, "NASDAQ", firstDate)
                    predictedPrice = coefficients[0][0] + coefficients[1][0] * self.dividend + coefficients[2][0] * self.date \
                                     + coefficients[3][0] * self.tradingVolume + coefficients[4][0] * self.indexPrice
                    self.output_label.config(text="The predicted price is " + str(predictedPrice))
                except ValueError:
                    self.output_label.config(text="You have inputted invalid values")

class stockGraphPage(tk.Frame):
    def __init__(self, master, firstDate):
        super().__init__(master)
        self.choice = ""  # The type of graph must be stored so the right graph is displayed
        self.stock = ""  # The stock must be stored so the right graph is displayed
        self.firstDate = firstDate  # The first date must be stored so data can be normalised
        self.index = ""  # The index must be stored so the right graph is displayed
        self.canvas = None

        self.back_button = tk.Button(self, text="Back", command=lambda: master.showStockOptionPage(self.stock, self.index))
        self.back_button.grid(row=0,column=3)

        self.frame = tk.Frame(self)
        self.frame.grid(row=1, column=0)

        self.info = tk.Label(self, text="")
        self.info.grid(row=2, column=0)

        self.description = tk.Label(self, text="The line is the predicted values and the points are the actual measured values")
        self.description.grid(row=3, column=0)

        self.description2 = tk.Label(self, text = "If there is a 1ex that means that the values are 10 to the power of x multiplied by the values on the axis")
        self.description2.grid(row=4, column=0)

    def getChoice(self, choice):
        self.choice = choice

    def getStock(self, stock):
        self.stock = stock

    def getIndex(self, index):
        self.index = index

    def showGraphInfo(self):  # Extra info is needed when a graph using date is displayed
        self.info.config(text="The date information is done as a number of days since the first date"
                              " that values have been measured from therefore from " + self.firstDate)

    def resetGraphInfo(self):
        self.info.config(text="")

    def showStockGraph(self):
        '''
            This procedure plots a graph on the page when the page is created
        '''
        if self.choice == "INDEX":  # Different data collection functions must be used for graphs using index
            self.clearFrame()  # The frame must be cleared of previous graphs
            y = fillYMatrix(self.stock)  # This gets the y values for the graph
            x = fillXMatrixIndex(self.index, self.firstDate)  # This gets the x values for the graph
            coefficients = twoDRegressionStockIndex(self.stock, self.index)
            graphPlot(self.choice, self.frame, x, y, coefficients[1][0], coefficients[0][0])
        else:
            self.clearFrame() # The frame must be cleared of previous graphs
            y = fillYMatrix(self.stock)  # This gets the y values for the graph
            x = fillXMatrixOneVar(self.stock, self.choice, self.firstDate)  # This gets the x values for the graph
            coefficients = twoDRegression(self.stock, self.choice, firstDate)
            graphPlot(self.choice, self.frame, x, y, coefficients[1][0], coefficients[0][0])

    def clearFrame(self):  # This clears the frame so that the last graph chosen is not displayed when we want to display a graph
        for widget in self.frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":  # This is needed for the GUI to be displayed
    gui = GUI(firstDate)
    gui.mainloop()
