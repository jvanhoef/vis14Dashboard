import re
import pandas as pd
import numpy as np

def get_data():
# Import the data
    df = pd.read_csv('all_data.csv', delimiter=';')
    pd.set_option('display.max_columns', None)

    # Any further data preprocessing can go here
    # drop Name and SSN columns
    df = df.drop(['Name', 'SSN'], axis=1)

    # Replace all empty cells with NaN in the entire dataframe
    df.replace([None], np.nan, inplace=True)
        
    # First we order the data by Customer_ID and Month. That way we have a nice overview of 12 consecutive data points that belong to a single customer.

    # Order DataFrame by customer id and month
    month_to_num = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 
                    'June': 6, 'July': 7, 'August': 8, 'September': 9, 
                    'October': 10, 'November': 11, 'December': 12}

    df["temp_Month"] = df["Month"].map(month_to_num)
    df.sort_values(["Customer_ID", "temp_Month"], inplace=True)
    df.drop("temp_Month", axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)


    # The numeric columns are cleaned from unwanted (special) characters, and are all transformed into the correct data type.  
    # It was decided that error values of the Occupation column will be replaced by the most occurring value of that customer.  
    # Then certain error values are replaced with a uniform value ("Not available" for strings, Nan for numeric values) so we can easily identify them in the future.  
    # The Payment_Behaviour column is split into two columns. If this is not used in the future, remove from code!

    # Define columns with numeric values
    numeric_column_names = ["Age", "Annual_Income", "Monthly_Inhand_Salary", "Num_Bank_Accounts", 
    "Num_Credit_Card", "Interest_Rate", "Num_of_Loan", "Delay_from_due_date", 
    "Num_of_Delayed_Payment", "Changed_Credit_Limit", "Num_Credit_Inquiries", 
    "Outstanding_Debt", "Credit_Utilization_Ratio", "Total_EMI_per_month", 
    "Amount_invested_monthly", "Monthly_Balance"]

    # Clean numeric columns from unwanted characters 
    special_chars = set()
    special_char_regex = r'[^0-9]'
    for column in numeric_column_names:
        df[column] = df[column].astype(str).str.replace(',', '.').str.replace('_', '') # Perform replacements
        df[column] = pd.to_numeric(df[column], errors='coerce').round(2) # Convert to numeric


    # Custom cleaning for specific columns
    df["Occupation"] = df.groupby("Customer_ID")["Occupation"].transform(lambda x: x.mode()[0] if x.mode().size > 0 else np.nan) # Replaces NaN values with the mode of that customer
    df['Amount_invested_monthly'] = df['Amount_invested_monthly'].replace(10000, np.nan)
    df['Credit_Mix'] = df['Credit_Mix'].replace("_", "Not available")
    df['Payment_of_Min_Amount'] = df['Payment_of_Min_Amount'].replace("NM", "Not available")
    df["Payment_Behaviour"] = df["Payment_Behaviour"].replace("!@9#%8", "Not available")


    # Split 'Payment_Behaviour' column into two new columns
    df[['Behaviour_Spending_Level', 'Behaviour_Value_Size']] = df['Payment_Behaviour'].str.split('_(?=[A-Z])', n=1, expand=True)
    df.loc[df['Payment_Behaviour'] == 'Not available', ['Behaviour_Spending_Level', 'Behaviour_Value_Size']] = 'Not available'

    # Set new columns next to 'Payment_Behaviour'
    pb_index = df.columns.get_loc('Payment_Behaviour')
    df = df[df.columns.tolist()[:pb_index+1] + ['Behaviour_Spending_Level', 'Behaviour_Value_Size'] + df.columns.tolist()[pb_index+1:-2]]

    # In columns where negative values are not allowed/possible, negative values will be replaced by the mode of the positive values of the customer.

    # Define columns with non-negative numeric values
    non_negative_column_names = numeric_column_names.copy()
    non_negative_column_names.remove("Delay_from_due_date")
    non_negative_column_names.remove("Changed_Credit_Limit")

    # Replace negative values  with the mode (of the positive) values of the customer
    for column in non_negative_column_names:
        mode_values = df.groupby('Customer_ID')[column].transform(lambda x: x[x >= 0].mode()[0])
        df.loc[df[column] < 0, column] = mode_values[df[column] < 0]

    # To filter out error/impossible values from certain columns, an upper limit is selected. Every value above this upper limit will be replaced by the mode of the other values of that customer.  
    # It was decided that if a value of a column occurs more than once for a customer, this value is legitimate and thus not an error/impossible value.  
    # By sorting these values for each numeric column (with a few exceptions), the largest value was selected as an upper limit for these columns.  The code below was used to find these limits.  
    # After investigation, it seems like Amount_invested_monthly and Monthly_Balance do not have error values. So it was not needed to assign those columns an upper limit.

    # Uncomment if you want the highest check the highest values of a column
    # def highest_values(column_name):
    #     """
    #     This function will give you the 10 highest values of a column where 
    #     the value appears more than once for a customer.
    #     This will identify the highest values that are most likely not error values.
    #     """
    #     income_counts = df.groupby(['Customer_ID', column_name]).size().reset_index(name='count')
    #     income_counts_filtered = income_counts[income_counts['count'] >= 1]
    #     income_counts_filtered_sorted = income_counts_filtered.sort_values(column_name, ascending=False)
    #     top_10_incomes = income_counts_filtered_sorted.head(10)
    #     print(top_10_incomes)

    # highest_values("Amount_invested_monthly")

    # For the selected columns, the upper limits are defined and any value above those limits are replaced by the mode value of that customer.

    # Replace values above the upper limit with the mode value of that customer
    upper_limit_dict = {"Age": 56, "Annual_Income": 179987.28, "Monthly_Inhand_Salary": 15204.63,
                    "Num_Bank_Accounts": 11, "Num_Credit_Card": 11, "Interest_Rate": 34,
                    "Num_of_Loan": 9, "Delay_from_due_date": 67, "Num_of_Delayed_Payment": 28,
                    "Changed_Credit_Limit": 34.21, "Num_Credit_Inquiries": 17, "Outstanding_Debt": 4998.07,
                    "Credit_Utilization_Ratio": 43.06, "Total_EMI_per_month": 1841.35}

    for column, limit in upper_limit_dict.items():
        # Calculate the mode value for each customer_id in the specified column
        mode_values = df.groupby('Customer_ID')[column].transform(lambda x: x.mode()[0])
        # Replace values above the limit with the corresponding mode value
        df.loc[df[column] > limit, column] = mode_values[df[column] > limit]

    # Credit_History_Age is transformed from its string format to a numeric representation of the total number of months.  
    # After this, the missing values are replaced by the correct ones with the following logic:
    # First, every missing value in January is replaced by the correct value by looking at the subsequent months until a non-NaN value is found. The missing value in January is then calculated based on the found value and the distance between those two months.
    # After this, every value in January is correct, and every subsequent month for each customer can easily be calculated and inserted into the dataset.

    def total_months(str):
        """
        This function will convert a string of the format "{x} years and {y} months" 
        to the total number of months.
        """
        if str is np.nan:
            return np.nan
        
        numbers = re.findall(r'\d+', str)
        if len(numbers) == 2:
            return int(numbers[0]) * 12 + int(numbers[1])
        else:
            return np.nan

    df['Credit_History_Age'] = df['Credit_History_Age'].apply(total_months)

    # Replace missing values with the correct values based on existing data
    for idx in range(len(df)):
        if df.loc[idx, "Month"] == "January":
            if pd.isna(df.loc[idx, "Credit_History_Age"]):
                # If the first month's value is NaN, find the next non-NaN value
                distance = 0
                current_idx = idx
                while current_idx < len(df) and pd.isna(df.loc[current_idx, "Credit_History_Age"]):
                    distance += 1
                    current_idx += 1

                # Calculate the new value for January
                new_value = df.loc[current_idx, 'Credit_History_Age'] - distance
                df.at[idx, 'Credit_History_Age'] = new_value
            
            # Set the starting value for the customer
            starting_value = df.loc[idx, 'Credit_History_Age']
            current_customer_id = df.loc[idx, 'Customer_ID']
            current_idx = idx + 1

            # Increment the value for each subsequent month
            while current_idx < len(df) and df.loc[current_idx, 'Customer_ID'] == current_customer_id:
                starting_value += 1
                df.at[current_idx, 'Credit_History_Age'] = starting_value
                current_idx += 1

    # Finally, the data is stored in a new csv file for easy access. 

    
    df.to_csv('cleaned_data.csv', index=False)
    return df
