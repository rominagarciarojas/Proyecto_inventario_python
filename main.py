import conexion
import funciones
from colorama import init, Fore, Style

init(autoreset=True)

def menu_principal():
    conexion.crear_base_datos()
    
    while True:
        print(Fore.CYAN + Style.BRIGHT + "\n==================================================")
        print(Fore.WHITE + Style.BRIGHT + "     SISTEMA DE GESTIÓN DE LIBRERÍA TOLKIEN    ")
        print(Fore.CYAN + Style.BRIGHT + "==================================================")
        print(Fore.WHITE + " 1. " + Fore.LIGHTYELLOW_EX + "Registrar nuevo libro")
        print(Fore.WHITE + " 2. " + Fore.LIGHTYELLOW_EX + "Visualizar todos los libros")
        print(Fore.WHITE + " 3. " + Fore.LIGHTYELLOW_EX + "Actualizar datos de un libro (por ID)")
        print(Fore.WHITE + " 4. " + Fore.LIGHTYELLOW_EX + "Eliminar un libro (por ID)")
        print(Fore.WHITE + " 5. " + Fore.LIGHTYELLOW_EX + "Buscar un libro (ID / Título / Autor)")
        print(Fore.WHITE + " 6. " + Fore.LIGHTYELLOW_EX + "Reporte de libros con Bajo Stock")
        print(Fore.WHITE + " 7. " + Fore.LIGHTRED_EX + "Salir del sistema")
        print(Fore.CYAN + Style.BRIGHT + "==================================================")
        
        opcion = input(Fore.WHITE + Style.BRIGHT + "Seleccione una opción (1-7): ").strip()
        
        if opcion == "1":
            funciones.registrar_libro()
        elif opcion == "2":
            funciones.visualizar_libros()
        elif opcion == "3":
            funciones.actualizar_libros()
        elif opcion == "4":
            funciones.eliminar_libro()
        elif opcion == "5":
            funciones.buscar_libro()
        elif opcion == "6":
            funciones.reporte_bajo_stock()
        elif opcion == "7":
            print(Fore.GREEN + Style.BRIGHT + "\n¡Gracias por usar el sistema de la librería Tolkien! Gracias Talento Tech!!!")
            break
        else:
            print(Fore.RED + Style.BRIGHT + "Opción no válida.")

if __name__ == "__main__":
    menu_principal()