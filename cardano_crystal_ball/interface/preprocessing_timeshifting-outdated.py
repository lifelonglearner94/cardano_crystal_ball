import pandas as pd
import numpy as np

def make_timesteps(df, number_of_steps=120): #120h = 5 days
    """
    Generate time step features for a given dataframe.

    Args:
        df (DataFrame): The dataframe containing the data.
        number_of_steps (int, optional): Number of time steps to generate. Defaults to 120 / 5 days.

    Returns:
        DataFrame: Dataframe with time step features.
    """
    #Assumes that there is a column called target with the y value

    #Exclude target
    columns_to_apply_operation = df.columns.difference(['target'])

    #Making the first timeshift
    first_col_names_next_timestep = [f"{col_name}_t-1" for col_name in columns_to_apply_operation]
    df[first_col_names_next_timestep] = df[columns_to_apply_operation].shift()

    #Drop unnecessary columns
    df = df.drop(columns=columns_to_apply_operation)

    previous_col_names = first_col_names_next_timestep

    for timestep in range(2, number_of_steps+1):
        #Making all the timeshifts
        df = df.copy()
        new_col_names_next_timestep = [f"{col_name}_t-{timestep}" for col_name in columns_to_apply_operation]

        df[new_col_names_next_timestep] = df[previous_col_names].shift()

        previous_col_names = new_col_names_next_timestep

    #Drop the nan
    df = df.dropna()

    return df


if __name__ == "__main__":
    ###JUST TESTING THE FUNCTION WITH A SIX DAYS DF WITH RANDOM DATA

    # Set the number of rows
    num_rows = 144

    # Create a DatetimeIndex with hourly frequency
    date_index = pd.date_range(start='2024-03-12', periods=num_rows, freq='h')

    # Create random data
    data = np.random.randn(num_rows, 11)

    # Create DataFrame
    df = pd.DataFrame(data, index=date_index, columns=[f'scaled_X_{i-1}' for i in range(1, 12)])
    df.rename(columns={'scaled_X_0': 'target'}, inplace=True)

    timestepped_df = make_timesteps(df)

    print(timestepped_df.shape)
