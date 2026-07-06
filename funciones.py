import sqlite3
from colorama import init, Fore, Style

init(autoreset=True)

def conectar():
    return sqlite3.connect('inventario.db')

def registrar_libro():
    print(Fore.BLUE + Style.BRIGHT + "\n--- Registrar Nuevo Libro ---")
    
    nombre = input("Título del libro (Obligatorio): ").strip()
    while not nombre:
        print(Fore.RED + "El título es obligatorio.")
        nombre = input("Título del libro: ").strip()
        
    autor = input("Autor del libro (Opcional): ").strip()
    
    while True:
        try:
            cantidad = int(input("Cantidad disponible: "))
            if cantidad < 0:
                print(Fore.RED + "La cantidad no puede ser negativa.")
                continue
            break
        except ValueError:
            print(Fore.RED + "Error: Ingrese un número entero válido.")

    while True:
        try:
            precio = float(input("Precio del libro (Pesos): "))
            if precio < 0:
                print(Fore.RED + "El precio no puede ser negativo.")
                continue
            break
        except ValueError:
            print(Fore.RED + "Error: Ingrese un número decimal válido.")

    categoria = input("Género / Categoría: ").strip()

    conexion = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        query = '''INSERT INTO productos (nombre, autor, cantidad, precio, categoria) 
                   VALUES (?, ?, ?, ?, ?)'''
        cursor.execute(query, (nombre, autor, cantidad, precio, categoria))
        conexion.commit()
        print(Fore.GREEN + f"\n[ÉXITO] El libro '{nombre}' ha sido registrado.")
    except sqlite3.Error as e:
        print(Fore.RED + f"[ERROR] No se pudo registrar: {e}")
    finally:
        if conexion is not None:
            conexion.close() 

def visualizar_libros():
    print(Fore.BLUE + Style.BRIGHT + "\n--- Inventario de Librería Tolkien ---")
    conexion = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        
        if not productos:
            print(Fore.YELLOW + "La librería no tiene libros registrados.")
            return

        print(f"{'ID':<5} | {'Título':<25} | {'Autor':<20} | {'Cant.':<6} | {'Precio':<10}")
        print("-" * 75)
        for prod in productos:
            print(f"{prod[0]:<5} | {prod[1]:<25} | {prod[2]:<20} | {prod[3]:<6} | ${prod[4]:<10.2f}")
    except sqlite3.Error as e:
        print(Fore.RED + f"[ERROR] Error al leer los datos: {e}")
    finally:
        if conexion is not None:
            conexion.close() 

def actualizar_libros():
    print(Fore.BLUE + Style.BRIGHT + "\n--- Actualizar Datos del Libro ---")
    
    try:
        id_prod = int(input("Ingrese el ID del libro que desea modificar: "))
    except ValueError:
        print(Fore.RED + "Error: El ID debe ser un número entero.")
        return

    conexion = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_prod,))
        producto = cursor.fetchone()

        if not producto:
            print(Fore.RED + f"No existe ningún libro registrado con el ID: {id_prod}")
            return

        print(Fore.YELLOW + f"\nModificando: {producto[1]} (Presione ENTER para mantener el valor actual)")
        
        nombre = input(f"Nuevo Título [{producto[1]}]: ").strip() or producto[1]
        autor = input(f"Nuevo Autor [{producto[2]}]: ").strip() or producto[2]
        
        cant_input = input(f"Nueva Cantidad [{producto[3]}]: ").strip()
        if cant_input:
            try:
                cantidad = int(cant_input)
                if cantidad < 0: raise ValueError
            except ValueError:
                print(Fore.RED + "Cantidad inválida. Se conservará el valor anterior.")
                cantidad = producto[3]
        else:
            cantidad = producto[3]
        
        precio_input = input(f"Nuevo Precio [{producto[4]}]: ").strip()
        if precio_input:
            try:
                precio = float(precio_input)
                if precio < 0: raise ValueError
            except ValueError:
                print(Fore.RED + "Precio inválido. Se conservará el valor anterior.")
                precio = producto[4]
        else:
            precio = producto[4]
        
        categoria = input(f"Nueva Categoría/Género [{producto[5]}]: ").strip() or producto[5]

        cursor.execute('''UPDATE productos 
                          SET nombre=?, autor=?, cantidad=?, precio=?, categoria=? 
                          WHERE id=?''', (nombre, autor, cantidad, precio, categoria, id_prod))
        conexion.commit()
        print(Fore.GREEN + f"[ÉXITO] Libro ID {id_prod} actualizado con éxito.")
    except sqlite3.Error as e:
        print(Fore.RED + f"[ERROR] Ocurrió un error al actualizar: {e}")
    finally:
        if conexion is not None:
            conexion.close() 

def eliminar_libro():
    print(Fore.BLUE + Style.BRIGHT + "\n--- Eliminar un Libro ---")
    try:
        id_prod = int(input("Ingrese el ID del libro que desea ELIMINAR: "))
    except ValueError:
        print(Fore.RED + "Error: El ID debe ser un número entero.")
        return

    conexion = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_prod,))
        producto = cursor.fetchone()

        if not producto:
            print(Fore.RED + f"No se encontró ningún libro con el ID {id_prod}")
            return

        confirmar = input(Fore.YELLOW + f"¿Está seguro de eliminar '{producto[1]}'? (s/n): ").strip().lower()
        if confirmar == 's':
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_prod,))
            conexion.commit()
            print(Fore.GREEN + "[ÉXITO] Libro eliminado de la librería.")
        else:
            print(Fore.YELLOW + "Operación cancelada.")
    except sqlite3.Error as e:
        print(Fore.RED + f"[ERROR] No se pudo eliminar: {e}")
    finally:
        if conexion is not None:
            conexion.close() 

def buscar_libro():
    print(Fore.BLUE + Style.BRIGHT + "\n--- Búsqueda de Libros ---")
    print("1. Buscar por ID")
    print("2. Buscar por Título (Nombre)")
    print("3. Buscar por Autor")
    opcion = input("Seleccione criterio (1-3): ").strip()

    conexion = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        if opcion == "1":
            id_prod = int(input("Ingrese el ID exacto: "))
            cursor.execute("SELECT * FROM productos WHERE id = ?", (id_prod,))
        elif opcion == "2":
            nombre_buscar = input("Ingrese el título: ").strip()
            cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{nombre_buscar}%",))
        elif opcion == "3":
            autor_buscar = input("Ingrese el autor: ").strip()
            cursor.execute("SELECT * FROM productos WHERE autor LIKE ?", (f"%{autor_buscar}%",))
        else:
            print(Fore.RED + "Opción inválida.")
            return

        resultados = cursor.fetchall()
        if not resultados:
            print(Fore.YELLOW + "No se encontraron coincidencias.")
            return

        print(Fore.GREEN + f"\nResultados:")
        print(f"{'ID':<5} | {'Título':<25} | {'Autor':<20} | {'Cant.':<6} | {'Precio':<10}")
        print("-" * 75)
        for prod in resultados:
            print(f"{prod[0]:<5} | {prod[1]:<25} | {prod[2]:<20} | {prod[3]:<6} | ${prod[4]:<10.2f}")
    except Exception as e:
        print(Fore.RED + f"[ERROR] {e}")
    finally:
        if conexion is not None:
            conexion.close() 

def reporte_bajo_stock():
    print(Fore.BLUE + Style.BRIGHT + "\n--- Alerta de Stock Bajo ---")
    try:
        limite = int(input("Ingrese el límite para el reporte: "))
    except ValueError:
        print(Fore.RED + "Debe introducir un número entero válido.")
        return

    conexion = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
        productos = cursor.fetchall()
        if not productos:
            print(Fore.GREEN + "Stock óptimo.")
            return
        print(f"{'ID':<5} | {'Título':<25} | {'Autor':<20} | {'Cant.':<6} | {'Precio':<10}")
        print("-" * 75)
        for prod in productos:
            print(f"{prod[0]:<5} | {prod[1]:<25} | {prod[2]:<20} | {Fore.RED}{prod[3]:<6}{Fore.RESET} | ${prod[4]:<10.2f}")
    except Exception as e:
        print(Fore.RED + f"[ERROR] {e}")
    finally:
        if conexion is not None:
            conexion.close() 

def exportar_catalogo_txt():

    print(Fore.BLUE + Style.BRIGHT + "\n--- Exportar Catálogo ---")
    conexion = None
    archivo = None 
    
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        libros = cursor.fetchall()
        
        if not libros:
            print(Fore.YELLOW + "No hay libros en la base de datos para exportar.")
            return

        archivo = open("catalogo_libros.txt", "w", encoding="utf-8")
        
        archivo.write("==================================================\n")
        archivo.write("        CATÁLOGO OFICIAL DE LIBRERÍA TOLKIEN      \n")
        archivo.write("==================================================\n\n")
        
        for libro in libros:
            archivo.write(f"ID: {libro[0]}\n")
            archivo.write(f"Título: {libro[1]}\n")
            archivo.write(f"Autor: {libro[2] if libro[2] else 'Sin autor registrado'}\n")
            archivo.write(f"Cantidad disponible: {libro[3]} unidades\n")
            archivo.write(f"Precio: ${libro[4]:.2f}\n")
            archivo.write(f"Categoría/Género: {libro[5]}\n")
            archivo.write("-" * 50 + "\n")
        
        print(Fore.GREEN + "[ÉXITO] Catálogo exportado correctamente como 'catalogo_libros.txt'.")
            
    except sqlite3.Error as e:
        print(Fore.RED + f"[ERROR] No se pudieron leer los datos de la BD: {e}")
    except IOError as e:
        print(Fore.RED + f"[ERROR] No se pudo escribir el archivo de texto: {e}")
    finally:

        if archivo is not None:
            archivo.close()
        if conexion is not None:
            conexion.close()