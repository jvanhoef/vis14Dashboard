from jbi100_app.main import app
from jbi100_app.data import get_data
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.infoPlots import InfoPlots
from jbi100_app.views.parallelCoordinatePlot import ParallelCoordinatePlot
from jbi100_app.views.personalPlots import PersonalPlots
from jbi100_app.views.sunburstPlot import SunburstPlot
from jbi100_app.views.histogramPlot import HistogramPlot

import dash
from dash import html
from dash import dcc
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
    
    x_labels ={'Payment_of_Min_Amount': 'Payment of Minimum Amount',
                'Behaviour_Spending_Level': 'Behaviour Spending Level',
                'Payment_Behaviour': 'Payment Behaviour',
                'Num_Credit_Card': 'Number of creditcards',
                'Num_Bank_Accounts': 'Number of bank accounts'}
    
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
        x_labels,
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

    # Histogram plot
    HistogramPlot = HistogramPlot(
        "Histogram plot",
        df
    )
    
    app.layout = html.Div(
        children=[
            dcc.Location(id='url', refresh=False),
            html.Div(
                id="app-container",
                children=[
                    # Left column
                    html.Div(
                        id="left-column",
                        className="three columns",
                    ),

                    # Right column
                    html.Div(
                        id="right-column",
                        className="nine columns",
                    )
                ],
            ),
        ]
    )
    
    @app.callback(
        Output('left-column', 'children'),
        [Input('url', 'pathname')]
    )
    def update_left_column(pathname):
        return make_menu_layout(pathname)

    @app.callback(
        Output('right-column', 'children'),
        [Input('url', 'pathname')]
    )
    def update_right_column(pathname):
        if pathname == '/sunburst_personal':
            return html.Div(
                id="sunburst-plot",
                children=[
                    html.H1('Sunburst and Personal Plots Page'),
                    html.Div(
                        id="sunburst-plot",
                        children=[
                            sunburstPlot,
                        ], style={'width': '50%', 'display': 'inline-block'}),
                    html.Div(
                        id="personal-plot",
                        children=[
                            personalPlots,
                        ], style={'width': '50%', 'display': 'inline-block'})
                    ]),
                # Replace with the actual content for the sunburst_personal page
        elif pathname == '/info_plots':
            return html.Div(
                id="sunburst-plot",
                children=[
                    html.H1('Info plots page'),
                    html.P('This is the info plots page, here you can find general information about the distribution of the data'),
                    infoPlots,
                ]
            , )
        elif pathname == '/histogram_plot':
            return html.Div(
                id="histogram-plot",
                children=[
                    html.H1('Histogram plot page'),
                    html.P('This is the histogram plot page, here you can find the distribution of the data'),
                    HistogramPlot,
                ]
            , )
        else:
            return html.Div([
                parallelCoordinatePlot
            ])

    # Callbacks to set colorblindness checks
    @app.callback(
        Output(parallelCoordinatePlot.html_id, "figure"), 
        [ Input('colorblind-checkbox', "value")]
    )
    def update_parallel_coordinates_plot(colorblind_friendly):
        return parallelCoordinatePlot.update_plot(colorblind_friendly)
    
    #updates for personal plots
    @app.callback(
        Output(personalPlots.html_id, 'figure'),
        [Input('age-slider', 'value'),
        Input('income-slider', 'value'),
        Input('occupation-checklist', 'value'),
        Input('behavior-select', 'value'),]
    )
    def update_personal_plots(age_range, income_range, occupations, behavior):
        return personalPlots.update_plot(age_range, income_range, occupations, behavior)        
    
    # @app.callback(
    #     Output('segment-select', 'options'),
    #     Input('subgroup-select', 'value')
    # )
    # # Callback to set segment options based on the selected subgroup
    # def set_segment_options(selected_subgroup):
    #     if selected_subgroup == 'Age':
    #         return [{'label': label, 'value': label} for label in age_groups.keys()]
    #     elif selected_subgroup == 'Income':
    #         return [{'label': label, 'value': label} for label in income_groups.keys()]
    #     elif selected_subgroup == 'Occupation':
    #         return [{'label': label, 'value': label} for label in occupation_groups.keys()]
    #     else:
    #         return []
        
    # # Callbacks to set selection for personal plots
    # @app.callback(
    #     Output(personalPlots.html_id, 'figure'),
    #     [
    #         Input('subgroup-select', 'value'),
    #         Input('segment-select', 'value'),
    #         Input('behavior-select', 'value'),
    #         Input('graph-type-select', 'value')
    #     ]
    # )
    # def update_personal_plots(subgroup, segment, behavior, graph_type):
    #     return personalPlots.update_plot(subgroup, segment, behavior, graph_type)
    
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
    
    @app.callback(
        Output(HistogramPlot.html_id, 'figure'),
        [Input('category-dropdown', 'value')]
    )
    def update_histogram_plot():
        return HistogramPlot.update_plot()
    
    
    app.run_server(debug=False, dev_tools_ui=False, port=8051)
    