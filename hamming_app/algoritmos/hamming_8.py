import random
import os


# Éste método se implementó para modularizar los procesos y se encarga de llamar al método que maneja la codificación de hamming, primero con los primeros 4 bits de información, y luego con los últimos 4 bits de información.
def hamminizacion(p):
    primer=codificacion_hamming(p>>4)
    segundo=codificacion_hamming(p % 16)
    return {"primer" : primer , "segundo" : segundo}


# Éste método realiza la codificación hamming, donde se calculan los bits de control y el parity check, obteniendo un número codificado mediante sumas con corrimientos.
def codificacion_hamming(p):
    control1=(((p & 8) >> 3) + ((p & 4) >> 2)+ ((p & 1))) % 2
    control2=(((p & 8) >> 3) + ((p & 2) >> 1)+ ((p & 1))) % 2
    control3=(((p & 4) >> 2)+ ((p & 2) >> 1) + ((p & 1))) % 2
    paridad=(control1 + control2 + control3 + (((p & 8) >> 3) + ((p & 4) >> 2)+ ((p & 1)) + ((p & 2) >> 1)))%2
    num = (control1 << 7) + (control2 << 6) + ((p & 8) << 2) + (control3 << 4) + ((p & 4) << 1) + ((p & 2) << 1) + ((p & 1) << 1) + paridad
    return num


# Éste método está encargado de la codificación de un archivo cuyo path es pasado por parámetro y es codificado en un archivo cuyo path también es pasado por parámetro. Los archivos se abren en binario para manejar los bloques de bytes. Es importante aclarar que los primeros 5 bytes son reservados para el tamaño en memoria del archivo a codificar.
def codificar_archivo(file_name_read, file_name_write):
    try:
        with open(file_name_read, "rb") as f:
            contenido = f.read()
            original_len = os.path.getsize(file_name_read)
            with open(file_name_write, 'wb') as wr:
                wr.write(original_len.to_bytes(5, byteorder='big'))
                for byte in contenido:
                    hamming = hamminizacion(byte)
                    hamming_bytes = int.to_bytes(hamming['primer'], 1, byteorder='big') + int.to_bytes(hamming['segundo'], 1, byteorder='big')
                    wr.write(hamming_bytes)
    except FileNotFoundError as e:
        print("Ocurrió un error al abrir los archivos: ", e)
    except Exception as e:
        print("Error: ", e)


# Éste método se utiliza para manejar los errores y decodificar, llama a módulos para controlar el bit de paridad (control_bit_paridad), para calcular el síndrome (control_hamming), para corregir el error en caso de que se lo necesite (corregir_error) y para decodificar el byte (decodificacion_hamming). Se calculan de a dos bytes codificados para poder formar un byte decodificado con bits de información, ya sea sin errores como con errores (puede haber 1 o 2 errores, si hay 2 errores doble_error se setea en 1).
def deshamminizacion(p,q,fix_module):
    doble_error = 0
    bytes_codificados = [p,q]
        
    result = {}
    
    for i,byte in enumerate(bytes_codificados):
        
        decodificacion = control_hamming(byte)
        
        if i == 0:
            indice = 'primer'
        else:
            indice = 'segundo'
            
        if control_bit_paridad(byte) == 0:
            if not decodificacion:
                result[indice] = decodificacion_hamming(byte)
            else:
                doble_error = 1
                result[indice] = decodificacion_hamming(byte)
        else:
            if not decodificacion:
                #Hay error en el bit de paridad
                if fix_module == 1:
                    byte = corregir_error(byte,8) 
                    result[indice] = decodificacion_hamming(byte)
                else:
                    result[indice] = decodificacion_hamming(byte)
            else:
                #Hay error en una posición que no es el bit de paridad
                if fix_module == 1:
                    error = (decodificacion["s2"] << 2) + (decodificacion["s1"] << 1) + (decodificacion["s0"] )
                    byte = corregir_error(byte,error) 
                    result[indice] = decodificacion_hamming(byte)
                else:
                    result[indice] = decodificacion_hamming(byte)
                    
    return [doble_error, (result['primer'] << 4) + (result['segundo'])]


# Éste método calcula el síndrome haciendo un xor con las correspondientes posiciones de control.
def control_hamming(p):
    s0 = ((p & 128) >> 7) ^ ((p & 32) >> 5) ^ ((p & 8) >> 3) ^ ((p & 2) >> 1)
    s1 = ((p & 64) >> 6) ^ ((p & 32) >> 5) ^ ((p & 4) >> 2) ^ ((p & 2) >> 1)
    s2 = ((p & 16) >> 4) ^ ((p & 8) >> 3) ^ ((p & 4) >> 2) ^ ((p & 2) >> 1)

    if (s0 or s1 or s2):
        return {"s0": s0, "s1": s1, "s2": s2}
    else:
        return {}


# Éste método realiza el control de paridad con un xor, si es 0 el número cumple con la paridad, y si es 1 no lo cumple.
def control_bit_paridad(p):
    return ((p & 128) >> 7) ^ ((p & 64) >> 6) ^ ((p & 32) >> 5) ^ ((p & 16) >> 4) ^ ((p & 8) >> 3) ^ ((p & 4) >> 2) ^ ((p & 2) >> 1) ^ (p & 1)


# Éste método permite extraer los bits de información del número codificado
def decodificacion_hamming(p):
    return ((p & 32) >> 2) + ((p & 8) >> 1) + ((p & 4) >> 1) + ((p & 2) >> 1)


# Éste método corrige el error en la posición indicada por el parámetro de entrada error. Se realiza un xor entre el número a corregir y un número con un 1 en la posición indicada por error 
def corregir_error(p, error):
    return (p ^ (256 >> error))


# Éste método maneja la decodificación del archivo, el cual extrae mediante el path pasado en file_name_read, realiza correcciones de errores si arreglar_archivo es 1, y lo escribe en un archivo cuyo path se envía en file_name_write. Es importante aclarar que se extraen los primeros 5 bytes del archivo para escribir la misma cantidad de bytes del archivo que fue codificado. Si hay doble error en el archivo se retorna un 1, de lo contrario un 0.
def decodificar_archivo(file_name_read, file_name_write, arreglar_archivo):
    try:
        with open(file_name_read, "rb") as f, open(file_name_write,'wb') as wr:
            contenido = f.read()
            original_byte= contenido[0:5]

            contenido=contenido[5:]
            
            longitud = len(contenido)
            if not contenido:
                return
            contenido = int.from_bytes(contenido,byteorder='big')
            original_len = int.from_bytes(original_byte, byteorder='big')
            total_decodificado = bytearray()
            
            doble_error_general = 0
            for i in range(1,longitud,2):
                primer = (contenido >> (8 * (longitud-i))) & 0xFF
                segundo = (contenido >> (8 * (longitud-(i+1)))) & 0xFF
                ddeshamminizacion = deshamminizacion(primer,segundo,arreglar_archivo)
                doble_error_general = max(ddeshamminizacion[0],doble_error_general)
                total_decodificado.append(ddeshamminizacion[1])
                
            wr.write(total_decodificado[:original_len])
            return doble_error_general
    except FileNotFoundError as e:
        print("Ocurrió un error al abrir los archivos: ", e)
    except Exception as e:
        print("Error al decodificar archivo: ", e)


# Éste método es una propuesta de la cátedra para ingresar 1 o 2 errores por módulo. Aquí se utiliza un módulo random para que las probabilidades de error sean equiprobables.
def ingresar_error(file_name_read,file_name_write,errores):
    try:
        with open(file_name_read, 'rb') as f, open(file_name_write, 'wb') as wr:
            tamaño = f.read(5)
            wr.write(tamaño)
            while True:
                bloque = f.read(1)
                bloque_bytes = int.from_bytes(bloque,byteorder='big')
                if(len(bloque)==0):
                    break
                error_elegido = -1
                for i in range(0,errores):
                    if random.randint(0,1) == 1:
                        error = random.randint(0,7)
                        if error != error_elegido:
                            error_elegido = error
                            mask = 1 << error
                            bloque_bytes^= mask
                wr.write(bloque_bytes.to_bytes(1,byteorder='big'))

    except Exception as e:
        print(f"Error al ingresar error: {e}")
