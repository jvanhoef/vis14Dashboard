from dash import dcc, html
import pandas as pd
import plotly.express as px

class SunburstPlot(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        df = df.copy()
        ##DATA HANDLING
        #Encoder of credit score
        custom_encoding = {'Good': 2, 'Standard': 1, 'Poor': 0}
        df['Credit_Score_Numeric'] = df['Credit_Score'].map(custom_encoding)

        #Making Agen groups bins
        age_bins = [13, 18, 30, 40, 50, 60]
        age_labels = ["<18",'18-29', '30-39', '40-49', '50-59',]
        df['Age_Group'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)

        #Making bins for annual income
        income_bins =[0,21000,35000,49000,73000,100000,190000]
        income_labels = ['0k-21k', '22k-34k', '35k-48k', '49k-72k', '73k-100k', '100k+']
        df['Income_Group'] = pd.cut(df['Annual_Income'], bins=income_bins, labels=income_labels, right=False, ordered=False)


        # #Making bins for number of delayed payments
        delayed_payment_bins = [0, 1, 3, 9, 13, 16, 19, 29]
        delayed_payment_labels = ['0', '1-2', '3-8', '9-12', '13-15', '16-18', '19+']
        df['delayed_payment_group'] = pd.cut(df['Num_of_Delayed_Payment'], bins=delayed_payment_bins, labels=delayed_payment_labels, right=False)
        
        self.df = df
        
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )
    
    def update_plot(self, personal_slct, behavioural_slct):
        ## clean the data set and remove missing values
        df_clean = self.df.dropna(subset=["Credit_Score"])
        df_clean = df_clean.dropna(subset=[behavioural_slct])
        df_clean = df_clean.dropna(subset=[personal_slct])
        
        # Create new columns that combine the column name and its value
        # Replace underscores with spaces in the column names
        df_clean[personal_slct.replace('_', ' ') + '_new'] = personal_slct.replace('_', ' ') + ': ' + df_clean[personal_slct].astype(str)
        df_clean[behavioural_slct.replace('_', ' ') + '_new'] = behavioural_slct.replace('_', ' ') + ': ' + df_clean[behavioural_slct].astype(str)
        df_clean['Credit Score_new'] = 'Credit Score: ' + df_clean['Credit_Score'].astype(str)
        
        ##create sunburst
        self.fig = px.sunburst(
            data_frame=df_clean,
            path=[personal_slct.replace('_', ' ') + '_new', behavioural_slct.replace('_', ' ') + '_new', 'Credit Score_new'],  # Root, branches, leaves
            color="Credit_Score_Numeric",
            color_continuous_scale=["#94caec", "#dddddd", "#7e2954"],
            range_color=[0,2],
            maxdepth= 2, 
            hover_data=[personal_slct.replace('_', ' ') + '_new', behavioural_slct.replace('_', ' ') + '_new', 'Credit Score_new']  # Add "Credit_Score" to hover_data
        )
        ## choose what text on traces
        self.fig.update_traces(textinfo='label+percent parent', hovertemplate='%{label}')
        self.fig.update_traces(sort=False, selector=dict(type='sunburst')) 

        ## Layout titles  
        self.fig.update_layout(title_text = "Sunburst graph of personal groups and behavioral variables selected in the dropdown.",coloraxis_colorbar_title='Credit Score', margin=dict(t=0, l=0, r=0, b=0))

        return self.fig
    