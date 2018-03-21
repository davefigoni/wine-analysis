import flask
from flask import render_template
app = flask.Flask(__name__)
import mapbox
from jinja2 import Template
from jinja2 import Environment
from jinja2.ext import Extension
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
jinja_env = Environment(extensions=['jinja2.ext.do'])

@app.route('/')
def homepage():
	allWine = pd.read_pickle('allWine.pkl')
	allWine = allWine.to_dict('records')
	"""
	wineryinfo = pd.read_pickle('wineryinfo.pkl')
	appellationinfo = pd.read_pickle('appellationinfo.pkl')
	grapeinfo = pd.read_pickle('grapeinfo.pkl')
	wineryinfo = wineryinfo.to_dict('records')
	appellationinfo = appellationinfo.to_dict('records')
	grapeinfo = grapeinfo.to_dict('records')
	"""
	return flask.render_template('winery2.html', allWine=allWine)
	
@app.route('/wineMapAll/')
def wineMapAll():
	return flask.render_template('wineMapAll.html')
	


@app.route('/winecharts/')
def chartpage(chartID = 'chart_ID', chartID2 = 'chart_ID2', chart_type = 'bar',chart_type2 = 'bar', chart_height = 1050,chart_height2 = 1050):
	grapeAvg = pd.read_pickle('grapeCharts.pkl')
	wineryAvg = pd.read_pickle('wineryCharts.pkl')
	glist= []
	gavglist= []
	gbestlist = []
	gworstlist =[]
	wlist= []
	wavglist= []
	wbestlist=[]
	wworstlist=[]
	for w,x,y,z in zip(grapeAvg['Grape'], grapeAvg['Avg Bottle Score for Grape'],grapeAvg['Best Bottle Score for Grape'],grapeAvg['Worst Bottle Score for Grape']):
		glist.append(w)
		gavglist.append(x)
		gbestlist.append(y)
		gworstlist.append(z)
	for a,b,c,d in zip(wineryAvg['Winery'], wineryAvg['Avg Bottle Score for Winery'],wineryAvg['Best Bottle Score for Winery'],wineryAvg['Worst Bottle Score for Winery']):
		wlist.append(a)
		wavglist.append(b)
		wbestlist.append(c)
		wworstlist.append(d)
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	chart2 = {"renderTo": chartID2, "type": chart_type2, "height": chart_height2,}
	series = [{"name": 'Average Score', "data": gavglist, "color": '#e2ceb5', "tooltip": {"valueSuffix": ''}}]
	series2 = [{"name": 'Average Score', "data": wavglist, "color": '#94ba98', "tooltip": {"valueSuffix": ''}}]
	title = {"text": 'Top 40 Grapes with AVA and State'}
	title2 = {"text": 'Top 40 Wineries with AVA and State'}
	xAxis = {"categories": glist, "crosshair": "true"}
	yAxis = {"min":"88"}
	yAxis2 = {"min":"92"}
	xAxis2 = {"categories": wlist, "crosshair": "true"}
	tooltip = {"headerFormat":'<span style="font-size:10px">{point.key}</span><table>', "pointFormat": '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' + '<td style="padding:0"><b>{point.y:.0f} </b></td></tr>', "footerFormat": '</table>', "shared": "true", "useHTML": "true"}
	tooltip2 = {"headerFormat":'<span style="font-size:10px">{point.key}</span><table>', "pointFormat": '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' + '<td style="padding:0"><b>{point.y:.0f} </b></td></tr>', "footerFormat": '</table>', "shared": "true", "useHTML": "true"}	
	return flask.render_template("winecharts.html",chartID=chartID, chart=chart, series=series,
	title=title, xAxis=xAxis, yAxis=yAxis,tooltip=tooltip,
	chartID2=chartID2, chart2=chart2, series2=series2,
	title2=title2, xAxis2=xAxis2,yAxis2=yAxis2, tooltip2=tooltip2)
	

	
	
if __name__ == "__main__":
	app.run(debug=True)