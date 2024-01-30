from jbi100_app.main import app
from jbi100_app.data import get_data
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.infoPlots import InfoPlots
from jbi100_app.views.parallelCoordinatePlot import ParallelCoordinatePlot
from jbi100_app.views.personalPlots import PersonalPlots
from jbi100_app.views.sunburstPlot import SunburstPlot

from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
import os
import pandas as pd



if __name__ == '__main__':
    # Create data
    # Check if cleaned_data.csv exists
    if os.path.exists('cleaned_data.csv'):
        df = pd.read_csv('cleaned_data.csv')
    else:
        df = get_data()
    
    #personal options:
    age_groups = {
    '0-17': (0, 17),
    '18-24': (18, 24),
    '25-34': (25, 34),
    '35-44': (35, 44),
    '45-54': (45, 54),
    '55+': (55, df['Age'].max()),
    }

    income_groups = {
        '0-20k': (0, 20000),
        '20k-40k': (20000, 40000),
        '40k-60k': (40000, 60000),
        '60k-80k': (60000, 80000),    
        '80k-100k': (80000, 100000),
        '100k-120k': (100000, 120000),
        '120k-140k': (120000, 140000),
        '140k-160k': (140000, 160000),
        '160k+': (160000, df['Annual_Income'].max()),
    }

    occupation_groups = {
        'Lawyer': 'Lawyer', 
        'Mechanic': 'Mechanic', 
        'Media_Manager': 'Media_Manager', 
        'Doctor': 'Doctor', 
        'Journalist': 'Journalist',
        'Accountant': 'Accountant', 
        'Manager': 'Manager', 
        'Entrepreneur': 'Entrepreneur', 
        'Scientist': 'Scientist', 
        'Architect': 'Architect',
        'Teacher': 'Teacher', 
        'Engineer': 'Engineer', 
        'Writer': 'Writer', 
        'Developer': 'Developer', 
        'Musician': 'Musician'
    }
    # Instantiate plots
    # Parallel coordinate plot:
    dimensions=[
        'Annual_Income',
        'Amount_invested_monthly',
        'Credit_Utilization_Ratio',
        'Num_of_Delayed_Payment',
        'Num_of_Delayed_Payment',
        'Outstanding_Debt',
        'credit_score_mapped' ],

    parallelCoordinatePlot = ParallelCoordinatePlot(
        "Parallel coordinate plot of trends for a certain credit score",
        dimensions,
        df
    )
    
    # Personal plots
    personalPlots = PersonalPlots(
        "Personal plots",
        age_groups,
        income_groups,
        occupation_groups,
        df
    )
    
    # Sunburst plot
    sunburstPlot = SunburstPlot(
        "Sunburst plot",
        df
    )
    
    # Info plot
    infoPlots = InfoPlots(
        "Information plots",
        df
    )
    
    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=make_menu_layout()
            ),

            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=[
                    parallelCoordinatePlot,
                    personalPlots,
                    sunburstPlot,
                    infoPlots
                ],
            ),
        ],
    )
    
    # Callbacks to set colorblindness checks
    @app.callback(
        Output(parallelCoordinatePlot.html_id, "figure"), 
        [ Input('colorblind-checkbox', "value")]
    )
    def update_parallel_coordinates_plot(colorblind_friendly):
        return parallelCoordinatePlot.update_plot(colorblind_friendly)
    
    @app.callback(
        Output('segment-select', 'options'),
        Input('subgroup-select', 'value')
    )
    # Callback to set segment options based on the selected subgroup
    def set_segment_options(selected_subgroup):
        if selected_subgroup == 'Age':
            return [{'label': label, 'value': label} for label in age_groups.keys()]
        elif selected_subgroup == 'Income':
            return [{'label': label, 'value': label} for label in income_groups.keys()]
        elif selected_subgroup == 'Occupation':
            return [{'label': label, 'value': label} for label in occupation_groups.keys()]
        else:
            return []
        
    # Callbacks to set selection for personal plots
    @app.callback(
        Output(personalPlots.html_id, 'figure'),
        [
            Input('subgroup-select', 'value'),
            Input('segment-select', 'value'),
            Input('behavior-select', 'value'),
            Input('graph-type-select', 'value')
        ]
    )
    def update_personal_plots(subgroup, segment, behavior, graph_type):
        return personalPlots.update_plot(subgroup, segment, behavior, graph_type)
    
    # Callback for sunburst graph
    @app.callback(
        Output(component_id=sunburstPlot.html_id,    component_property = 'figure'),
        [
            Input(component_id='personal_slct',     component_property='value'),
            Input(component_id='behavioural_slct',  component_property='value'),
        ]
    )
    def update_sunburst_plot(personal_slct, behavioural_slct):
        return sunburstPlot.update_plot(personal_slct, behavioural_slct)
    
    # Callback for updating the barchart
    @app.callback(
        Output(infoPlots.html_id, 'figure'),
        [Input('category-dropdown', 'value')]
    )
    def update_info_plot(selected_category):
        return infoPlots.update_plot(selected_category)
    
    
    app.run_server(debug=False, dev_tools_ui=False)
    