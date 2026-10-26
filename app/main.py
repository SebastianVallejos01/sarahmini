from fastapi import FastAPI, HTTPException
import psycopg
import os

app = FastAPI(title="Sarah Mini API conectada a BD")

# Leemos las credenciales desde las variables de entorno (inyectadas por Compose)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "sarah_mini")
DB_USER = os.getenv("DB_USER", "sarah_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

def get_db_connection():
    try:
        # psycogp conecta usando los parámetros extraídos
        conn = psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

@app.get("/")
def root():
    return {"message": "API funcionando"}

@app.get("/db-check")
def check_database():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
    
    # Hacemos una consulta simple para obtener la versión de PostgreSQL
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return {
        "status": "Conexión exitosa",
        "postgres_version": db_version[0]
    }