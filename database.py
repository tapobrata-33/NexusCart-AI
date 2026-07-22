import mysql.connector


def get_connection():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kanu@2006",
        database="nexuscart"
    )

    return connection


# Test

if __name__ == "__main__":

    try:
        conn = get_connection()

        print("Database Connected Successfully")

        conn.close()

    except Exception as e:
        print("Database Error:", e)