from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

csv = pd.read_csv('temperature.csv', encoding='latin1')

csv = csv[csv['Element'] == 'Temperature change']

years = []
for y in range(1961, 2020):
    years.append([y, csv[f'Y{y}'].mean()])

data = pd.DataFrame(years, columns=['Year', 'Temp'])

@app.route("/", methods=["GET", "POST"])
def home():
    a, b = 1961, 2019
    if request.method == "POST":
        a = int(request.form['start'])
        b = int(request.form['end'])
    
    f = data[(data['Year'] >= a) & (data['Year'] <= b)]
    fig = px.line(f, x='Year', y='Temp', title=f'Глобальное потепление {a}-{b}')
    
    return render_template('index.html', graph=fig.to_html(full_html=False), start=a, end=b)

app.run(debug=True)