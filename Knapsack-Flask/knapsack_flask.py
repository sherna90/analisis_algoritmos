from flask import *
import pandas as pd
import os
import re
app = Flask(__name__)

filename='portfolio.xlsx'
data = [pd.read_excel(filename,sheet_name=i,header=1) for i in range(5)]
    
@app.route("/")
def show_tables():
    df = data[0].fillna('')
    weights=df.columns[1:7].get_values()
    values=df.columns[7:14].get_values()
    return render_template('index.html')



@app.route('/optimize', methods= ['POST'])
def optimize():
    period = int(request.form['period'])
    weight = int(request.form['weight'])
    value = int(request.form['value'])
    df = data[period].fillna('')
    df=df[[df.columns[weight],df.columns[value]]]
    return render_template('optimize.html',tables=[re.sub(' mytable', '" id="example', df.to_html(classes='mytable'))],
    titles = ['Portfolio Optimization'])


if __name__ == "__main__":
    app.run(debug=True)
