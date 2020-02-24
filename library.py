# Function for first round data cleansing

def data_cleansing(raw, filter_out, replace_dict, drop_list):
    
    # Remove unnecessary columns that contain these text
    df = raw.copy()
    for f in filter_out:
        df = df.loc[:, ~df.columns.str.contains(f)]

    # Clean up characters from column names
    for key, value in replace_dict.items():
        df.columns = df.columns.str.replace(key, value)

    # Manually drop irrelevant columns
    remain_cols = [i for i in df.columns if i not in drop_list]
    df = df[remain_cols]

    # Drop column if data is > 20% null
    df = df.drop(df.loc[:,list((100*(df.isnull().sum()/len(df.index))>20))].columns, 1)

    # Replace NaN values with the state's median. If still missing, use national.
    df = df.groupby('State_Abbreviation').apply(lambda x: x.fillna(x.median()))
    df = df.fillna(df.median())

    # Remove state-level data, keep only county-level data
    df = df.drop(df[df.County_FIPS_Code==0].index)

    return df

# Function to remove outliers

def remove_outliers(df, k):
    # k = num of std from mean as outlier
    
    dfcopy = df.copy()
    for col in df.columns:
        mean = dfcopy[col].mean()
        std  = dfcopy[col].std()
        df = df.drop(df[df[col] > mean + k*std].index)
        df = df.drop(df[df[col] < mean - k*std].index)
    print(f'{round((1 - df.shape[0] / dfcopy.shape[0])*100,1)}% of rows removed')
    print(f'{df.shape[0]} rows remains')
    return df