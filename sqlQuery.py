import psycopg2
import time
import random

db_params = {
   "dbname": "postgres",
   "user": "postgres.gujygmchiikhydyjfvca",
   "password": "NN1Pp2jqupcu4MPR",
   "host": "aws-0-us-west-1.pooler.supabase.com",
   "port": "6543",  # 5432 #6543
   "connect_timeout": 10,
   "sslmode": "require",
}




def connect_with_retry(max_attempts=3):
   attempt = 0
   last_error = None


   while attempt < max_attempts:
       try:
           print(f"Attempt {attempt+1} of {max_attempts}...")
           conn = psycopg2.connect(**db_params)
           print("✅ Connection successful!")
           return conn
       except Exception as e:
           attempt += 1
           last_error = e
           if attempt < max_attempts:
               wait_time = (2**attempt) + (random.random())
               print(f"Connection failed: {e}")
               print(f"Retrying in {wait_time:.1f} seconds...")
               time.sleep(wait_time)
           else:
               print(f"❌ Connection attempts failed. Last error: {e}")
               raise e

def access_table():
    try:
        print("Attempting connection...")
        conn = connect_with_retry()
        cur = conn.cursor()


        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        print(f"Current time: {result[0]}")
        
        cur.execute('SELECT * FROM "The Milo Unit Data"')
        description = cur.fetchall()

        sendbackDict = {}
        sendbackList = []

        for item in description:
            sendbackDict = {'unit_id': item[0], 'unit_number' : item[1], 'floor_plan' : item[2], 
                        'unit_price' : item[3], 'unit_status' : item[4], 'lease_terms' : item[5]}
            sendbackList.append(sendbackDict)

        cur.close()
        conn.close()
        print("\nConnection closed.")
        return sendbackList


    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Ensure you have psycopg2 installed")