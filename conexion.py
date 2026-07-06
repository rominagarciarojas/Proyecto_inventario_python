import sqlite3

def crear_base_datos():
    """
    Crea la base de datos 'inventario.db' y la tabla 'productos' si no existen.
    Define las columnas obligatorias: id, nombre, autor, cantidad, precio y categoria.
    """
    try:
        with sqlite3.connect('inventario.db') as conexion:
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
        print(f"Error al inicializar la base de datos: {e}")

if __name__ == "__main__":
    crear_base_datos()
    print("Base de datos y tabla inicializadas correctamente.")