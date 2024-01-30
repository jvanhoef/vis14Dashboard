from dash import dcc, html
import pandas as pd
import plotly.express as px

class PersonalPlots(html.Div):
    def __init__(self, name, age_groups, income_groups, occupation_groups, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.age_groups = age_groups
        self.income_groups = income_groups
        self.occupation_groups = occupation_groups
                
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )
        
    # Callback to update the bar plot based on the selected options
    def update_plot(self, subgroup, segment, behavior, graph_type):
        if graph_type == 'heatmap':
            # Binning and then converting intervals to strings for JSON serialization
            if subgroup == 'Age':
                bins = pd.IntervalIndex.from_tuples(list(self.age_groups.values()))
                age_bins = pd.cut(self.df['Age'], bins=bins)
                self.df['Age_Bin'] = age_bins.apply(lambda x: f'{x.left}-{x.right}')
                pivot_column = 'Age_Bin'
            elif subgroup == 'Income':
                bins = pd.IntervalIndex.from_tuples(list(self.income_groups.values()))
                income_bins = pd.cut(self.df['Annual_Income'], bins=bins)
                self.df['Income_Bin'] = income_bins.apply(lambda x: f'{x.left}-{x.right}')
                pivot_column = 'Income_Bin'
            elif subgroup == 'Occupation':
                pivot_column = 'Occupation'
            
            # Group by the pivot column and credit score to get the count
            heatmap_data = self.df.groupby([pivot_column, 'Credit_Score']).size().unstack(fill_value=0)

            # heatmap_data = heatmap_data[]

            # Ensure all expected credit score categories are present
            heatmap_data = heatmap_data.reindex(['Good', 'Standard', 'Poor'], axis=1, fill_value=0)

            # Use imshow from plotly express to generate the heatmap
            self.fig = px.imshow(heatmap_data, aspect='auto', 
                            color_continuous_scale='Viridis')  # Or any other color scale you prefer

            # Update layout to have more meaningful axis titles
            self.fig.update_layout(
                xaxis_title="Credit Score",
                yaxis_title=subgroup,
                yaxis=dict(type='category'),
                xaxis=dict(type='category')
            )
            self.fig.update_xaxes(side="bottom")
            return self.fig

        if subgroup == 'Age':
            age_range = self.age_groups.get(segment, (0, 0))
            filtered_data = self.df[(self.df['Age'] >= age_range[0]) & (self.df['Age'] <= age_range[1])]
        elif subgroup == 'Income':
            income_range = self.income_groups.get(segment, (0, 0))
            filtered_data = self.df[(self.df['Annual_Income'] >= income_range[0]) & (self.df['Annual_Income'] <= income_range[1])]
        elif subgroup == 'Occupation':
            occupation = self.occupation_groups.get(segment)
            filtered_data = self.df[(self.df['Occupation'] == occupation)]
        else:
            filtered_data = self.df

        # Define custom colors for clarity
        custom_colors = ['#2ca02c', '#fa9c1b', '#d62728'] # Green for Good, Blue for Standard, Red for Poor

        # Specify the order of the categories
        category_order = {'Credit_Score': ['Good', 'Standard', 'Poor']}

        if graph_type == 'bar':
            filtered_data = filtered_data[filtered_data[behavior] != "Not available"]
            self.fig = px.histogram(filtered_data, x=behavior, color='Credit_Score', color_discrete_sequence=custom_colors, category_orders=category_order)
        elif graph_type == 'box':
            self.fig = px.box(filtered_data, x=behavior, y='Credit_Score', color='Credit_Score', color_discrete_sequence=custom_colors, category_orders=category_order)
        
        return self.fig
    