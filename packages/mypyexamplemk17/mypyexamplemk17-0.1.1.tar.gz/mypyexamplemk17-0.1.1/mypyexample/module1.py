import pandas as pd


def df_info(df):
    print(df.describe)
    print(df.head(3))
    print("...")
    print(df.tail(3))

def print_default():
    df = pd.Series([1, 3, 5, 5, 6, 8])
    df_info(df)

