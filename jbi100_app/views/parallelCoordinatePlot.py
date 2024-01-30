from dash import dcc, html
import pandas as pd
import plotly.express as px
from sklearn.model_selection import StratifiedShuffleSplit

class ParallelCoordinatePlot(html.Div):
    def __init__(self, name, dimensions, df):
        self.html_id = name.lower().replace(" ", "-")
        
        # Do some preprocessing specific for the parallel coordinate plot
        df = df.copy()
        # Define the aggregation functions for each column
        aggregations = {col: 'mean' if df[col].dtype == 'float64' else 'first' for col in df.columns.drop('Customer_ID')}

        # Group by 'Customer_ID' and aggregate
        df_grouped= df.groupby('Customer_ID').agg(aggregations).reset_index()

        # The 3 credit score categories
        credit_categories = ['Poor', 'Standard', 'Good']
        
        # Convert the 'credit_score' column to a categorical type
        credit_score_categorical = pd.Categorical(df_grouped['Credit_Score'], categories=credit_categories, ordered=True)

        # Add a new column that contains the integer codes of the 'credit_score' column
        df_grouped['credit_score_mapped'] = credit_score_categorical.codes
        
        # Get a random smaller split of the data where the split between the credit scores is kept
        # the same as it is in the complete dataset
        # Define the stratified shuffle split
        sss = StratifiedShuffleSplit(n_splits=100, test_size=0.05, random_state=0)

        # Get the indices for the rows to keep
        for _, index in sss.split(df_grouped, df_grouped['Credit_Score']):
            df_sample = df_grouped.loc[index]

        self.df = df_sample
        self.dimensions = dimensions
        
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                html.Div(
                    id="coordinate graph description",
                    children='In this graph you can see the general trends of people that have a certain level of credit score, You can see that when all the lines of one color are close together, that this variable will probably be a big influence on the final credit score. '),
                dcc.Graph(id=self.html_id)
            ],
        )
        
    def update_plot(self, colorblind_friendly):
        # The 3 credit score categories
        credit_categories = ['Poor', 'Standard', 'Good']
        
        color_scale = px.colors.sequential.Cividis if 'CB' in colorblind_friendly else px.colors.diverging.Tealrose

        self.fig = px.parallel_coordinates(
            self.df,
            color='credit_score_mapped',
            dimensions=['Annual_Income', 'Amount_invested_monthly', 'Credit_Utilization_Ratio', 'Num_of_Delayed_Payment', 'Num_of_Delayed_Payment', 'Outstanding_Debt', 'credit_score_mapped' ],
            color_continuous_scale=color_scale,
            color_continuous_midpoint=1,
            range_color=[0, 2], # Set the color map to go from 0 to 2
            labels={'credit_score_mapped': 'Credit Score'}
        )  

        # Update color bar ticks to category labels
        self.fig.update_coloraxes(colorbar=dict(
            tickvals=[0, 1, 2],
            ticktext=credit_categories
        ))

        return self.fig