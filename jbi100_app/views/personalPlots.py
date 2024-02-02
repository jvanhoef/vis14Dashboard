from dash import dcc, html
import pandas as pd
import plotly.express as px

class PersonalPlots(html.Div):

    def __init__(self, name, x_labels, df):
        data = pd.read_csv('cleaned_data.csv')
        
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.x_labels = x_labels
        self.income_range = [data['Annual_Income'].min(), data['Annual_Income'].max()]
        self.occupations = [{'label': i, 'value': i} for i in data['Occupation'].unique()]
        self.behavior = 'Num_Credit_Card'
                
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )
        
    # Callback to update the bar plot based on the selected options
    def update_plot(self, age_range, income_range, occupations, behavior):
        # Filter data based on inputs
        filtered_data = self.df[
            (self.df['Age'] >= age_range[0]) & (self.df['Age'] <= age_range[1]) &
            (self.df['Annual_Income'] >= income_range[0]) & (self.df['Annual_Income'] <= income_range[1]) &
            (self.df['Occupation'].isin(occupations))
        ]
        self.income_range = income_range
        self.occupations = occupations
        self.behavior = behavior

        # Define custom colors for clarity
        custom_colors = ['#2ca02c', '#d62728'] # Green for Good, Blue for Standard, Red for Poor

        filtered_data = filtered_data[filtered_data[behavior] != "Not available"]
        filtered_data['Good_Standard'] = filtered_data['Credit_Score'].apply(lambda x: 'Good_Standard' if x in ['Good', 'Standard'] else 'Poor')
        counts = filtered_data.groupby([behavior, 'Good_Standard']).size().reset_index(name='counts')

        # Pivot the data to have 'Good_Standard' and 'Poor' side by side
        pivot_data = counts.pivot(index=behavior, columns='Good_Standard', values='counts').fillna(0)

        # Normalize the counts to show proportions
        pivot_data['total'] = pivot_data.sum(axis=1)
        for col in pivot_data.columns[:-1]:  # Exclude the total column
            pivot_data[col] = pivot_data[col] / pivot_data['total']

        # Reset index to make 'behavior' a column again for plotting
        pivot_data.reset_index(inplace=True)

        # Plotting with normalized counts
        self.fig = px.bar(pivot_data, x=behavior, y=['Good_Standard', 'Poor'], title=f"Good+Standard to Poor Ratio by {self.x_labels[behavior]}",
                        labels={'value': 'Normalized Credit Score', behavior:  self.x_labels[behavior]}, 
                        color_discrete_sequence=custom_colors)

        self.fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
        return self.fig
    
    def update_age(self, selected_age_bin):
        age_range = selected_age_bin.split(":")[1].strip()
        # Split the age range on the dash to get the two ages
        age1, age2 = map(int, age_range.split("-"))
        print([age1, age2], self.income_range, self.occupations, self.behavior)
        self.update_plot([age1, age2], self.income_range, self.occupations, self.behavior)
        