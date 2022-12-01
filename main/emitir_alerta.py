import csv


def leer_denuncias(denuncias) -> list:

    '''
    Lee todas las denuncias en BaseDenuncias.csv y las guarda en una lista.
    Pre: Recibe la lista denuncias vacía.
    Post: Devuelve la lista denuncias con cada denuncia leida.
    '''
    
    with open('BaseDenuncias.csv', 'r') as archivo:
        csv_reader = csv.reader(archivo, delimiter = ',')
        next(csv_reader)
        
        
        for denuncia in csv_reader:
            denuncias.append(denuncia)

    
    return denuncias
        
        
def detectar_sospechoso(denuncias):

    '''
    Detecta patentes sospechosas y muestra por pantalla la ubicación y fecha.
    Pre: Recibe la lista denuncias.
    Post: No devuelve nada por ser un procedimiento.
    '''    
    
    with open('robados.txt', 'r') as archivo:
        
        for robado in archivo:
            
            for denuncia in denuncias:
                
                if (denuncia[6] == robado.strip()):
                    
                    print('------ALERTA------','\n')
                    print('------INFRACCIÓN DE AUTO SOSPECHOSO------', '\n')
                    print(f'Ubicación: {denuncia[4]}, Fecha: {denuncia[1]}')
                    print()
                    
                       
def main() -> None:
    denuncias: list = []
    
    leer_denuncias(denuncias)
    detectar_sospechoso(denuncias)
    
main()