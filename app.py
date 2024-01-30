from jbi100_app.main import app
from jbi100_app.data import get_data
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.parallelCoordinatePlot import ParallelCoordinatePlot

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
    
    # Instantiate plots
    dimensions=[
        'Annual_Income',
        'Amount_invested_monthly',
        'Credit_Utilization_Ratio',
        'Num_of_Delayed_Payment',
        'Num_of_Delayed_Payment',
        'Outstanding_Debt',
        'credit_score_mapped' ],

    parallelCoordinatePlot = ParallelCoordinatePlot(
        "Parellel coordinate plot of trends for a certain credit score",
        dimensions,
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
                    parallelCoordinatePlot
                ],
            ),
        ],
    )

    # # Define interactions
    # @app.callback(
    #     Output(parallelCoordinatePlot.html_id, "figure"), [
    #     Input("select-color-scatter-1", "value"),
    #     Input(scatterplot2.html_id, 'selectedData')
    # ])
    # def update_scatter_1(selected_color, selected_data):
    #     return scatterplot1.update(selected_color, selected_data)

    # @app.callback(
    #     Output(scatterplot2.html_id, "figure"), [
    #     Input("select-color-scatter-2", "value"),
    #     Input(scatterplot1.html_id, 'selectedData')
    # ])
    # def update_scatter_2(selected_color, selected_data):
    #     return scatterplot2.update(selected_color, selected_data)
    
    @app.callback(
        Output(parallelCoordinatePlot.html_id, "figure"), [
        Input('colorblind-checkbox', "value")
    ])
    def update_parallel_coordinates_plot(colorblind_friendly):
        return parallelCoordinatePlot.update_plot(colorblind_friendly)


    app.run_server(debug=False, dev_tools_ui=False)