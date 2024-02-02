from dash import dcc, html
import pandas as pd
import plotly.express as px

class HistogramPlot(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
                
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )
        
    # Callback to update the bar plot based on the selected options
    def update_plot(self):
        
        numeric_change_counts = self.df['Numeric_Credit_Change'].value_counts()
        numeric_change_counts /= 8  # There are 8 values per customer
        order = [-2, -1, 0, 1, 2]
        numeric_change_counts = numeric_change_counts.reindex(order, fill_value=0)

        # new dataframe column for change in credit score
        customer_credit_change = self.df.groupby('Customer_ID')['Credit_Score_Change'].value_counts().unstack(fill_value=0)
        customer_credit_change['Numeric_Credit_Change'] = customer_credit_change['Improvement'] - customer_credit_change['Decline']

        # Merge the calculated numeric change back into the original DataFrame
        self.df = self.df.merge(customer_credit_change[['Numeric_Credit_Change']], left_on='Customer_ID', right_index=True)

        # Plotting with normalized counts
        self.fig = px.bar(self.df, 
                          x='Numeric Credit Score Change',
                          y='Average Count',
                          title='Average Distribution of Numeric Credit Score Change'
        )

        return self.fig
        