import argparse
import psycopg2

def _parse_variable():
    parser = argparse.ArgumentParser()
    parser.add_argument('--context_variable', type=str)
    args = parser.parse_args()

    return args.context_variable

def fetch_pageview(execution_date):
    result = {}

    # Read the file within the mounted volume
    with open("/mnt/input/wikipageviews", "r") as f:
        for line in f:
            domain_code, page_title, view_counts, _ = line.split(" ")
            if domain_code == "en":
                result[page_title] = view_counts
    
    # Establish a connection to the PostgreSQL database
    connection = psycopg2.connect(
        host='host',
        port='port',
        dbname='database',
        user='user',
        password='password'
    )

    # Create a cursor object to execute SQL statements
    cursor = connection.cursor()

    # Execute SQL statements to save the data in the database
    for pagename, pageviewcount in result.items():
        query = "INSERT INTO pageview_counts VALUES ("f"'{pagename}', {pageviewcount}, '{execution_date}'"");"
        cursor.execute(query=query)

    # Commit the changes and close the cursor and connection
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    variables = _parse_variable()
    fetch_pageview(execution_date=variables)