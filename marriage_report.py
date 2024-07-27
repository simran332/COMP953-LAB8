"""
Description:
 Generates a CSV reports containing all married couples in
 the Social Network database.

Usage:
 python marriage_report.py
"""
import os
import sqlite3
from create_relationships import db_path, script_dir
import pandas as pd

def main():
    # Query DB for list of married couples
    couples = fetch_married_couples()

    # Save all married couples to CSV file
    file_path = os.path.join(script_dir, 'married_couples.csv')
    write_couples_to_csv(couples, file_path)

def fetch_married_couples():
    """Queries the Social Network database for all married couples.

    Returns:
        list: (name1, name2, start_date) of married couples 
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """ SELECT person1.name, person2.name, 
    start_date, type FROM relationships 
    JOIN people person1 ON person1_id = person1.id 
    JOIN people person2 ON person2_id = person2.id where type="spouse"; """

    cursor.execute(query)
    relationships = cursor.fetchall()

    conn.commit()
    conn.close()

    results = []
    temp = []

    for name1, name2, start_date, type in relationships:
        temp = [name1, name2, start_date]
        results.append(temp)

    return results

def write_couples_to_csv(couples, file_path):
    """Saves list of married couples to a CSV file, including both people's 
    names and their wedding anniversary date  

    Args:
        couples (list): (name1, name2, start_date) of married couples
        file_path (str): Path of CSV file
    """
    df = pd.DataFrame(couples, columns=['Name 1', 'Name 2', 'Anniversary'])
    df.to_csv(file_path, index=False)
    return

if __name__ == '__main__':
   main()
