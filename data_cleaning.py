import pandas as pd


def clean_data(df):

    df.columns = df.columns.str.replace(
        "ï»¿",
        "",
        regex=False
    )


    df["Date"] = pd.to_datetime(
        df["Date"],
        dayfirst=True
    )


    return df