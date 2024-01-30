from dash import dcc, html
from ..config import color_list1, color_list2


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
        ], style={"textAlign": "float-left"}
    )


def make_menu_layout():
    return [generate_description_card(), generate_control_card()]
