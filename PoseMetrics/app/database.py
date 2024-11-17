import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        dbname="PoseMetrics",  
        user="postgres",  
        password="18080812", 
        host="localhost", 
        port="5433" 
    )
    return conn
