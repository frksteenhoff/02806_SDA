# Henriette Steenhoff, Jonas Søndergaard Schmidt, DTU May 2017
# Function definitions used in Explainer Notebook found at:
# http://nbviewer.jupyter.org/github/frksteenhoff/02806_SDA/blob/master/02806_FinalProject-ExplainerNotebook.ipynb

# --------------------------------------------------------------- #
## LIBRARIES
# --------------------------------------------------------------- #
from __future__ import division
# Plotting with plotly
import plotly 
from IPython.display import Image
# Henriettes plotly API key og brugernavn -- gemmer plots i skyen
plotly.tools.set_credentials_file(username='frksteenhoff2', api_key='duu8hsfRmuI5rF2EU8o5')
import plotly.plotly as py
import plotly.graph_objs as go
from collections import Counter 
import geoplotlib as gpl
from plotly import tools
from geoplotlib.utils import BoundingBox

# --------------------------------------------------------------- #
## VARIABLES
# --------------------------------------------------------------- #
# Plotting color variables
bgBorder  = 'rgba(255, 255, 255, 0)'
ticksAxes = 'rgb(107, 107, 107)'

# --------------------------------------------------------------- #
## FUNCTIONS
# --------------------------------------------------------------- #
# Get subset of dataset values
# dataFrame    - pandas dataframe
# feature      - column value to count
# listOfValues - values to find in feature column
def getValuesFromDataFrame(dataFrame, feature, listOfValues):
    data = dataFrame.loc[dataFrame[feature].isin(listOfValues)]
    return data

# 1 Count occurences of each value in dataframe for plotting
# dataFrame - pandas dataframe
# feature   - column value to count
def countValuesInDataFrame(dataFrame, feature):
    val_cnt = {}
    for val in list(set(dataFrame[feature])):
        val_cnt[val] = len(dataFrame.loc[dataFrame[feature].isin([val])])
    return val_cnt

# Plot data based in year range, for all borough etc. with Geoplotlib
# dataFrame - pandas dataframe
# feature   - column value to fetch (lon/lat) data from (have to read as LATITUDE/LONGITUDE)
# label     - 
def plotGeoData(dataFrame, feature, label):
	plot_inc_d = {}
	for inc in dataFrame[feature].unique():
	    accidents = dataFrame.loc[dataFrame[feature].isin([inc])]
	    
	    plot_inc = {}
	    plot_inc = accidents[['LATITUDE', 'LONGITUDE']]
	    plot_inc.columns = ['lat','lon']
	    
	    for col in plot_inc.columns:
	        plot_inc_d[col] = plot_inc[col].tolist()
	    
	    # Plotting the data w. geoplotlib
	    print label + ":", inc
	    print "Samples:", len(accidents)
	    gpl.kde(plot_inc_d, bw=2, cut_below=2e-4)
	    gpl.set_bbox(BoundingBox(north=40.93, west=-73.85, south=40.53, east=-73.83))
	    gpl.inline()
	    plot_inc_d = {}

# --------------------------------------------------------------- #


# 2 Count occurences of each value in dataframe for plotting
# sampleSeries - series from dataframe to count on
def countSamples(sampleSeries):
	sample_count = Counter()
	for sample in sampleSeries:
	   	sample_count[sample] += 1
	return sample_count

# --------------------------------------------------------------- #

# valueDict   values and labels for plots (listlike, string/int)
# plotTitle - title plot (string)
# x/ytitle    - axis labels (string)
# nameToSave  - name on file to save
# bgBorder    - borderColor
# ticksAxes   - axes color
# marginValue - space (px) for x axis labels
# Function plotting bar plot given dictionary and basic information
def createBarPlot(valueDict, plotTitle, xtitle, ytitle, nameToSave, bgBorder, ticksAxes, marginValue):

    # Plot bar chart of vehicle types involved in collisions
    labels, values = zip(*valueDict.most_common())

    data = [go.Bar(
              x = labels,
              y = values
    )]

    # Setting layout details for plot
    layout = go.Layout(
        title=plotTitle,
        autosize=False,
        width=900,
        height=700,

        margin=dict(
            b=marginValue
        ),

        xaxis=dict(
            title=xtitle,
            ticklen=15,
            tickfont=dict(
                size=14,
                color=ticksAxes
            )
        ),

        yaxis=dict(
            range=[min(values)-1,max(values)+1],
            title=ytitle,
            titlefont=dict(
                size=16,
                color=ticksAxes
            ),
            tickfont=dict(
                size=16,
                color=ticksAxes
            )
        ),

        legend=dict(
            x=0,
            y=1.0,
            bgcolor=bgBorder,
            bordercolor=bgBorder
        )
    )

    fig = go.Figure(data=data, layout=layout)
    py.image.save_as(fig, filename=nameToSave+'.png')
    return py.iplot(fig) # Display a static image

# --------------------------------------------------------------- #


# Plot two lists in bar plotly
# labels      - labels on plots (listlike, string/int)
# values      - values for each label (listlike, numeral)
# plotTitle - title plot (string)
# x/ytitle    - axis labels (string)
# nameToSave  - name on file to save
# bgBorder    - borderColor
# ticksAxes   - axes color
# marginValue - space (px) for x axis labels 
def createXYBarPlot(labels, values, plotTitle, xtitle, ytitle, nameToSave, bgBorder, ticksAxes, marginValue):
    data = [go.Bar(
              x = labels,
              y = values
    )]

    # Setting layout details for plot
    layout = go.Layout(
        title=plotTitle,
        autosize=False,
        width=700,
        height=500,

        margin=dict(
            b=marginValue
        ),

        xaxis=dict(
            title=xtitle,
            ticklen=15,
            tickfont=dict(
                size=14,
                color=ticksAxes
            )
        ),

        yaxis=dict(
            range=[0,max(values)+1],
            title=ytitle,
            titlefont=dict(
                size=16,
                color=ticksAxes
            ),
            tickfont=dict(
                size=16,
                color=ticksAxes
            )
        ),

        legend=dict(
            x=0,
            y=1.0,
            bgcolor=bgBorder,
            bordercolor=bgBorder
        )	
    )

    fig = go.Figure(data=data, layout=layout)
    py.image.save_as(fig, filename=nameToSave+'.png')
    return py.iplot(fig) # Display a static image

# --------------------------------------------------------------- #

# A template for plotting several bar charts in subplot
# numRows/cols  - number of rows and columns in plot grid, int
# plotTitles    - listlike, all names of plot as string
# dataFrame     - dataframe to extract features from
# feature       - feature to extract
# sampleFeature - feature to sample on 
def plotBarInSubplotGrid(numRows, numCols, subplotTitles, plotTitle, dataFrame, feature, sampleFeature, saveName, maxRange, w, h):
    sample_cnt = {}
    i = 1 # Keeping track of plot grid columns
    j = 1 # Keeping track of plot grid rows
    k = 1 # Setting axis range for all y axes 


    # Creating initial figure for subplots
    fig = tools.make_subplots(rows=2, cols=3, subplot_titles=(subplotTitles))

    for val in dataFrame[feature].unique():
        # Find needed values from dataframe
        temp       = dataFrame.loc[dataFrame[feature].isin([val])]
        # Count instances of each
        sample_cnt = countSamples(sorted(temp[sampleFeature]))
        
        trace = go.Bar(
            x=sample_cnt.keys(),
            y=sample_cnt.values()
        )

        # Creating each subplot
        fig.append_trace(trace, j, i)
        fig['layout']['yaxis'+str(k)].update(title='Number of incidents', range=[0,maxRange])
        
        # Follow the grid size
        if i < numCols:            
            i += 1
        else:
            j += 1
            i  = 1
        k += 1

    # Plot result
    fig['layout'].update(height=h, width=w, title=plotTitle, margin=dict(b=100))
    py.image.save_as(fig, filename=saveName+'.png')
    return py.iplot(fig, filename='temp')


# --------------------------------------------------------------- #
# FUNCTIONS USED FOR MACHINE LEARNING PURPOSES
# --------------------------------------------------------------- #

# Calculating the score for train and test data
def score(pred_data, test_data):
    c = 0
    for i in range(len(test_data)):
        if pred_data[i] == test_data[i]:
            c += 1
    return c/len(test_data)
