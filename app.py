from flask import Flask, render_template, request, redirect
#from bokeh.plotting import figure,show
#from bokeh.io import output_notebook
#from bokeh.resources import CDN
#from bokeh.embed import file_html
#from bokeh.embed import components

app = Flask(__name__)

app.vars={}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    #nquestions=5
    if request.method == 'GET':
        return render_template('main.html')
    else:
        #request was a POST
        app.vars['ticker'] = request.form['ticker']
        if request.form.get('Close'):
            app.vars['Close'] = 1
        else : app.vars['Close'] = 0
        if request.form.get('Adj. Close'):
            app.vars['AdjClose'] = 1
        else : app.vars['AdjClose'] = 0
        if request.form.get('Open'):
            app.vars['Open'] = 1
        else : app.vars['Open'] = 0
        if request.form.get('Adj. Open'):
            app.vars['AdjOpen'] = 1
        else : app.vars['AdjOpen'] = 0
        #app.vars['Close'] = request.form.get('Close')
        #app.vars['AdjClose'] = request.form['Adj. Close']
        #app.vars['Open'] = request.form['Open']
        #app.vars['AdjOpen'] = request.form['Adj. Open']
        
        
        f = open('info.txt','w')
        f.write('Ticker: %s\n'%(app.vars['ticker']))
        f.write('Close: %s\n'%(app.vars['Close']))
        f.write('Adjusted Close: %s\n'%(app.vars['AdjClose']))
        f.write('Open: %s\n'%(app.vars['Open']))
        f.write('Adjuseted Open: %s\n'%(app.vars['AdjOpen']))
        
        f.close()
        
        




        x=app.vars['ticker']
        C=app.vars['Close']
        AC=app.vars['AdjClose']
        O=app.vars['Open']
        AO=app.vars['AdjOpen']


        y='WIKI/%s'%(x)
        mydata = Quandl.get(y, authtoken="nWMHwtzyAfUAE9nJPZ82",rows=30)
        NumLines=C+AC+O+AO

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

        p = bokeh.plotting.figure(title="%s Stock Ticks"%(x),x_axis_type="datetime", plot_width=500, plot_height=500)
        for name in calls:
            p.line(mydata.index.values,mydata[name].values,
                legend=name,
                line_color=colors[name],
                line_width=3)

        #plot = file_html(p, CDN, "my plot")

        script, div = bokeh.embed.components(p)
    
        return render_template('end.html',plotscript=script,plotdiv=div)


if __name__ == '__main__':
  app.run(host='0.0.0.0')
