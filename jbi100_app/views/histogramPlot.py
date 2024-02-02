from dash import dcc, html
import pandas as pd
import plotly.express as px

class HistogramPlot(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        
        df = df.copy()

        # Create a function to categorize the change
        def credit_score_change(row):
            if row['Credit_Score'] == row['Previous_Score']:
                return 'No Change'
            elif row['Credit_Score'] == 'Poor' and row['Previous_Score'] == 'Standard':
                return 'Decline'
            elif row['Credit_Score'] == 'Poor' and row['Previous_Score'] == 'Good':
                return 'Decline'
            elif row['Credit_Score'] == 'Standard' and row['Previous_Score'] == 'Good':
                return 'Decline'
            elif row['Credit_Score'] == 'Good' and row['Previous_Score'] == 'Poor':
                return 'Improvement'
            elif row['Credit_Score'] == 'Good' and row['Previous_Score'] == 'Standard':
                return 'Improvement'
            elif row['Credit_Score'] == 'Standard' and row['Previous_Score'] == 'Poor':
                return 'Improvement'
            else:
                return 'No Change'

        # Create a shifted version of the credit score column
        df['Previous_Score'] = df.groupby('Customer_ID')['Credit_Score'].shift(1)

        # Apply the function to categorize each change
        df['Credit_Score_Change'] = df.apply(credit_score_change, axis=1)
        
        # new dataframe column for change in credit score
        customer_credit_change = df.groupby('Customer_ID')['Credit_Score_Change'].value_counts().unstack(fill_value=0)
        customer_credit_change['Numeric_Credit_Change'] = customer_credit_change['Improvement'] - customer_credit_change['Decline']

        # Merge the calculated numeric change back into the original DataFrame
        df = df.merge(customer_credit_change[['Numeric_Credit_Change']], left_on='Customer_ID', right_index=True)

        numeric_change_counts = customer_credit_change['Numeric_Credit_Change'].value_counts()
        numeric_change_counts /= 8  # There are 8 values per customer
        order = [-2, -1, 0, 1, 2]
        numeric_change_counts = numeric_change_counts.reindex(order, fill_value=0)

        # Convert to DataFrame for Plotly
        numeric_change_df = numeric_change_counts.reset_index()
        numeric_change_df.columns = ['Numeric Credit Score Change', 'Average Count']

        self.numeric_change_df = numeric_change_df
                
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
        # Plotting with normalized counts
        self.fig = px.bar(self.numeric_change_df, 
                          x='Numeric Credit Score Change',
                          y='Average Count',
                          title='Average Distribution of Numeric Credit Score Change'
        )

        return self.fig
        