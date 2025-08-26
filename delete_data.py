import mysql.connector

    
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Priti@02'
)
cursor = conn.cursor()

delete=int(input("0 create db, 1 delete db: ")) # 0 create db, 1 delete db
dbs = ['airline_system', 'flights_system', 'passenger_system']

if delete:
    print("insider delete db")

    for db in dbs:
        cursor.execute(f"USE {db}")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")  # Disable foreign key checks temporarily
        
        # Drop foreign key constraints first
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        for (table_name,) in tables:
            cursor.execute(f"SHOW CREATE TABLE {table_name}")
            create_table_sql = cursor.fetchone()[1]
            
            # Find foreign key constraints in the table's creation SQL
            if "FOREIGN KEY" in create_table_sql:
                # Drop foreign keys
                cursor.execute(f"ALTER TABLE {table_name} DROP FOREIGN KEY {table_name}_ibfk_1")
                print(f"Dropped foreign key constraint from {table_name}")
            
        # Drop all tables in the database
        for (table_name,) in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"Dropped table: {db}.{table_name}")
        
        # Drop the database itself
        cursor.execute(f"DROP DATABASE IF EXISTS {db}")
        print(f"Dropped database: {db}")
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")  # Re-enable foreign key checks

    conn.commit()
else:
    # Create database if it doesn't exist\
    for db in dbs:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
        print("created db ",db)

        # Continue with your logic for table creation, data insertion, etc.
cursor.close()
cursor.close()