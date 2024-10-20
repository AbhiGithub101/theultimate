# Query data from the 'movies' table
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import urllib

# Set up SQL Server connection
server = 'movieservers.database.windows.net'
database = 'moviedatabase'
username = 'movielogin'
password = 'Arbre@123#'
driver = 'ODBC Driver 17 for SQL Server'

# Create SQLAlchemy connection string
connection_string = (
    f"mssql+pyodbc://{username}:{urllib.parse.quote_plus(password)}@{server}:1433/"
    f"{database}?driver={urllib.parse.quote_plus(driver)}&encrypt=yes&trustServerCertificate=no"
)
engine = create_engine(connection_string)

# Streamlit app to search movies
search = st.text_input('Search Movie Name:')

if search:
    # Parameterized query to prevent SQL injection
    query = text("SELECT * FROM dbo.movies WHERE title = :title")

    try:
        with engine.connect() as conn:
            # Execute the query with the user-provided title as a parameter
            df = pd.read_sql_query(query, conn, params={"title": search})

            # Display the results
            if not df.empty:
                st.write("### Movies Data", df)
            else:
                st.warning("No matching movies found.")
    except Exception as e:
        st.error(f"Error querying the database: {e}")
