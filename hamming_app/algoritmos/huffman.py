import heapq
from collections import Counter
import os

'''-----------------------------------------------------Tabla de frecuencias-------------------------------------------------------------------'''


def tabla_frecuencia(content) -> dict:
    total = len(content)
    frecuencias = Counter(content)
    return dict(sorted({byte: freq / total for byte, freq in frecuencias.items()}.items(), key=lambda x: x[1], reverse=True))



'''-----------------------------------------------------Compactación-------------------------------------------------------------------'''


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
                
                print(f'La cantidad de bytes ocupados es: {len(codificacion_bytes.to_bytes(longitud,'big'))}')
                
                codificacion_bytes = codificacion_dict.to_bytes(longitud_dict,'big')  + cantidad_ceros.to_bytes(1,'big') + codificacion_bytes.to_bytes(longitud,'big')
                

                
                wr.write(codificacion_bytes)

    except Exception as e:
        print('Error en la codificación', e)


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
        print(f'Error en la descompactación{e}')


'''-----------------------------------------------------Ver estadística-------------------------------------------------------------------'''


def ver_estadistica(file_original,file_compactado):
    tamaño_original = os.path.getsize(file_original)
    tamaño_compactado = os.path.getsize(file_compactado)

    dic={}
    dic["original"]=tamaño_original
    dic["compactado"]=tamaño_compactado
    dic["porcentaje"] = (((tamaño_compactado - tamaño_original) / tamaño_original) * 100)
    
    return dic

