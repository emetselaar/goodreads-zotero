import pandas as pd
import sqlite3

# File paths
csv_file = 'goodreads_library_export.csv'
sqlite_db = 'goodreads.db'
table_name = 'books'

# Load CSV into pandas DataFrame
df = pd.read_csv(csv_file)

# Infer column names and types
columns = df.columns

# Transform the ISBN columns, they need to be stripped of non-numeric characters
for col in columns:
    if 'isbn' in col.lower():
        df[col] = df[col].str.replace('=', '')

# convert ISBN13 column to INT
df['ISBN13'] = df['ISBN13'].str.replace('=', '')
# Remove the " symbol from the ISBN13 column
df['ISBN13'] = df['ISBN13'].str.replace('"', '')
# Handle empty values
df['ISBN13'] = df['ISBN13'].replace('', 0)
# Convert the ISBN13 column to integer 
df['ISBN13'] = df['ISBN13'].astype(int)

# Convert specific columns to integer if they are numeric
numeric_columns = ["Year Published", "Original Publication Year", "Number of Pages"]
for col in numeric_columns:
    if pd.api.types.is_numeric_dtype(df[col]):  # Check if it's numeric first
        df[col] = df[col].fillna(0).astype(int) # fill nan first


data_types = []
for col in df.columns:
    colname = col.replace(" ", "_").lower()
    colname = colname.replace("-", "_")
    colname = colname.replace("(", "")
    colname = colname.replace(")", "")
    dtype = df[col].dtype
    if pd.api.types.is_integer_dtype(dtype):
        sql_type = "INTEGER"
    elif pd.api.types.is_float_dtype(dtype):
        sql_type = "REAL"
    elif pd.api.types.is_bool_dtype(dtype):
        sql_type = "BOOLEAN"
    else:
        sql_type = "TEXT"
    data_types.append((colname, sql_type))

# Create SQLite connection
conn = sqlite3.connect(sqlite_db)
cursor = conn.cursor()

# Drop the old table if it exists
drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
cursor.execute(drop_table_query)

# Create table
create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
create_table_query += ", ".join([f"{col} {dtype}" for col, dtype in data_types])
create_table_query += ");"
cursor.execute(create_table_query)

# Insert data
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Commit and close connection
conn.commit()
conn.close()

print("CSV data successfully imported into SQLite database!")
