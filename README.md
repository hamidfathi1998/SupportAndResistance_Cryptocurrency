# trendln

Support and Resistance Trend lines Calculator for Cryptocurrency Analysis
====================================================================

Note
----

This library can calculate and plot trend lines for any time series.

Please puts your both identify code in credentials.txt [Binance](https://www.binance.com/en/support/faq/360002502072-How-to-create-API)

Formula
----


Quick Start
===========

Calculation Only
----------------

The **calc_support_resistance** function will calculate all support and
resistance information including local extrema, average and their
trend lines using several different methods:

	import trendln
	# this will serve as an example for security or index closing prices, or low and high prices
	from Binance import Binance # requires Binance.py 
	# this will download data from binance
	def donData(symbol,defualt_timeStyle):
	    hist = exchange.GetSymbolKlines(symbol, defualt_timeStyle, defualt_candel)
	    # prepare Data
	    hist.rename(columns={'open':'Open'}, inplace=True)
	    hist.rename(columns={'high':'High'}, inplace=True)
	    hist.rename(columns={'low':'Low'}, inplace=True)
	    hist.rename(columns={'close':'Close'}, inplace=True)
	    hist.rename(columns={'date':'Date'}, inplace=True)
	    hist.set_index('Date', inplace=True)
	    temp = hist['time']
	    hist = hist.assign(volume=hist['time'])
	    del hist['time']
	    hist.rename(columns={'volume':'Time'}, inplace=True)
	    return hist
	fig = trendln.plot_support_resistance(hist.Close,fromwindows=False,title_txt = symbol + " / " + timeframe) 
	# requires matplotlib - pip install matplotlib
	def illustrateChart(fig,ifSave=False,filename="chart",formatC = "svg"):
    		fig.set_size_inches(22, 9)
    		if ifSave:
        		plt.savefig(filename+"."+formatC, format=formatC)
    		plt.show()
    		plt.clf() #clear figure


Documentation for usage:
	fig = trendln.plot_sup_res_date((hist.Low, hist.High),hist[-100:].index,fromwindows=False,title_txt=defualt_timeStyle) # requires matplotlib - pip install matplotlib
        # requires matplotlib - pip install matplotlib
    	illustrateChart(fig) 
	# list/numpy ndarray/pandas Series of data as bool/int/float and if not a list also unsigned
	# or 2-tuple (support, resistance) where support and resistance are 1-dimensional array-like or one or the other is None
	# can calculate only support, only resistance, both for different data, or both for identical data
	
	# you can add in trendln.plot_sup_res_date
		# METHOD_NAIVE - any local minima or maxima only for a single interval (currently requires pandas)
		# METHOD_NAIVECONSEC - any local minima or maxima including those for consecutive constant intervals (currently requires pandas)
		# METHOD_NUMDIFF (default) - numerical differentiation determined local minima or maxima (requires findiff)
		# extmethod = METHOD_NUMDIFF,
		
		# METHOD_NCUBED - simple exhuastive 3 point search (slowest)
		# METHOD_NSQUREDLOGN (default) - 2 point sorted slope search (fast)
		# METHOD_HOUGHPOINTS - Hough line transform optimized for points
		# METHOD_HOUGHLINES - image-based Hough line transform (requires scikit-image)
		# METHOD_PROBHOUGH - image-based Probabilistic Hough line transform (requires scikit-image)
		# method=METHOD_NSQUREDLOGN,
		
		# window size when searching for trend lines prior to merging together
		# window=125,
		
		# maximum percentage slope standard error
		# errpct = 0.005,
		
		# for all METHOD_*HOUGH*, the smallest unit increment for discretization e.g. cents/pennies 0.01
		# hough_scale=0.01,
		
		# only for METHOD_PROBHOUGH, number of iterations to run
		# hough_prob_iter=10,
		
		# sort by area under wrong side of curve, otherwise sort by slope standard error
		# sortError=False,
		
		# accuracy if using METHOD_NUMDIFF for example 5-point stencil is accuracy=3
		# accuracy=1)
	
	# if h is a 2-tuple with one value as None, then a 2-tuple is not returned, but the appropriate tuple instead
	# minimaIdxs - sorted list of indexes to the local minima
	# pmin - [slope, intercept] of average best fit line through all local minima points
	# mintrend - sorted list containing (points, result) for local minima trend lines
		# points - list of indexes to points in trend line
		# result - (slope, intercept, SSR, slopeErr, interceptErr, areaAvg)
			# slope - slope of best fit trend line
			# intercept - y-intercept of best fit trend line
			# SSR - sum of squares due to regression
			# slopeErr - standard error of slope
			# interceptErr - standard error of intercept
			# areaAvg - Reimann sum area of difference between best fit trend line
			#   and actual data points averaged per time unit
	# minwindows - list of windows each containing mintrend for that window
	
	# maximaIdxs - sorted list of indexes to the local maxima
	# pmax - [slope, intercept] of average best fit line through all local maxima points
	# maxtrend - sorted list containing (points, result) for local maxima trend lines
		#see for mintrend above
	# maxwindows - list of windows each containing maxtrend for that window

The **get_extrema** function will calculate all of the local minima and local maxima
without performing the full trend line calculation.
	
	minimaIdxs, maximaIdxs = trendln.get_extrema(hist[-1000:].Close)
	maximaIdxs = trendln.get_extrema((None, hist[-1000:].High)) #maxima only
	minimaIdxs, maximaIdxs = trendln.get_extrema((hist[-1000:].Low, hist[-1000:].High))

Documentation for usage:	

	minimaIdxs, maximaIdxs = trendln.get_extrema(
		h,
		extmethod=METHOD_NUMDIFF,
		accuracy=1)
	# parameters and results are as per defined for calc_support_resistance

Plotting Calculations
---------------------
The **plot_support_resistance** function will calculate and plot the average
and top 2 support and resistance lines, along with marking extrema used with
a maximum history length, and otherwise identical arguments to the
calculation function.

	fig = trendln.plot_support_resistance(hist[-1000:].Close) # requires matplotlib - pip install matplotlib
	plt.savefig('suppres.svg', format='svg')
	plt.show()
	plt.clf() #clear figure
	
Documentation for usage:

	fig = trendln.plot_support_resistance(
		hist, #as per h for calc_support_resistance
		xformatter = None, #x-axis data formatter turning numeric indexes to display output
		  # e.g. ticker.FuncFormatter(func) otherwise just display numeric indexes
		numbest = 2, #number of best support and best resistance lines to display
		fromwindows = True, #draw numbest best from each window, otherwise draw numbest across whole range
		pctbound = 0.1, # bound trend line based on this maximum percentage of the data range above the high or below the low
		extmethod = METHOD_NUMDIFF,
		method=METHOD_NSQUREDLOGN,
		window=125,
		errpct = 0.005,
		hough_prob_iter=10,
		sortError=False,
		accuracy=1)
	# other parameters as per calc_support_resistance
	# fig - returns matplotlib.pyplot.gcf() or the current figure
	
The **plot_sup_res_date** function will do the same as **plot_support_resistance** with
help for nice formatting of dates based on a pandas date index.
	
	idx = hist[-1000:].index
	fig = trendln.plot_sup_res_date((hist[-1000:].Low, hist[-1000:].High), idx) #requires pandas
	plt.savefig('suppres.svg', format='svg')
	plt.show()
	plt.clf() #clear figure
	
Documentation for usage:

	fig = trendln.plot_sup_res_date( #automatic date formatter based on US trading calendar
		hist, #as per h for calc_support_resistance
		idx, #date index from pandas
		numbest = 2,
		fromwindows = True,
		pctbound = 0.1,
		extmethod = METHOD_NUMDIFF,
		method=METHOD_NSQUREDLOGN,
		window=125,
		errpct = 0.005,
		hough_scale=0.01,
		hough_prob_iter=10,
		sortError=False,
		accuracy=1)
	# other parameters as per plot_support_resistance

Finally, for the above mentioned article, some figures were generated for reference material,
while others use the library to demonstrate how it works.  These can be generated as well:
	
	trendln.plot_sup_res_learn('.', hist)

Documentation for usage:

	trendln.plot_sup_res_learn( #draw learning figures, included for reference material only
		curdir, #base output directory for png and svg images, will be saved in 'data' subfolder
		hist) #pandas DataFrame containing Close and date index
	
![Example output of plotting support resistance](https://github.com/hamidfathi1998/SupportAndResistance_Cryptocurrency/blob/main/chart.svg)


Requirements
------------


* [Python](https://www.python.org) >= 2.7, 3.4+
* [pandas](https://github.com/pydata/pandas) >= 0.23.1 (if using date plotting function, or using naive minima/maxima methods)
* [matplotlib](https://matplotlib.org) >= 2.2.4 (if using any plotting function)
* [numpy](http://www.numpy.org) >= 1.15
* [findiff](https://github.com/maroba/findiff) >= 0.7.0 (if using default numerical differentiation method)
* [scikit-image](https://scikit-image.org) >= 0.14.0 (if using image-based Hough line transform or its probabilistic variant)



Support
-------

Any questions, issues or ideas can kindly be submitted for review.

**Hamid Fathi**
<hamid.fathi.developer@gmail.com>
