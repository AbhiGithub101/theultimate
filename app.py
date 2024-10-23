import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import movieposters as mp
import urllib
import wikipedia
import re

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
st.title('Rate and Review Movies')

search = st.text_input('Search Movie Name:')

if search:
    # Optional: Use regex to clean/validate/format the search query
    match = re.match(r"^(.*?)\s*\(", search)
    movie_title = match.group(1) if match else search  # Use the cleaned title if regex matched, otherwise use the raw search
    
    # Parameterized query to prevent SQL injection
    query = text("SELECT * FROM dbo.movies WHERE title = :title")

    try:
        with engine.connect() as conn:
            # Execute the query with the user-provided title as a parameter
            df = pd.read_sql_query(query, conn, params={"title": movie_title})

            # Display the results
            if not df.empty:
                # Fetch and display the movie poster if the movie is found
                link = mp.get_poster(title=movie_title)
                
                col1,col2 = st.columns(2)
                with col1:
                    st.image(link,width=200)
                with col2:
                    st.write(wikipedia.summary(movie_title))
                
                st.write("### Movies Data", df)
            else:
                st.warning("No matching movies found.")
    except Exception as e:
        st.error(f"Error querying the database: {e}")




# # Query data from the 'movies' table
# import streamlit as st
# import pandas as pd
# from sqlalchemy import create_engine, text
# import urllib

# # Set up SQL Server connection
# server = 'movieservers.database.windows.net'
# database = 'moviedatabase'
# username = 'movielogin'
# password = 'Arbre@123#'
# driver = 'ODBC Driver 17 for SQL Server'

# # Create SQLAlchemy connection string
# connection_string = (
#     f"mssql+pyodbc://{username}:{urllib.parse.quote_plus(password)}@{server}:1433/"
#     f"{database}?driver={urllib.parse.quote_plus(driver)}&encrypt=yes&trustServerCertificate=no"
# )
# engine = create_engine(connection_string)

# # Streamlit app to search movies
# search = st.text_input('Search Movie Name:')

# if search:
#     # Parameterized query to prevent SQL injection
#     query = text("SELECT * FROM dbo.movies WHERE title = :title")

#     try:
#         with engine.connect() as conn:
#             # Execute the query with the user-provided title as a parameter
#             df = pd.read_sql_query(query, conn, params={"title": search})

#             # Display the results
#             if not df.empty:
#                 st.write("### Movies Data", df)
#             else:
#                 st.warning("No matching movies found.")
#     except Exception as e:
#         st.error(f"Error querying the database: {e}")
