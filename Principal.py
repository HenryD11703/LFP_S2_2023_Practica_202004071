from Producto import Producto
from tabulate import tabulate
def menu():
    print('Seleccione una opcion')
    print('----------------------------')
    print('1. Cargar Inventario ')
    print('2. Modificar Inventario')
    print('3. Generar Reporte')
    print('----------------------------')
    eleccion = input('Seleccione una opcion: ')
    if eleccion =='1':
        print('Opcion 1')
        cargar()
        return menu()
    elif eleccion == '2':
        print('Opcion 2')
        modificar()
        menu()

    elif eleccion == '3':
        print('Opcion 3')
        guardar_productos_en_archivo()
    else:
        print('Opcion incorrecta')
        print('Intente otra vez')
        menu()

lista_productos = []


def guardar_productos_en_archivo():
    data = []
    for producto in lista_productos:
        valor_total = producto.stock * producto.precio
        data.append([producto.nombre, producto.stock, producto.precio, producto.ubicacion, valor_total])
    headers = ["Nombre", "Stock", "Precio", "Ubicación", "Valor Total"]

    # usar w para sobreescribir, si fuese a necesitar agregar usar 'a'
    with open('reporte_202004071.txt', 'w') as archivo:
        archivo.write(tabulate(data, headers, tablefmt="pretty"))#      https://www.youtube.com/watch?v=Yq0lbu8goeA
        print('Informe guardado en "reporte_202004071.txt".')


# Llama a esta función para generar el informe y guardarlos en "reporte.txt"
guardar_productos_en_archivo()
def imprimir_productos():
    data = []
    for producto in lista_productos:
        data.append([producto.nombre, producto.stock, producto.precio, producto.ubicacion])
    headers = ["Nombre", "Stock", "Precio", "Ubicacion"]
    print(tabulate(data, headers, tablefmt="pretty"))

def cargar():
    with open('inventario.inv', 'r') as archivo:#usare with por que dice que esto asegura el cierre del archivo cuando termine
        for linea in archivo:
            if linea.startswith("crear_producto"):
                print('crear')
                partes = linea.strip().split(';')
                if len(partes) == 4:# len para medir la longitud de la lista partes la cual contendra nombre,stock,precio,ubicacion
                    nombre = partes[0].split(' ')[1]#indicando que nombre sera partes[0] que es crear_producto nombre
                    stock = int(partes[1])#guardando en un int el stock del producto
                    precio = float(partes[2])# y en un float el precio este es partes 2 por que es nombre0 sctock 1 precio 2
                    ubicacion = partes[3]
                    producto = Producto(nombre, stock, precio, ubicacion)#creando un objeto de la clase Producto para agregarlo al listado
                    lista_productos.append(producto)


    imprimir_productos()


def modificar():
    try:
        with open('movimiento.mov', 'r') as archivo_movimientos:
            for linea in archivo_movimientos:
                partes = linea.strip().split(' ')
                accion = partes[0]
                datos = partes[1:]
                if accion == "agregar_stock":
                    nombre, cantidad, ubicacion = datos[0].split(';')
                    agregar_stock(nombre, int(cantidad), ubicacion)
                elif accion == "vender_producto":
                    nombre, cantidad, ubicacion = datos[0].split(';')
                    vender_producto(nombre, int(cantidad), ubicacion)
    except FileNotFoundError:
        print("El archivo de movimientos 'movimiento.mov' no encontrado.")

def agregar_stock(nombre, cantidad, ubicacion): #de aca corregir que no me agrega de manera correcta si se encuentra un producto sin ubicacion
    producto_encontrado = False  #probando poninendo un false y que siempre que este sea cambiado a true si se encontro el producto

    for producto in lista_productos:
        if producto.nombre == nombre and producto.ubicacion == ubicacion:
            producto.stock += cantidad
            producto_encontrado = True
            break

    if not producto_encontrado:#o se queda en false si no
        print(f"No se encontró el producto '{nombre}' en la ubicación '{ubicacion}'")
    else:
        print("Stock agregado exitosamente")


def vender_producto(nombre, cantidad, ubicacion):
    for producto in lista_productos:
        if producto.nombre == nombre and producto.ubicacion == ubicacion:
            if producto.stock >= cantidad:
                producto.stock -= cantidad
            else:
                print(f"No hay suficiente stock de {nombre} en {ubicacion}")
            return

menu()