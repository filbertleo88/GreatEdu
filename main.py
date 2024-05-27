import streamlit as st
from streamlit_option_menu import option_menu

import home, eda, predict, forecast, about

st.set_page_config(layout='wide',
                    page_icon="😷",
                    page_title="Air Quality Seoul")
    
class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        # Sidebar
        with st.sidebar:     
      
            app = option_menu(
                menu_title='Dashboard',
                options=['Home','EDA','Prediction', 'Forecast','About'],
                icons=['house','bar-chart','alt','activity','info-circle-fill'],
                menu_icon='wind',
                default_index=0,
                styles={
                        "container": {"padding": "5!important","background-color":'black'},
                        "icon": {"color": "white", "font-size": "23px"}, 
                        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                        "nav-link-selected": {"background-color": "#02ab21"},}
                )

        # Menu
        if app == "Home":
            home.app()
        if app == "EDA":
            eda.app()    
        if app == "Prediction":
            predict.app()        
        if app == "Forecast":
            forecast.app()        
        if app == 'About':
            about.app()     
  
    run()            