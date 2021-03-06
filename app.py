from flask import Flask, render_template, request, redirect
import requests
import simplejson as json
import pandas
#from Quandl import get
#import Quandl
#from quandl import Quandl
import bokeh
from bokeh.plotting import figure,show
#from bokeh.io import output_notebook
#from bokeh.resources import CDN
#from bokeh.embed import file_html
from bokeh.embed import components

app = Flask(__name__)

var={}

@app.route('/')
def main():
    return redirect('/index')

#@app.route('/index')
#def index():
#    return render_template('index.html')


@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        #request was a POST
        var['ticker'] = request.form['ticker']
        if request.form.get('Close'):
            var['Close'] = 1
        else : var['Close'] = 0
        if request.form.get('Adj. Close'):
            var['AdjClose'] = 1
        else : var['AdjClose'] = 0
        if request.form.get('Open'):
            var['Open'] = 1
        else : var['Open'] = 0
        if request.form.get('Adj. Open'):
            var['AdjOpen'] = 1
        else : var['AdjOpen'] = 0
        
        

        stock=var['ticker']
        C=var['Close']
        AC=var['AdjClose']
        O=var['Open']
        AO=var['AdjOpen']

	api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock
	session = requests.Session()
	session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))

	raw_data = session.get(api_url)

	try:
		mydata_full = pandas.DataFrame.from_dict(raw_data.json()['data'])
	except:
		return render_template('index-2.html',stock=stock)
	mydata=mydata_full[:25]
	mydata.columns=raw_data.json()['column_names']
	mydata['Date'] = mydata['Date'].astype('datetime64')

#        api_url_csv = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.csv' % stock
#        mydata = pandas.read_csv(api_url_csv)	
#        y='WIKI/%s'%(stock)
#        mydata = Quandl.get(y, authtoken="nWMHwtzyAfUAE9nJPZ82",rows=30)
#        mydata = Quandl.get(y,rows=30)
        NumLines=C+AC+O+AO
	if NumLines == 0 : C=1

        colors={}
        colors['Close']="red"
        colors['Adj. Close']="yellow"
        colors['Open']="green"
        colors['Adj. Open']="blue"

        calls=[]
        if C==1 : calls.append('Close')
        if AC==1 : calls.append('Adj. Close')
        if O==1 : calls.append('Open')
        if AO==1 : calls.append('Adj. Open')

        p = figure(title="%s Stock Ticks"%(stock),x_axis_type="datetime",x_axis_label='date',y_axis_label='value', plot_width=500, plot_height=500)
        for name in calls:
            p.line(mydata['Date'],mydata[name].values,
                legend=name,
                line_color=colors[name],
                line_width=1)

#        #plot = file_html(p, CDN, "my plot")

        script, div = components(p)
    
        return render_template('end.html',plotscript=script,plotdiv=div,stock=stock)
#	return render_template('end.html')

#if __name__ == '__main__':
#    app.run()
#    app.run(host='0.0.0.0')

#from flask import Flask, render_template, request, redirect

#app = Flask(__name__)

#@app.route('/')
#def main():
#  return redirect('/index')

#@app.route('/index')
#def index():
#  return render_template('index.html')

if __name__ == '__main__':
	app.run(port=33507)
#    app.run(debug=True)
