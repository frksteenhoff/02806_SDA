# Plotting with plotly
import plotly 
from IPython.display import Image
# Henriettes plotly API key og brugernavn -- gemmer plots i skyen
plotly.tools.set_credentials_file(username='frksteenhoff2', api_key='duu8hsfRmuI5rF2EU8o5')
import plotly.plotly as py
import plotly.graph_objs as go
from collections import Counter 
import geoplotlib as gpl
from geoplotlib.utils import BoundingBox

# Plotting color variables
bgBorder  = 'rgba(255, 255, 255, 0)'
ticksAxes = 'rgb(107, 107, 107)'

# Get subset of dataset values
def getValuesFromDataFrame(dataFrame, feature, listOfValues):
    data = dataFrame.loc[dataFrame[feature].isin(listOfValues)]
    return data

# 1 Count occurences of each value in dataframe for plotting
def countValuesInDataFrame(dataFrame, feature):
    val_cnt = {}
    for val in list(set(dataFrame[feature])):
        val_cnt[val] = len(dataFrame.loc[dataFrame[feature].isin([val])])
    return val_cnt

# Plot data based in year range, for all borough etc. with Geoplotlib
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


# 2 Count occurences of each value in dataframe for plotting
def countSamples(sampleSeries):
	sample_count = Counter()
	for sample in sampleSeries:
	   	sample_count[sample] += 1
	return sample_count

# Function plotting bar plot given dictionary and basic information
def createBarPlot(valueDict, plotTitle, xtitle, ytitle, nameToSave, bgBorder, ticksAxes, marginValue):

    # Plot bar chart of vehicle types involved in collisions
    labels, values = sorted(zip(*valueDict.most_common()))

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
            range=[min(values)-1,max(values+1)],
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
    return Image(nameToSave+'.png') # Display a static image


# Plot two lists in bar plotly
def createXYBarPlot(labels, values, plotTitle, xtitle, ytitle, nameToSave, bgBorder, ticksAxes, marginValue):
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
    return Image(nameToSave+'.png') # Display a static image