import sqlite3

def crear_base_datos():
    conexion = None
    try:
        conexion = sqlite3.connect('inventario.db')
        cursor = conexion.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                autor TEXT,
                cantidad INTEGER NOT NULL,
                precio PESOS NOT NULL,
                categoria TEXT
            )
        ''')
        conexion.commit()
    except sqlite3.Error as e:
        print(f"Error crítico al inicializar la base de datos: {e}")
    finally:
        if conexion is not None:
            conexion.close()

if __name__ == "__main__":
    crear_base_datos()
    print("Base de datos de la librería inicializada correctamente.")