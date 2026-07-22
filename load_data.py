import pandas as pd
from database import get_connection


def load_data():

    connection = get_connection()

    query = "SELECT * FROM retail_sales"

    df = pd.read_sql(
        query,
        connection
    )

    connection.close()

    return df



if __name__ == "__main__":

    data = load_data()

    print(data.head())