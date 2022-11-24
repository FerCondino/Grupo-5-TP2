import csv, os


archivo: str = 'reclamos.csv'
campos: tuple = ('Timestamp', 'Teléfono_celular', 'coord_lat', 'coord_long',
                     'ruta_foto', 'descripción texto', 'ruta_audio')


def cargar_reclamos(archivo) -> list:
    
# Carga todos los datos del archivo en una lista y la devuelve.

    reclamos: list = []
    
    if not os.path.exists(archivo):
        
        return reclamos
    
    with open(archivo) as f:
        
        datos_csv = csv.reader(f)
        encabezado = next(datos_csv)
        
        for item in datos_csv:
            
            reclamos.append(item)
            
            
    return reclamos


def guardar_reclamos(reclamos, archivo) -> None:
    
#Guarda los reclamos en un archivo.
    
    with open(archivo, 'w', newline = '') as f:
        
        datos_csv = csv.writer(f)
        datos_csv.writerow(campos)
        datos_csv.writerows(reclamos)
        
        
def menu_alta(reclamos) -> None:
    
# Guarda un nuevo reclamo.

    print('|||||INGRESO NUEVO RECLAMO|||||','\n')
    
    timestamp: list = []
    
    fecha: int = int(input('Ingrese la fecha: '))
    hora: int = int(input('Ingrese la hora: '))
    timestamp.append([fecha, hora])
    
    celu: int = int(input('Ingrese su número de celular: '))
    coord_latitud: int = int(input('Ingrese la latitud: '))
    coord_longitud: int = int(input('Ingrese la longitud: '))
    ruta_foto: str = input('Ingrese la ruta de la foto: ')
    descripcion: str = input('Ingrese una breve descripción del reclamo: ')
    ruta_audio: str = input('Ingrese la ruta del audio: ')
    print()
    
    reclamos.append([timestamp, celu, coord_latitud, coord_longitud, ruta_foto, descripcion, ruta_audio])
    
    
def main() -> None:
    
    reclamos: list = cargar_reclamos(archivo)
    salir: bool = False
    
    
    while not salir:
        
        pregunta: str = input('Desea ingresar un nuevo reclamo? (s/n): ')
        print()
        
        if (pregunta == 's'):
            
            menu_alta(reclamos)
                   
        else:
            salir = True
            
    
    guardar_reclamos(reclamos, archivo)
            

main()