import psycopg2

class Book:
    def __init__(self, dat_base):
        self.dat_base = dat_base

    def __enter__(self):
        self.conn = psycopg2.connect(**self.dat_base)
        self.cur = self.conn.cursor()
        return self.conn, self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

        if self.cur:
            self.cur.close()

dat_base = {
    "host": "localhost",
    "port": 5432,
    "database": "cars",
    "user": "postgres",
    "password": "1111"
}

# CREATE

with Book(dat_base) as (conn, cur):
    commands = (
        """
        CREATE TABLE IF NOT EXISTS company(
        company_id SERIAL PRIMARY KEY,
        company_name VARCHAR(100) NOT NULL)""",

        """CREATE TABLE IF NOT EXISTS workers(
        worker_id SERIAL PRIMARY KEY,
        worker_name VARCHAR(255) NOT NULL,
        worker_age INT NOT NULL,
        company_id INT, 
        CONSTRAINT fk_company FOREIGN KEY(company_id) REFERENCES company(company_id))"""
    )

    for command in commands:
        cur.execute(command)
    conn.commit()
    print('Successfully created!')

# INSERT
with Book(dat_base) as (conn, cur):
    postgres_insert_query = "INSERT INTO company(company_name) VALUES (%s)"
    insert_values = [('BLACK ROAD',), ('Google',), ('Amazon',)]
    cur.executemany(postgres_insert_query, insert_values)
    conn.commit()
    print('Successfully inserted into table1!')


with Book(dat_base) as (conn, cur):
    postgres_insert_query2 = "INSERT INTO workers(worker_name, worker_age, company_id) VALUES (%s, %s, %s)"
    insert_values2 = [('Zuhra', 23, 2), ('Lola', 25, 1), ('Kamola', 34, 3)]
    cur.executemany(postgres_insert_query2, insert_values2)
    conn.commit()
    print('Second table successfully inserted!')

# READ
with Book(dat_base) as (conn, cur):
    postgresql_select_query1 = "SELECT * FROM company"
    cur.execute(postgresql_select_query1)
    rows_company = cur.fetchall()
    print("Company Table:")
    for row in rows_company:
        print(row)

    postgresql_select_query2 = "SELECT * FROM workers"
    cur.execute(postgresql_select_query2)
    rows_workers = cur.fetchall()
    print("\nWorkers Table:")
    for row in rows_workers:
        print(row)

# UPDATE

with Book(dat_base) as (conn, cur):
    postgres_update_query = "UPDATE workers SET worker_age = 23 WHERE worker_id = 1"
    cur.execute(postgres_update_query)
    conn.commit()
    print("Worker's age updated successfully!")

with Book(dat_base) as (conn, cur):
    postgresql_select_query2 = "SELECT * FROM workers"
    cur.execute(postgresql_select_query2)
    rows_workers = cur.fetchall()
    print("\nWorkers Table:")
    for row in rows_workers:
        print(row)
        
# DELETE

with Book(dat_base) as (conn, cur):
    postgres_delete_query = "DELETE FROM workers WHERE worker_id = 3"
    cur.execute(postgres_delete_query)
    conn.commit()
    print("Worker deleted successfully!")