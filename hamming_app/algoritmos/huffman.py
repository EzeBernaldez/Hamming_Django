import heapq
from collections import Counter
import os

'''-----------------------------------------------------Tabla de frecuencias-------------------------------------------------------------------'''

# Éste método utiliza el módulo Counter para manejar eficientemente (en tiempos) la asignación de frecuencias, es decir que devuelve un diccionario con la probabilidad de ocurrencia de cada uno de los bytes leídos.
def tabla_frecuencia(content) -> dict:
    total = len(content)
    frecuencias = Counter(content)
    return dict(sorted({byte: freq / total for byte, freq in frecuencias.items()}.items(), key=lambda x: x[1], reverse=True))



'''-----------------------------------------------------Compactación-------------------------------------------------------------------'''

# Ésta clase se defina para manejar la estructura encargada del proceso de reducción de huffman, es decir que tenemos nodos con atributos como el byte que lo caracteriza (el símbolo), la frecuencia de aparición de ese símbolo, los hijos izquiedos y derechos de tal nodo, y la cantidad de derivaciones de tal nodo (es decir la cantidad de reducciones que se realizó para llegar a la creación de ese nodo). Además del método de inicialización se define el método cuyo objetivo es la comparación de menor, la cual servirá para la implementación de la estructura de datos elegida por el team, es decir el heap o parva de mínimos.
class Nodo:

    def __init__(self,byte=b'0',frecuencia=None,derivaciones=0):
        self.byte = byte
        self.frecuencia = frecuencia 
        self.left = None
        self.rigth = None
        self.derivaciones = derivaciones

    def __lt__(self, other):
        if self.frecuencia < other.frecuencia:
            return True 
        elif self.frecuencia == other.frecuencia:
            return self.derivaciones < other.derivaciones 


# Éste método lee el archivo a compactar cuyo path se pasó como parámetro de entrada file_read, y escribe la compactación en file_write. Tal método llama inicialmente a tabla_frecuencia para obtener la probabilidad de ocurrencia de cada byte, luego inicializa un heap de mínimos cuyos componentes son nodos, dando como resultado un heap con todos nodos hojas, y se va realizando el proceso de reducción para obtener una estructura por la cual se puede realizar el proceso de asignación, es decir asignar a cada byte un código que lo caracterice basándonos en el algoritmo de huffman. Es necesario alcarar que en el archivo compactado se almacena, en 2 bytes, la cantidad de caracteres del diccionario utilizado para codificar, luego se almacena el diccionario con las codificaciones para cada byte, y luego se envía el código compactado con huffman (al principio puede contener 0's debido a que la codificación puede ocupar menor cantidad de bits que no llegan al byte).
def compactacion_archivo(file_read,file_write):
    
    codificacion = {}

    try:
        with open(file_read, 'rb') as f:
            content = f.read()
        
            frecuencias_dict = tabla_frecuencia(content)
            frecuencias_heap = [Nodo(byte,frecuencia) for byte, frecuencia in frecuencias_dict.items()]
            heapq.heapify(frecuencias_heap)

            if len(frecuencias_dict) == 1:
                codificacion = {k:format(1,'01b') for k,_ in frecuencias_dict.items()}
            else:
                while len(frecuencias_heap) > 1:
                    minimo_minimo = heapq.heappop(frecuencias_heap)
                    minimo_maximo = heapq.heappop(frecuencias_heap)
                    tupla = Nodo(frecuencia=minimo_maximo.frecuencia + minimo_minimo.frecuencia,derivaciones= max(minimo_maximo.derivaciones,minimo_minimo.derivaciones)+1,byte=[minimo_maximo.byte,minimo_minimo.byte])

                    tupla.left = minimo_minimo  # izquierdo = menos frecuente
                    tupla.rigth = minimo_maximo
                    heapq.heappush(frecuencias_heap,tupla)

                raiz = frecuencias_heap[0]
                codificacion = generar_codigos(raiz,0,codificacion,0)


            #Ahora tenemos que escribir el archivo codificado

            with open(file_write,'wb') as wr:

                codificacion_bytes = ''.join(codificacion[byte] for byte in content)

                codificacion_dict = format(len(codificacion),'016b')
                #Cuantos bytes hay en la codificacion.
                longitud_dict = 2

                for key,value in codificacion.items():
                    longitud = len(value)
                    codificacion_dict += format(key,'08b') + format(longitud,'08b') + (value.zfill(8 * ((longitud + 7) // 8))) #por cada byte, guardar el número de bits que utiliza la codificacion y la codificación propiamente dicha
                    longitud_dict += 2 + ((longitud + 7) // 8)


                cantidad_ceros = (8 - (len(codificacion_bytes) % 8)) % 8

                longitud = (len(codificacion_bytes) + 7) // 8

                codificacion_bytes = int(codificacion_bytes,2)

                codificacion_dict = int(codificacion_dict,2)
                
                
                codificacion_bytes = codificacion_dict.to_bytes(longitud_dict,'big')  + cantidad_ceros.to_bytes(1,'big') + codificacion_bytes.to_bytes(longitud,'big')
                

                
                wr.write(codificacion_bytes)

    except Exception as e:
        print('Error en la codificación', e)


# Éste método consiste en una recursión, la cual está encargada del proceso de asignación de códigos a cada uno de los símbolos (en este caso bytes).
def generar_codigos(nodo, codigo_actual, codificacion, shift):
    if nodo is None:
        return
    if nodo.left is None and nodo.rigth is None:
        codificacion[nodo.byte] = format(codigo_actual, f'0{shift}b')
        return 
    generar_codigos(nodo.left,  (codigo_actual << 1), codificacion, shift+1)
    generar_codigos(nodo.rigth, (codigo_actual << 1) | 1, codificacion, shift+1)
    return codificacion




'''-----------------------------------------------------Descompactación-------------------------------------------------------------------'''


# Éste método se utiliza para descomprimir un archivo cuyo path es enviado como parámetro de entrada file_read y se escribe en file_write. Inicialmente lee todo el contenido del archivo, luego extraemos el diccionario de codificaciones leyendo, primeramente la cantidad de caracteres del diccionario, luego la cantidad de 0's iniciales, y por último el diccionario mismo, que contiene el byte representativo, la longitud de la codificación y la codificación. Por último se realiza la decodificación mediante parsing de los códigos con el texto comprimido y las codificaciones. A medida que vaya parseando, se va asignando en una variable el texto descomprimido y luego se escribe en bytes en el archivo descomprimido.
def descompactacion_archivo(file_read,file_write):
    try:
        with open(file_read,'rb') as f:
            content = f.read() 
            if not content:
                return
            
            content_bytes = ''.join(format(byte, '08b') for byte in content)


            #Extraemos el diccionario de codificaciones
            codificacion_dict = {}

            cantidad_caracteres_codificacion = content_bytes[0:16]
            

            cantidad_caracteres_codificacion = int(cantidad_caracteres_codificacion,2)

            content_bytes = content_bytes[16:]

            for i in range(0,cantidad_caracteres_codificacion):
                byte = content_bytes[0:8]

                longitud_codificacion = content_bytes[8:16]
                longitud_codificacion = int(longitud_codificacion,2)

                longitud = 8 * ((longitud_codificacion + 7 ) // 8)

                codificacion = content_bytes[16: 16 + longitud]
                codificacion = codificacion[longitud-longitud_codificacion:]


                codificacion_dict[byte] = codificacion
                
                content_bytes = content_bytes[16 + longitud:]
            
            #Contamos cuantos 0's hay de relleno

            cantidad_ceros = content_bytes[0:8]
            cantidad_ceros = int(cantidad_ceros,2)

            content_bytes = content_bytes[8 + cantidad_ceros:] #Tenemos que sacarle los 0's agregados para enviar palabras (bytes) al archivo codificado

            #Decodificamos
            bits_seleccionados = ''
            mensaje = ''

            codificacion_dict_reverse = {value:key for key,value in codificacion_dict.items()}
            for bits in content_bytes:
                bits_seleccionados += bits
                if bits_seleccionados in codificacion_dict_reverse:
                    mensaje += codificacion_dict_reverse[bits_seleccionados]
                    bits_seleccionados = ''

            longitud_mensaje = (len(mensaje) + 7) // 8
            
            mensaje_bytes = int(mensaje,2)
            
            mensaje_bytes = mensaje_bytes.to_bytes(longitud_mensaje,'big')

            with open(file_write, 'wb') as wr:
                wr.write(mensaje_bytes)
    except Exception as e:
        print(f'Error en la descompactación: {e}')


'''-----------------------------------------------------Ver estadística-------------------------------------------------------------------'''


# Éste método es propuesto por la cátedra y consiste en visualizar el porcentaje de compactación de un archivo al ser aplicado huffman. Primeramente recupera el tamaño del archivo original, luego el del archivo compactado, y obtiene el porcentaje de compresión.
def ver_estadistica(file_original,file_compactado):
    tamaño_original = os.path.getsize(file_original)
    tamaño_compactado = os.path.getsize(file_compactado)

    dic={}
    dic["original"]=tamaño_original
    dic["compactado"]=tamaño_compactado
    dic["porcentaje"] = (((tamaño_compactado - tamaño_original) / tamaño_original) * 100)
    
    return dic

