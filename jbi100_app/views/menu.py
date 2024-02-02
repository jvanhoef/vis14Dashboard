from dash import dcc, html
from ..config import color_list1, color_list2
import pandas as pd

data = pd.read_csv('cleaned_data.csv')
def generate_description_home():
    """

    :return: A Div containing dashboard title & descriptions for the personal plots.
    """
    return html.Div(
        id="description-card-personal",
        children=[
            html.H5("Dashboard options"),
            html.Div(
                id="intro-personal",
                children="Here you can select your preferences for the visualisation and you can navigate to other pages. ",
            ),
        ],
    )
def generate_description_personal():
    """

    :return: A Div containing dashboard title & descriptions for the personal plots.
    """
    return html.Div(
        id="description-card-personal",
        children=[
            html.H5("Dashboard options"),
            html.Div(
                id="intro-personal",
                children="Here you can select different preferences and visualisations to learn more about how you can improve your credit score!. The selection of the sunburst_plot will also change the selection of the personal plots",
            ),
        ],
    )
    
def generate_description_info():
    """

    :return: A Div containing dashboard title & descriptions for the personal plots.
    """
    return html.Div(
        id="description-card-info",
        children=[
            html.H5("Dashboard options"),
            html.Div(
                id="intro-info",
                children="Here you can select your preferences for the style of the information graphs.",
            ),
        ],
    )

def generate_control_home():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.Label("Colorblind friendly colors"),
            dcc.Checklist(
                id='colorblind-checkbox',
                options=[{'label': 'Use colorblind-friendly color scale', 'value': 'CB'}],
                value=[]
            ),
            html.Div([
                dcc.Link(
                    'Sunburst and Personal Plots',
                    href='/sunburst_personal',
                    refresh=True,
                    style={
                        'marginRight': '10px',
                        'padding': '10px',
                        'backgroundColor': '#f0f0f0',
                        'border': '1px solid #000',
                        'display': 'inline-block'
                    }
                ),
                dcc.Link(
                    'Info Plots',
                    href='/info_plots',
                    refresh=True,
                    style={
                        'marginLeft': '10px',
                        'padding': '10px',
                        'backgroundColor': '#f0f0f0',
                        'border': '1px solid #000',
                        'display': 'inline-block'
                    }
                )
            ], style={'textAlign': 'float-left'})
        ]
    )

def generate_control_personal():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.Label("Colorblind friendly colors"),
            dcc.Checklist(
                id='colorblind-checkbox',
                options=[{'label': 'Use colorblind-friendly color scale', 'value': 'CB'}],
                value=[]
            ),
            html.Div([
                "Age Range:",
                dcc.RangeSlider(
                    id='age-slider',
                    min=data['Age'].min(),
                    max=data['Age'].max(),
                    step=1,
                    value=[data['Age'].min(), data['Age'].max()],
                    marks={i: str(i) for i in range(15, 55 + 1, 5)}
                ),
            ], style={'padding': 20}),

            html.Div([
                "Income Range:",
                dcc.RangeSlider(
                    id='income-slider',
                    min=data['Annual_Income'].min(),
                    max=data['Annual_Income'].max(),
                    step=1000,
                    value=[data['Annual_Income'].min(), data['Annual_Income'].max()],
                    marks={
                        0: '${:,.0f}'.format(0),
                        30000: '${:,.0f}'.format(30000),
                        60000: '${:,.0f}'.format(60000),
                        90000: '${:,.0f}'.format(90000),
                        120000: '${:,.0f}'.format(120000),
                        150000: '${:,.0f}'.format(150000),
                        180000: '${:,.0f}'.format(180000)
                    }                ),
            ], style={'padding': 20}),

            html.Div([
                "Occupation:",
                dcc.Checklist(
                    id='occupation-checklist',
                    options=[{'label': i, 'value': i} for i in data['Occupation'].unique()],
                    value=data['Occupation'].unique().tolist(),
                    inline=True
                ),
            ], style={'padding': 20}),

            dcc.Dropdown(
                id='behavior-select',
                options=[
                    {'label': 'Payment of Minimum Amount', 'value': 'Payment_of_Min_Amount'},
                    {'label': 'Behaviour Spending Level', 'value': 'Behaviour_Spending_Level'},
                    {'label': 'Payment Behaviour', 'value': 'Payment_Behaviour'},
                    {'label': 'Number of creditcards', 'value': 'Num_Credit_Card'},
                    {'label': 'Number of bank accounts', 'value': 'Num_Bank_Accounts'}
                ],
                value='Num_Credit_Card'
            ),
            html.Div(
                dcc.Link(
                    'Home',
                    href='/',
                    refresh=True,
                    style={
                        'marginRight': '10px',
                        'padding': '10px',
                        'backgroundColor': '#f0f0f0',
                        'border': '1px solid #000',
                        'display': 'inline-block'
                    }
                ), style={"textAlign": "float-left"})
        ]
    )
    
def generate_control_info():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.Label("Colorblind friendly colors"),
            dcc.Checklist(
                id='colorblind-checkbox',
                options=[{'label': 'Use colorblind-friendly color scale', 'value': 'CB'}],
                value=[]
            ),
            html.Div(
                dcc.Link(
                    'Home',
                    href='/',
                    refresh=True,
                    style={
                        'marginRight': '10px',
                        'padding': '10px',
                        'backgroundColor': '#f0f0f0',
                        'border': '1px solid #000',
                        'display': 'inline-block'
                    }
                ), style={"textAlign": "float-left"})
        ]
    )
    
def make_menu_layout(pathname):
    if pathname == '/sunburst_personal':
        return [generate_description_personal(), generate_control_personal()]
    
    elif pathname == '/info_plots':
        return [generate_description_info(), generate_control_info()]
    else:
        return [generate_description_home(), generate_control_home()]


