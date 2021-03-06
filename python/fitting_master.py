'''
References:
================ GENERAL ================
https://stackoverflow.com/questions/3433486/how-to-do-exponential-and-logarithmic-curve-fitting-in-python-i-found-only-poly
https://stackoverflow.com/questions/19189362/getting-the-r-squared-value-using-curve-fit
================ EXPONENTIAL ================
https://plot.ly/python/exponential-fits/
https://stackoverflow.com/questions/3433486/how-to-do-exponential-and-logarithmic-curve-fitting-in-python-i-found-only-poly
https://stackoverflow.com/questions/9559346/deal-with-overflow-in-exp-using-numpy
================ R - SQUARED ================
http://blog.minitab.com/blog/adventures-in-statistics-2/why-is-there-no-r-squared-for-nonlinear-regression
https://stackoverflow.com/questions/38816154/obtaining-polynomial-regression-stats-in-numpy
http://statisticsbyjim.com/regression/r-squared-invalid-nonlinear-regression/
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2892436/
https://stackoverflow.com/questions/14530770/calculating-r2-for-a-nonlinear-least-squares-fit
https://stackoverflow.com/questions/893657/how-do-i-calculate-r-squared-using-python-and-numpy
================ FORCE COORDINATES ================
https://stackoverflow.com/questions/33539287/how-to-force-specific-points-in-curve-fitting
https://stackoverflow.com/questions/15191088/how-to-do-a-polynomial-fit-with-fixed-points
'''
import plotly
plotly.tools.set_credentials_file(username='ITPTest', api_key='u4vlV6AnIkJaZssMpyFp')
import plotly.plotly as py
import plotly.graph_objs as go
import json

# Line Fitting
import numpy as np
from scipy import stats  # For linregress

# Data Reading
from openpyxl import load_workbook

# R generation
import math
from operator import mul

# K Means
from sklearn.cluster import KMeans

# Graph Options Class Model - Will update with new params accordingly
# Graph Mode: 1 - Linear, 2 - Quadratic, 3 - Cubic, 4 - Polynomial
class GraphOptions:
    def __init__(self, xDataJSON="", yDataJSON="", kMeans=False,markers = False, xAxisLabel=None, yAxisLabel=None, graphTitle=None, graphMode=1):
        # https://stackoverflow.com/questions/18283510/how-to-pass-an-array-of-integers-as-a-parameter-from-javascript-to-python
        self.xData = json.loads(xDataJSON)
        self.yData = json.loads(yDataJSON)
        self.kMeans = kMeans
        self.markers = markers
        self.xAxisLabel = xAxisLabel
        self.yAxisLabel = yAxisLabel
        self.graphTitle = graphTitle
        self.graphMode = graphMode
    
''' 
# Initialize the list of graph options (To be completed according to how the front end passes the data
def initOptionsList():
    return None

# Reworked Graph Function
# To confirm whether it is generating multiple graphs at once per list or single graph with multiple lines
def generateGraphs(optList=[]):
    if len(optList) == 0:
        return None
    
    for options in optList:
        print options.graphMode
        # Clean data if necessary (nan)
        
        if options.kMeans is True:
            print 'K-Means applied to data\n'
            numClusters = len(x) / 5
            beforeCoords = np.c_[np.array(x), np.array(y)]
            kmeans = KMeans(n_clusters=numClusters, random_state=0).fit(beforeCoords)
            x = [xN for xN, yN in kmeans.cluster_centers_]
            y = [yN for xN, yN in kmeans.cluster_centers_]
'''
            
# To rewrite using a list of objects
def generateGraphTest(graphMode=1, xData=[], xData2=[], yData=[], yData2=[], zData=[], zData2=[], kmeansOn=False, viewMarkers=False):
    # Test Comparison
    # Workaround for NaN
    x = []
    y = []
    for i in range(len(xData)):
        if str(xData[i]) == 'nan' or str(yData[i]) == 'nan':
            continue
        else:
            x.append(xData[i])
            y.append(yData[i])
            
    data = []
    
##    x = xData
##    y = yData
    x2 = xData2
    y2 = yData2
    
    if kmeansOn is True:
        print 'K-Means applied to data\n'
        numClusters = len(x) / 5
        beforeCoords = np.c_[np.array(x), np.array(y)]
        kmeans = KMeans(n_clusters=numClusters, random_state=0).fit(beforeCoords)
        x = [xN for xN, yN in kmeans.cluster_centers_]
        y = [yN for xN, yN in kmeans.cluster_centers_]


    # Polyfit method master race 1=linear, 2=quadratic, 3=cubic, 4=idk
    print "Graph Mode is " + str(graphMode)
    z = np.polyfit(x, y, graphMode)
    f = np.poly1d(z)
    print 'First Formula'
    print f
    
    x_new = np.linspace(min(x), max(x), max(x))
    y_new = f(x_new)

    trace2 = go.Scatter(
        x=x_new,
        y=y_new,
        mode='lines',
        marker=go.Marker(color='rgb(31, 119, 180)'),
        name='After DD'
    )
    
    if viewMarkers:
        trace3 = go.Scatter(
            x=x,
            y=y,
            mode='markers',
            marker=go.Marker(color='rgb(31, 119, 180)'),
            name='After DD'
        )
        data.append(trace3)

    data.append(trace2)
        
    # Run if there is data for 2nd line
    if x2 != [] and y2 != []:
        if kmeansOn is True:
            print 'K-Means applied to data\n'
            numClusters2 = len(x2) / 5
            afterCoords = np.c_[np.array(x2), np.array(y2)]
            kmeans2 = KMeans(n_clusters=numClusters2, random_state=0).fit(afterCoords)
            x2 = [xN for xN, yN in kmeans2.cluster_centers_]
            y2 = [yN for xN, yN in kmeans2.cluster_centers_]
            
        z2 = np.polyfit(x2, y2, graphMode)
        f2 = np.poly1d(z2)
        print '2nd Formula'
        print f2
        print 'Individual Values of After DD formula (debug purposes)'
        for item in f2:
            print item  # individual value

        # calculate new x's and y's
        x_new2 = np.linspace(min(x2), max(x2), max(x2))
        y_new2 = f2(x_new2)

        # Creating the dataset, and generating the plot
        trace1 = go.Scatter(
            x=x_new2,
            y=y_new2,
            mode='lines',
            marker=go.Marker(color='rgb(255, 127, 14)'),
            name='Before DD'
        )
        data.append(trace1)
        
        if viewMarkers:
            trace4 = go.Scatter(
                x=x2,
                y=y2,
                mode='markers',
                marker=go.Marker(color='rgb(255, 127, 14)'),
                name='Before DD '
            )
            data.append(trace4)


    layout = go.Layout(
        title='FO Consumption & Speed Graph',
        plot_bgcolor='rgb(229, 229, 229)',
        xaxis=go.XAxis(title='Speed Made Good (Kts)', zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
        yaxis=go.YAxis(title='Wind Force', zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
        ##                  annotations=[annotation]
    )

    fig = go.Figure(data=data, layout=layout)
    return plotly.offline.plot(fig, filename='FO Consumption & Speed Polynomial Graph', output_type='div')

def calculate_r(xList, yList):
    ##    Defective Cubic R**2
    ##    yMean = sum(yList)/len(yList)
    ##    sstot = sum([(y - yMean)**2 for y in yList])
    ##    ssres = []
    ##    count = 0
    ##    for x in xList:
    ##        yVal = 0.1738*(x**3) - 10.53*(x**2) - 212.8*x - 1275
    ##        ssres.append((yList[count] - yVal)**2)
    ##        count += 1
    ##    ssres2 = sum(ssres)
    ##    r3 = 1 - (ssres2/sstot)
    ##    print "R2 cube = " + str(r3)

    # Linear
    sumXY = sum(map(mul, xList, yList))
    sumX = sum(xList)
    sumY = sum(yList)
    n = len(xList)
    sumX2 = sum([i ** 2 for i in xList])
    sumY2 = sum([i ** 2 for i in yList])

    rValue = (sumXY - (sumX * sumY) / n) / math.sqrt((sumX2 - sumX ** 2 / n) * (sumY2 - sumY ** 2 / n))

    print "R=" + str(rValue)
    print "R-Squared=" + str(rValue ** 2)
    return rValue


# linregress method with R value
##slope, intercept, r_value, p_value, std_err = stats.linregress(x2,y2)
##print slope
##print intercept
##print r_value
##calculate_r(x2, y2)
