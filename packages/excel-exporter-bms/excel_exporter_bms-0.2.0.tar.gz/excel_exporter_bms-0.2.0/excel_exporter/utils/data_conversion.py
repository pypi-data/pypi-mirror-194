def from_list_of_dicts(records_list):
    """Converts a list of dicts into a list of dicts"""
    return {
        col: [record[col] for record in records_list]
        for col in records_list[0]
    }


def from_pandas_dataframe(df):
    """Converts a pandas dataframe into a list of dicts"""
    return df.to_dict(orient='list')
