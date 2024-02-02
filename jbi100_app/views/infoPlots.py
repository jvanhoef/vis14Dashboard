from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import plotly.express as px

class InfoPlots(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        df = df.copy()
        #Adjust the income bins and labels
        income_bins = [0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000, np.inf]
        income_labels = ['0-20k', '20-40k', '40-60k', '60-80k', '80-100k', '100-120k', '120-140k', '140-160k', '160k+']
        df['IncomeGroup'] = pd.cut(df['Annual_Income'], bins=income_bins, labels=income_labels, right=False)

        # Create age groups
        age_bins = [14, 18, 25, 35, 45, 55, 57]  # Creating bins for the age groups
        age_labels = ['14-18', '19-25', '26-35', '36-45', '46-55', '56+']
        df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)

        self.df = df

        # Create all plots
        colors = {'Good': '#FFC20A', 'Poor': '#0C7BDC', 'Standard': '#777777'}
        income_credit_grouped = self.df.groupby(['IncomeGroup', 'Credit_Score']).size().unstack(fill_value=0)
        age_credit_grouped = self.df.groupby(['AgeGroup', 'Credit_Score']).size().unstack(fill_value=0)
        occupation_credit_grouped = self.df.groupby(['Occupation', 'Credit_Score']).size().unstack(fill_value=0)

        income_plot = self.create_plotly_stacked_bar_chart(income_credit_grouped, colors)
        age_plot = self.create_plotly_stacked_bar_chart(age_credit_grouped, colors)
        occupation_plot = self.create_plotly_stacked_bar_chart(occupation_credit_grouped, colors)

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id + '-income', figure=income_plot),
                dcc.Graph(id=self.html_id + '-age', figure=age_plot),
                dcc.Graph(id=self.html_id + '-occupation', figure=occupation_plot),
                dcc.Link('Return to Home', href='/')
            ],
        )
    
    def create_plotly_stacked_bar_chart(self, dataframe, colors):
        self.fig = go.Figure()

        # Calculate the total for each group (row)
        total_per_group = dataframe.sum(axis=1)

        for col in dataframe.columns:
            if col in colors:
                color = colors[col]
            else:
                color = 'grey'

            # Calculate the percentage
            percentage = (dataframe[col] / total_per_group) * 100

            # Adding the trace
            self.fig.add_trace(go.Bar(
                x=dataframe.index,
                y=dataframe[col],
                name=col,
                marker=dict(color=color),
                hovertemplate='%{y} (' + percentage.apply(lambda x: '{0:1.2f}%'.format(x)) + ')<extra></extra>',  # Custom hover text
            ))

        self.fig.update_layout(
            barmode='stack',
            xaxis=dict(title='Category'),
            yaxis=dict(title='Number of Individuals'),
            legend_title='Credit Score'
        )
        return self.fig
    
    def update_plot(self, selected_category):
        colors = {'Good': '#FFC20A', 'Poor': '#0C7BDC', 'Standard': '#777777'}

        if selected_category == 'income':
            # Prepare data for Income Group Plot
            income_credit_grouped = self.df.groupby(['IncomeGroup', 'Credit_Score']).size().unstack(fill_value=0)
            return self.create_plotly_stacked_bar_chart(income_credit_grouped, colors)
        elif selected_category == 'age':
            # Prepare data for Age Group Plot
            age_credit_grouped = self.df.groupby(['AgeGroup', 'Credit_Score']).size().unstack(fill_value=0)
            return self.create_plotly_stacked_bar_chart(age_credit_grouped, colors)
        else:
            # Prepare data for Occupation Plot
            occupation_credit_grouped = self.df.groupby(['Occupation', 'Credit_Score']).size().unstack(fill_value=0)
            return self.create_plotly_stacked_bar_chart(occupation_credit_grouped, colors)
        