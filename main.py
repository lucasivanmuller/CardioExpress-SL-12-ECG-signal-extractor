import PyPDF2
import re
import matplotlib.pyplot as plt

def extract_ECG_signal(pdf_file_path):
    """Extrae la señal de ECG como una serie de puntos a partir de un PDF.
    Devuelve un diccionario {derivation: signal}, siendo signal una serie ordenada de puntos ('X', 'Y')
    que representa una muestra de la señal"""
    
    ECG_signal = {} # Diccionario a devolver
    DERIVATIONS = ("DI", "DII", "DIII", "AVR", "AVL", "AVF", "V1", "V2", "V3", "V4", "V5", "V6", "DII largo")
    
    #Abre el PDF y lee la primera página
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        page = pdf_reader.pages[0]
        
        # Busca los datos del stream de todas las señales, 
        # los decodifica de ASCII a UTF-8 y convierte de bytes a string
        stream = str(page['/Contents'].get_object().get_data().decode('utf-8', errors='ignore')) 
        
        # Divide las 13 derivaciones según un patrón fijo que precede cada señal de la derivación
        separation_pattern = "j\r\nn\r\n"
        splitted_stream = re.split(separation_pattern, stream)[1:14] # Excluye el [0] (encabezado)
        
        # Patrón que matchea los pares de numeros decimales de tipo: "737.29 32.11"
        # Cada uno de estos representa las coordenadas X e Y de un punto de la señal.
        point_pattern = r'\b(\d+\.\d+)\s(\d+\.\d+)\s[lL]\b'
        for (index, derivation) in enumerate(DERIVATIONS):
            # Extrae todos los puntos (X, Y) de una derivación y los guarda como 
            # una lista de puntos [(X1, Y1), (X2, Y2)...]
            ECG_signal[derivation] = re.findall(point_pattern, splitted_stream[index]) 
            
    return ECG_signal 


def visualizate_derivation(ECG_signal, derivation):
    derivation_signal = ECG_signal[derivation]
    x_coords = [float(coord[0]) for coord in derivation_signal]
    y_coords = [float(coord[1]) for coord in derivation_signal]
    plt.plot(x_coords, y_coords, linestyle='-', color='b')
    plt.grid(True)
    plt.show()


visualizate_derivation(extract_ECG_signal("C:\\Users\\lucas\\Downloads\\567547-20230928-035831.pdf"), "V3")
