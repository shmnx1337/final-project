from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import warnings
warnings.filterwarnings('ignore') 

app = Flask(__name__)

def prepare_climate_data():
    raw_data = pd.read_csv('temperature.csv', encoding='latin1')
    
    temp_change_data = raw_data[raw_data['Element'] == 'Temperature change']
    
    yearly_data = []
    
    for year in range(1961, 2020):
        avg_temp = temp_change_data[f'Y{year}'].mean()
        yearly_data.append([year, avg_temp])
  
    return pd.DataFrame(yearly_data, columns=['Year', 'Temp'])

climate_df = prepare_climate_data()

def create_temperature_chart(data, start_year, end_year):
    filtered_data = data[
        (data['Year'] >= start_year) & 
        (data['Year'] <= end_year)
    ]
    
    fig = px.line(
        filtered_data,           
        x='Year',                
        y='Temp',                
        title=f'🌡️ Глобальное изменение температуры ({start_year}-{end_year})',
        labels={
            'Year': '📅 Год',
            'Temp': '🌡️ Температура (°C)'
        },
        template='plotly_dark'   
    )
    
    fig.update_traces(
        line=dict(
            color='#00ffe0',     
            width=3,              
            shape='spline'        
        ),
        mode='lines+markers',     
        marker=dict(
            size=6,               
            color='#00bfff',     
            symbol='circle'       
        )
    )
    
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',   
        plot_bgcolor='rgba(0,0,0,0)',    
        
        
        font=dict(
            family='Arial, sans-serif',
            size=12,
            color='white'
        ),
        
        
        title_font=dict(
            size=20,
            color='#00ffe0',
            family='Arial, sans-serif'
        ),
        
        
        xaxis=dict(
            showgrid=False,              
            showline=True,               
            linecolor='rgba(255,255,255,0.2)',  
            tickfont=dict(size=10),
            title_font=dict(size=12)
        ),
        
        
            yaxis=dict(
            showgrid=True,               
            gridcolor='rgba(255,255,255,0.1)',  
            showline=True,
            linecolor='rgba(255,255,255,0.2)',
            tickfont=dict(size=10),
            title_font=dict(size=12)
        ),
        
        
        hovermode='x unified',           
        hoverlabel=dict(
            bgcolor='rgba(0,0,0,0.8)',
            font_size=12,
            font_family='Arial'
        )
    )
    
    fig.add_hline(
        y=0, 
        line_dash="dash", 
        line_color="rgba(255,255,255,0.3)",
        annotation_text="Нулевая отметка"
    )
    
    return fig

@app.route("/", methods=["GET", "POST"])
def home():
    """
    Обработчик главной страницы
    GET - просто открыть страницу
    POST - пользователь отправил форму с выбором годов
    """
    
    start_year = 1961
    end_year = 2019
    
    if request.method == "POST":
        start_year = int(request.form.get('start', 1961))
        end_year = int(request.form.get('end', 2019))
        
        if start_year > end_year:
            start_year, end_year = end_year, start_year
        
        
        start_year = max(1961, min(2019, start_year))
        end_year = max(1961, min(2019, end_year))
    
    filtered_data = climate_df[
        (climate_df['Year'] >= start_year) & 
        (climate_df['Year'] <= end_year)
    ]
    avg_temperature = round(filtered_data['Temp'].mean(), 2)    
    max_temperature = round(filtered_data['Temp'].max(), 2)      
    years_count = len(filtered_data)                             
    
    min_temperature = round(filtered_data['Temp'].min(), 2)      
    temp_change = round(
        filtered_data['Temp'].iloc[-1] - filtered_data['Temp'].iloc[0], 2
    )  
    
    #ГРАФИК
    figure = create_temperature_chart(climate_df, start_year, end_year)
    
    print(f"📊 Запрошен период: {start_year}-{end_year}")
    print(f"📈 Средняя температура: {avg_temperature}°C")
    print(f"🔥 Максимальная: {max_temperature}°C")
    
    #HTML СТРАНИЦА С ДАННЫМИ
    return render_template(
        'index.html',                    
        start=start_year,                
        end=end_year,                    
        avg=avg_temperature,             
        max=max_temperature,             
        years=years_count,               
        graph=figure.to_html(full_html=False)  
    )

#ЗАПУСК ПРИЛОЖЕНИЯ
if __name__ == '__main__':
    print("=" * 50)
    print("🌍 Climate Dashboard запущен!")
    print("📊 Данные загружены:", len(climate_df), "лет")
    print("🔗 Откройте в браузере: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host='127.0.0.1', port=5000)