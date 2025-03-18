import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

# Database Configuration
DB_CONFIG = {
    "host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    "port": 4000,
    "user": "2Djg5GyoVwWC4gN.root",
    "password": "JWYIDlQjiVFU2pUD",
    "database": "IMDB"
}

# Function to fetch data based on SQL query
@st.cache_data
def fetch_data(query, params=None):
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            df = pd.read_sql(query, connection, params=params)
        return df
    except mysql.connector.Error as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()


st.title("IMDb 2024 - Movie Analysis & Visualization")

# Sidebar Navigation
st.sidebar.header("IMDb Movie Analysis")
page = st.sidebar.radio("", ["Filteration", "Visualizations"])

# 1️⃣ Filteration Page
if page == "Filteration":
    st.header("Movie Filteration")

    # Fetch distinct genres
    genre_query = "SELECT DISTINCT Genre FROM IMDb_Movies"
    genres = fetch_data(genre_query)

    if genres.empty:
        st.error("No genres available in the database.")
    else:
        selected_genre = st.selectbox("Select Genre", genres["Genre"].tolist())
        rating_range = st.slider("IMDb Rating Range", 0.0, 10.0, (0.0, 10.0), 0.1)
        min_votes = st.number_input("Minimum Votes", 0, value=10000, step=1000)
        duration_filter = st.radio("Select Duration", ["All", "< 2 hrs", "2-3 hrs", "> 3 hrs"])

        # Construct SQL query based on filters
        query = """
            SELECT Title, Genre, Rating, Votes, Duration_Minutes 
            FROM IMDb_Movies 
            WHERE Genre = %s 
            AND Rating BETWEEN %s AND %s 
            AND Votes >= %s
        """
        params = [selected_genre, rating_range[0], rating_range[1], min_votes]

        # Apply duration filter
        if duration_filter == "< 2 hrs":
            query += " AND Duration_Minutes < 120"
        elif duration_filter == "2-3 hrs":
            query += " AND Duration_Minutes BETWEEN 120 AND 180"
        elif duration_filter == "> 3 hrs":
            query += " AND Duration_Minutes > 180"

        # Fetch and display data
        df = fetch_data(query, params)
        st.write(f"Showing **{len(df)}** movies")
        st.dataframe(df)

# 2️⃣ Visualization Page
elif page == "Visualizations":
    st.header("Movie Data Visualizations")

    # 1️⃣ Top 10 Movies by Rating & Votes (Vertical Bar Chart)
    st.subheader("1. Top 10 Movies by Rating & Votes")
    top_movies_query = """
        SELECT Title, MAX(Rating) AS Rating, MAX(Votes) AS Votes
        FROM IMDb_Movies
        GROUP BY Title
        ORDER BY Votes DESC, Rating DESC 
        LIMIT 10;
    """
    top_movies = fetch_data(top_movies_query)
    st.dataframe(top_movies)
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(top_movies["Title"], top_movies["Votes"], color="cornflowerblue", label="Votes")
    for i, (title, votes, rating) in enumerate(zip(top_movies["Title"], top_movies["Votes"], top_movies["Rating"])):
        ax.text(i, votes + (votes * 0.02), f"{rating:.1f}", ha='center', fontsize=10, color='black')

    ax.set_xlabel("Movie Title")
    ax.set_ylabel("Votes")
    ax.set_title("Top 10 Movies by Votes & Rating")
    plt.xticks(rotation=45)  
    st.pyplot(fig)

    # 2️⃣ Genre Distribution
    st.subheader("2. Genre Distribution")
    genre_counts_query = """
        SELECT Genre, COUNT(*) AS Number_of_Movies 
        FROM IMDb_Movies 
        GROUP BY Genre
        ORDER BY Number_of_Movies DESC;
    """
    genre_counts = fetch_data(genre_counts_query)
    st.dataframe(genre_counts)

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=genre_counts["Genre"], y=genre_counts["Number_of_Movies"], palette="viridis", ax=ax)
    ax.set_xlabel("Genre")
    ax.set_ylabel("Number of Movies")
    ax.set_title("Movies Distribution by Genre")
    plt.xticks(rotation=45)
    st.pyplot(fig)



    # 3️⃣ Average Duration by Genre
    st.subheader("3. Average Duration by Genre")
    avg_duration_query = """
        SELECT Genre, CAST(AVG(Duration_Minutes) AS SIGNED) AS Average_Duration_Minutes
        FROM IMDb_Movies 
        GROUP BY Genre
        ORDER BY Average_Duration_Minutes DESC;
    """
    avg_duration = fetch_data(avg_duration_query)
    st.dataframe(avg_duration)

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(y=avg_duration["Genre"], x=avg_duration["Average_Duration_Minutes"], palette="bright", ax=ax)
    ax.set_xlabel("Average Duration (Minutes)")
    ax.set_ylabel("Genre")
    ax.set_title("Average Movie Duration by Genre")
    st.pyplot(fig)


    # 4️⃣ Voting Trends by Genre
    st.subheader("4. Voting Trends by Genre")
    avg_votes_query = """
        SELECT Genre, CAST(AVG(Votes) AS SIGNED) AS Average_Votes 
        FROM IMDb_Movies 
        GROUP BY Genre
        ORDER BY Average_Votes desc;
    """
    avg_votes = fetch_data(avg_votes_query)
    st.dataframe(avg_votes)

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(y=avg_votes["Genre"], x=avg_votes["Average_Votes"], palette="Paired", ax=ax)
    ax.set_xlabel("Average Votes")
    ax.set_ylabel("Genre")
    ax.set_title("Voting Trends by Genre")
    st.pyplot(fig)

    
    # 5️⃣ Rating Distribution - Histogram
    st.subheader("5. Rating Distribution")
    range_query = """
        SELECT 
            CASE 
                WHEN Rating >= 0 AND Rating < 2 THEN '0 - 2'
                WHEN Rating >= 2 AND Rating < 4 THEN '2 - 4'
                WHEN Rating >= 4 AND Rating < 6 THEN '4 - 6'
                WHEN Rating >= 6 AND Rating < 8 THEN '6 - 8'
                WHEN Rating >= 8 AND Rating <= 10 THEN '8 - 10'
                ELSE 'Unknown'
            END AS Rating_Range,
            COUNT(*) AS Movie_Count
        FROM IMDb_Movies
        GROUP BY Rating_Range
        ORDER BY Rating_Range;
    """
    range_df = fetch_data(range_query)
    st.dataframe(range_df)
    rating_distribution_query = """
        SELECT Rating
        FROM IMDb_Movies;
    """
    rating_distribution = fetch_data(rating_distribution_query)
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.hist(rating_distribution['Rating'], bins=20, color='#4CAF50', edgecolor='black', alpha=0.75)
    ax.set_title('Histogram of IMDb Ratings', fontsize=14)
    ax.set_xlabel('Rating')
    ax.set_ylabel('Number of Movies')
    st.pyplot(fig)

    
    # 6️⃣ Top-Rated Movie by Each Genre
    st.subheader("6. Top-Rated Movie by Each Genre")
    top_rated_movies_by_genre_query = """
        WITH RankedMovies AS (
            SELECT Genre, Title, Rating, DENSE_RANK() OVER (PARTITION BY Genre ORDER BY Rating DESC, Title ASC) AS RankPosition
            FROM IMDb_Movies
        )
        SELECT Genre, Title, Rating
        FROM RankedMovies
        WHERE RankPosition = 1
        ORDER BY Genre;
    """
    top_rated_movies_by_genre = fetch_data(top_rated_movies_by_genre_query)
    st.dataframe(top_rated_movies_by_genre)


    # 7️⃣ Most Popular Genres by Votes
    st.subheader("7. Most Popular Genres by Votes")

    genre_votes_df = fetch_data("""
        SELECT Genre, SUM(Votes) AS Total_Votes 
        FROM IMDb_Movies 
        GROUP BY Genre 
        ORDER BY Total_Votes DESC
    """)
    st.dataframe(genre_votes_df)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.pie(genre_votes_df["Total_Votes"], labels=genre_votes_df["Genre"], autopct='%1.1f%%', colors=sns.color_palette("bright"))
    ax.set_title("Most Popular Genres by Votes")
    st.pyplot(fig)
    
    
    # 8️⃣ Duration Extremes: Shortest & Longest Movies
    st.subheader("8. Duration Extremes: Shortest & Longest Movies")

    shortest_query = """
        SELECT 'Shortest Movie' AS Category, Title, Genre, Duration_Minutes 
        FROM IMDb_Movies 
        ORDER BY Duration_Minutes ASC 
        LIMIT 1;
    """
    longest_query = """
        SELECT 'Longest Movie' AS Category, Title, Genre, Duration_Minutes 
        FROM IMDb_Movies 
        ORDER BY Duration_Minutes DESC 
        LIMIT 1;
    """
    shortest_movie = fetch_data(shortest_query)
    longest_movie = fetch_data(longest_query)
    duration_extremes_df = pd.concat([shortest_movie, longest_movie], ignore_index=True)
    duration_extremes_df.rename(columns={
        "Category": "",
        "Title": "Movie Title",
        "Genre": "Genre",
        "Duration_Minutes": "Duration (mins)"
    }, inplace=True)
    st.table(duration_extremes_df)

    # 9️⃣ Ratings by Genre
    st.subheader("9. Ratings by Genre")

    genre_ratings_df = fetch_data("""
        SELECT Genre, AVG(Rating) AS Average_Rating
        FROM IMDb_Movies 
        GROUP BY Genre;
    """)
    genre_ratings_df["Average_Rating"] = genre_ratings_df["Average_Rating"].round(1)
    st.dataframe(genre_ratings_df)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(genre_ratings_df.set_index("Genre").T, annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
    ax.set_title("Average Ratings by Genre")
    st.pyplot(fig)


    # 🔟 Correlation Analysis: Ratings vs Votes
    st.subheader("10. Correlation Analysis: Ratings vs Votes")
    ratings_votes_df = fetch_data("""
        SELECT DISTINCT Title, Rating, Votes 
        FROM IMDb_Movies 
        ORDER BY Votes DESC
    """)
    st.dataframe(ratings_votes_df)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=ratings_votes_df, x="Rating", y="Votes", alpha=0.6, color="dodgerblue", edgecolor="black")
    ax.set_xlabel("IMDb Rating")
    ax.set_ylabel("Number of Votes")
    ax.set_title("Correlation Between Ratings and Votes")
    st.pyplot(fig)
