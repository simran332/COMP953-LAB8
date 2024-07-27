"""
Description:
 Creates the relationships table in the Social Network database
 and populates it with 100 fake relationships.

Usage:
 python create_relationships.py
"""
import os
import sqlite3
from random import randint, choice 
from faker import Faker

# Determine the path of the database
script_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(script_directory, 'social_network.db')

def main():
    create_relationship_table()
    populate_relationship_table()

def create_relationship_table():
    """Creates the relationships table in the DB"""
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY, 
        person1_id INTEGER NOT NULL, 
        person2_id INTEGER NOT NULL, 
        type TEXT NOT NULL, 
        start_date DATE NOT NULL, 
        FOREIGN KEY (person1_id) REFERENCES people (id), 
        FOREIGN KEY (person2_id) REFERENCES people (id)
    ); 
    """
    cur.execute(create_table_query)
    conn.commit() 
    conn.close()
    return

def populate_relationship_table():
    """Adds 100 random relationships to the DB"""
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    insert_query = """
    INSERT INTO relationships (person1_id, person2_id, type, start_date)
    VALUES (?, ?, ?, ?);
    """

    fake = Faker()
    
    for _ in range(100):
        person1_id = randint(1, 200)
        person2_id = randint(1, 200)

        while person2_id == person1_id:
            person2_id = randint(1, 200)

        relationship_type = choice(('friend', 'spouse', 'partner', 'relative'))
        start_date = fake.date_between(start_date='-50y', end_date='today')

        new_relationship = (person1_id, person2_id, relationship_type, start_date)

        cur.execute(insert_query, new_relationship)

    conn.commit()
    conn.close()
    return 

if __name__ == '__main__':
   main()
