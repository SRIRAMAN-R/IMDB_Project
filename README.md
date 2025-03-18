# 🎥 IMDb 2024 Data Scraping and Visualization  

This project automates the process of **scraping movie data from IMDb**, storing it in a **TiDB SQL database**, and providing **interactive visualizations and filtering** using **Streamlit**.  
It enables users to explore movies by **genre, rating, votes, and duration** through dynamic visualizations.  

---

## 📌 Table of Contents  
- 1️⃣ Project Overview  
- 2️⃣ Tech Stack  
- 3️⃣ Features
- 4️⃣ Architecture & Workflow
- 5️⃣ Installation Guide
- 6️⃣ Execution Steps
- 7️⃣ Example Screenshots

---

## 1️⃣ **Project Overview**

IMDb is a popular online database of movies, TV shows, and celebrity content.  
This project aims to:  
- **Scrape** IMDb movie data for the year 2024.  
- **Store** the scraped data in a **TiDB cloud SQL database**.  
- Create an **interactive Streamlit app** for filtering and visualizing the data.  
- Perform **data analysis and visualizations** to extract insights.  

---

## 2️⃣ **Tech Stack**

✅ **Languages:**  
- **Python:** For web scraping, data processing, and building the Streamlit app.  
- **SQL:** For data storage and querying in TiDB Cloud.  

✅ **Libraries & Tools:**  
- **Selenium:** For web scraping IMDb data.  
- **Pandas:** For data cleaning and manipulation.  
- **Streamlit:** For building the interactive web application.  
- **Matplotlib & Seaborn:** For visualizations.  
- **MySQL Connector:** For TiDB cloud integration.  

✅ **Database:**  
- **TiDB Cloud** (MySQL-compatible distributed SQL database).  

---

## 3️⃣ **Features**

### 🔹 **Data Scraping**
- Automated IMDb data scraping using Selenium.  
- Extracts **title, genre, rating, votes, and duration**.  
- Stores the scraped data into CSV files.  

### 🔹 **Data Storage**
- Combines multiple CSV files into a single dataset.  
- Stores the data in **TiDB Cloud** SQL database.  
- SQL table schema:
    - `Title`, `Genre`, `Rating`, `Votes`, `Duration_Minutes`.  

### 🔹 **Streamlit App**
- **Filteration Page:**  
    - Filter by **Genre, Rating, Votes, and Duration**.  
    - Display filtered movies in a table.  
- **Visualization Page:**  
    - **Top 10 Movies** by rating and votes.  
    - **Genre distribution** bar chart.  
    - **Average duration** by genre.  
    - **Voting trends** by genre.  
    - **Rating distribution** histogram.
    - **Genre-Based Rating** 
    - **Most popular genres by votes** (pie chart).
    - **Duration Extremes**  show the shortest and longest movies.
    - **Ratings by Genre** heatmap
    - **Correlation analysis:** Scatter plot for votes vs. ratings.  

---

## 4️⃣ **Architecture & Workflow**

### 📊 **High-Level Architecture**

```plaintext
       +-----------------------------+
       |       IMDb Website          |
       +-----------------------------+
                     |
        (1) Selenium Scraper (Python)
                     |
       +-----------------------------+
       |      CSV Files (Raw Data)   |
       +-----------------------------+
                     |
        (2) CSV Merging with Pandas
                     |
       +-----------------------------+
       |    TiDB Cloud SQL Database  |
       +-----------------------------+
                     |
        (3) Streamlit App (UI)      
         ↳ Filteration & Visualization
```
---

## 5️⃣ **Installation Guide**

### 🛠️ **Prerequisites**
- Install **Python 3.x**  
- Install **Google Chrome**  
- Set up a **TiDB Cloud Account**  
- Install required libraries:  

```bash
pip install -r 

selenium  
pandas  
mysql-connector-python  
streamlit  
matplotlib  
seaborn  
```
---

## 6️⃣ **Execution Steps**

### 🚀 **Step 1: Scrape IMDb Data**
Run the Jupyter notebook to extract movie details and save them to CSV files:
```bash
jupyter notebook IMDb_data_scraper.ipynb
```

## ✅ Generates multiple genre-specific CSV files:
- Action_movies.csv
- Adventure_movies.csv
- Animation_movies.csv
- Crime_movies.csv
- Family_movies.csv
- History_movies.csv


### 🚀 **Step 2: Merge CSV Files**
Combine all CSV files into a single dataset
## ✅ Output file:
- IMDb_2024_All_Movies.csv

### 🚀 Step 3: Launch the Streamlit App
Start the Streamlit application:

```bash
streamlit run IMDb_app.py
```
## ✅ Open the app in your browser at:
- http://localhost:8504
---
## 7️⃣ **Example Screenshots**
## 🎯 Filteration Page

- Filter by Genre, Rating, Votes, and Duration

 ![image](https://github.com/user-attachments/assets/227e870e-5172-4224-a901-3a007a0d4218)

  
## 📊 Visualization Page
- Top 10 Movies by Votes & Ratings

  ![image](https://github.com/user-attachments/assets/fa3457f2-5234-4545-baf1-73590ac830d5)


