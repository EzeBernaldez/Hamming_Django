import heapq
from collections import Counter

'''-----------------------------------------------------Tabla de frecuencias-------------------------------------------------------------------'''


def tabla_frecuencia(content) -> dict:
    total = len(content)
    frecuencias = Counter(content)
    return dict(sorted({char: freq / total for char, freq in frecuencias.items()}.items(), key=lambda x: x[1], reverse=True))



'''-----------------------------------------------------Compactación-------------------------------------------------------------------'''


class Nodo:

    def __init__(self,caracter='',frecuencia=None,derivaciones=0):
        self.caracter = caracter
        self.frecuencia = frecuencia 
        self.left = None
        self.rigth = None
        self.derivaciones = derivaciones

    def __lt__(self, other):
        if self.frecuencia < other.frecuencia:
            return self.frecuencia < other.frecuencia 
        elif self.frecuencia == other.frecuencia:
            return self.derivaciones < other.derivaciones 


def compactacion_archivo(file_read,file_write):
    
    codificacion = {}

    try:
        with open(file_read,'r',encoding="utf-8") as f:
            content = f.read()
        
            frecuencias_dict = tabla_frecuencia(content)
            frecuencias_heap = [Nodo(caracter,frecuencia) for caracter, frecuencia in frecuencias_dict.items()]
            heapq.heapify(frecuencias_heap)

            if len(frecuencias_dict) == 1:
                codificacion = {k:'1' for k,v in frecuencias_dict.items()}
            else:
                while len(frecuencias_heap) > 1:
                    minimo_minimo = heapq.heappop(frecuencias_heap)
                    minimo_maximo = heapq.heappop(frecuencias_heap)
                    tupla = Nodo(frecuencia=minimo_maximo.frecuencia + minimo_minimo.frecuencia,derivaciones= max(minimo_maximo.derivaciones,minimo_minimo.derivaciones)+1,caracter=[minimo_maximo.caracter,minimo_minimo.caracter])

                    tupla.left = minimo_minimo  # izquierdo = menos frecuente
                    tupla.rigth = minimo_maximo
                    heapq.heappush(frecuencias_heap,tupla)

                raiz = frecuencias_heap[0]
                codificacion = generar_codigos(raiz,0,codificacion,0)


            #Ahora tenemos que escribir el archivo codificado
            with open(file_write,'wb') as wr:

                codificacion_bytes = ''.join(codificacion[caracteres] for caracteres in content)

                codificacion_dict = format(len(codificacion),'08b') #Cuantos caracteres hay en la codificacion.
                longitud_dict = 1

                for key,value in codificacion.items():
                    longitud = len(value)
                    codificacion_dict += format((ord(key)),'08b') + format(longitud,'08b') + value.zfill(8 * ((longitud + 7) // 8)) #por cada caracter, guardar el número de bits que utiliza la codificacion y la codificación propiamente dicha
                    longitud_dict += 2 + ((longitud + 7) // 8)


                cantidad_ceros = (8 - (len(codificacion_bytes) % 8)) % 8

                longitud = (len(codificacion_bytes) + 7) // 8

                codificacion_bytes = int(codificacion_bytes,2)

                codificacion_dict = int(codificacion_dict,2)
                

                codificacion_bytes = codificacion_dict.to_bytes(longitud_dict,'big')  + cantidad_ceros.to_bytes(1,'big') + codificacion_bytes.to_bytes(longitud,'big')


                wr.write(codificacion_bytes)

    except:
        print('Algo ocurrió')


def generar_codigos(nodo, codigo_actual, codificacion, shift):
    if nodo is None:
        return
    if nodo.left is None and nodo.rigth is None:
        codificacion[nodo.caracter] = format(codigo_actual, f'0{shift}b')
        return 
    generar_codigos(nodo.left,  (codigo_actual << 1), codificacion, shift+1)
    generar_codigos(nodo.rigth, (codigo_actual << 1) | 1, codificacion, shift+1)
    return codificacion




'''-----------------------------------------------------Descompactación-------------------------------------------------------------------'''


def descompactacion_archivo(file_read,file_write):
    try:
        with open(file_read,'rb') as f:
            content = f.read() 
            if not content:
                return
            
            content_bytes = ''.join(format(byte, '08b') for byte in content)


            #Extraemos el diccionario de codificaciones
            codificacion_dict = {}

            cantidad_caracteres_codificacion = content_bytes[0:8]

            cantidad_caracteres_codificacion = int(cantidad_caracteres_codificacion,2)

            content_bytes = content_bytes[8:]

            for i in range(0,cantidad_caracteres_codificacion):
                caracter = content_bytes[0:8]
                caracter = chr(int(caracter,2))

                longitud_codificacion = content_bytes[8:16]
                longitud_codificacion = int(longitud_codificacion,2)

                longitud = 8 * ((longitud_codificacion + 7 ) // 8)

                codificacion = content_bytes[16: 16 + longitud]
                codificacion = codificacion[longitud-longitud_codificacion:]


                codificacion_dict[caracter] = codificacion
                
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


            with open(file_write,'w',encoding="utf-8") as wr:
                wr.write(mensaje)
    except Exception as e:
        print(e)


'''-----------------------------------------------------Ver estadística-------------------------------------------------------------------'''


def ver_estadistica(file_original,file_compactado,file_descompactado):
    pass
