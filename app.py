import matplotlib.pyplot as plt
from flask import Flask, render_template
import pandas as pd
import requests
import mysql.connector

# Data Extraction from API
def fetch_data():
    url = 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/circulation_evenement/records?limit=92'
    response = requests.get(url)
    response_data = response.json()
    return pd.json_normalize(response_data.get("results", []))

# Database Setup and Insertion
def setup_database():
    conn = mysql.connector.connect(host="localhost", user="Amine", password="Emin92731099@")
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS db_paris1;")
    cursor.execute("USE db_paris1;")
    create_table_query = """
    CREATE TABLE IF NOT EXISTS events (
        id VARCHAR(255) ,
        starttime DATETIME,
        endtime DATETIME,
        description TEXT,
        type VARCHAR(255),
        subtype VARCHAR(255),
        street VARCHAR(255),
        polyline TEXT,
        direction VARCHAR(255)
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    return conn, cursor

def insert_data(df, cursor):
    for _, row in df.iterrows():
        insert_query = """
        INSERT INTO events (id, starttime, endtime, description, type, subtype, street, polyline, direction)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (row['id'], row['starttime'], row['endtime'], row['description'], row['type'], row['subtype'], row['street'], row['polyline'], row['direction'])
        cursor.execute(insert_query, data)

# ---- Data Cleaning ----
def clean_data(cursor):
    cleaning_queries = [
        "ALTER TABLE events MODIFY starttime DATETIME, MODIFY endtime DATETIME;",
        "UPDATE events SET subtype = 'unknown' WHERE subtype IS NULL;",
        """
        UPDATE events
        SET description = LOWER(description),
            type = LOWER(type),
            subtype = LOWER(subtype),
            street = LOWER(street),
            direction = LOWER(direction);
        """,
        "UPDATE events SET description = REGEXP_REPLACE(description, '[^a-zA-Z0-9\\s]', '');"
    ]
    for query in cleaning_queries:
        cursor.execute(query)

#Export Data to CSV
def export_data_to_csv():
    conn = mysql.connector.connect(host="localhost", user="Amine", password="Emin92731099@", database="db_paris1")
    query = "SELECT * FROM events"
    df = pd.read_sql(query, conn)
    df.to_csv("exported_data.csv", index=False)
    conn.close()

#Flask Application and Visualization
app = Flask(__name__)

@app.route('/')
def display_charts():
    df = pd.read_csv('exported_data.csv')

    #Bar Chart
    type_counts = df['type'].value_counts()
    fig, ax = plt.subplots()
    ax.bar(type_counts.index, type_counts.values)
    ax.set_xlabel('Type')
    ax.set_ylabel('Count')
    ax.set_title('Event Count by Type')
    fig.savefig('static/bar_chart.png')

    # Pie Chart
    subtype_counts = df['subtype'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(subtype_counts.values, labels=subtype_counts.index)
    ax.set_title('Event Proportions by Subtype')
    fig.savefig('static/pie_chart.png')

    return render_template('index.html', bar_url='static/bar_chart.png', pie_url='static/pie_chart.png')

# ---- Main Execution ----
if __name__ == '__main__':
    df = fetch_data()
    conn, cursor = setup_database()
    insert_data(df, cursor)
    clean_data(cursor)
    conn.commit()
    cursor.close()
    conn.close()
    export_data_to_csv()
    app.run(debug=True)
