from src.data.database_manager import init_db

if __name__ == "__main__":
    engine = init_db()          # Crea todas las tablas
    print("Tablas creadas en:", engine.url)
