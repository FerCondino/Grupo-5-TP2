import csv


def leer_denuncias(denuncias) -> list:
    
    with open('BaseDenuncias.csv', 'r') as archivo:
        csv_reader = csv.reader(archivo, delimiter = ',')
        next(csv_reader)
        
        
        for denuncia in csv_reader:
            denuncias.append(denuncia)

    
    return denuncias
        
        
def detectar_sospechoso(denuncias):    
    
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