from dash import dcc, html
from ..config import color_list1, color_list2
import pandas as pd

data = pd.read_csv('cleaned_data.csv')
# Define the age and income groups

def generate_description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Dashboard options"),
            html.Div(
                id="intro",
                children="Here you can select different preferences and visualisations to learn more about how you can improve your credit score!.",
            ),
        ],
    )


def generate_control_card():
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
                dcc.Dropdown(
                id='subgroup-select',
                options=[
                    {'label': 'Age', 'value': 'Age'},
                    {'label': 'Income', 'value': 'Income'},
                    {'label': 'Occupation', 'value': 'Occupation'}
                    # Add other subgroups as needed
                ],
                value='Age'  # Default value
            ),
            dcc.Dropdown(
                id='segment-select',
                # Options will be set based on the callback
            ),
            dcc.Dropdown(
                id='behavior-select',
                options=[
                    {'label': 'Payment of Minimum Amount', 'value': 'Payment_of_Min_Amount'},
                    {'label': 'Behaviour Spending Level', 'value': 'Behaviour_Spending_Level'},
                    {'label': 'Payment Behaviour', 'value': 'Payment_Behaviour'},
                    {'label': 'Number of creditcards', 'value': 'Num_Credit_Card'},
                    {'label': 'Number of bank accounts', 'value': 'Num_Bank_Accounts'}
                    # Add other behaviors as needed
                ],
                value='Payment_of_Min_Amount'  # Default value
            ),
            dcc.Dropdown(
                id='graph-type-select',
                options=[
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Box Plot', 'value': 'box'},
                    {'label': 'Heatmap', 'value': 'heatmap'}
                ],
                value='bar'  # Default graph type
            ),
            dcc.Dropdown(id='personal_slct',
                options=[
                    {'label': 'Age', 'value': 'Age_Group'},
                    {'label': 'Occupation', 'value': 'Occupation'},
                    {'label': 'Income group', 'value': 'Income_Group'},
                ],
                value='Age_Group', # Default value                                        
            ), 
            dcc.Dropdown(
                id='behavioural_slct',
                options=[
                    {'label': 'Number of delayed payments', 'value': 'delayed_payment_group'},
                    {'label': 'Spending level', 'value': 'Behaviour_Spending_Level'},
                    {'label': 'Value size of payments', 'value': 'Behaviour_Value_Size'},
                ],
                value='delayed_payment_group',                   
            )
        ], style={"textAlign": "float-left"}
    )
    
def make_menu_layout():
    return [generate_description_card(), generate_control_card()]
