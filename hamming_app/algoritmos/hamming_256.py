import random
import os


# Éste método se utiliza para crear un número de 256 bits reservando las posiciones donde se colocarán los bits de control, es decir en cada posición potencia de 2 (1, 2, 4, ..., 128). Luego, se llama a la función de codificación (codificacion_hamming_256) para setear los bits de control en las posiciones reservadas.
def crear_numero_256(p):
    # p contiene 240 bits de datos
    j = 0
    res = 0
    for i in range(1, 257):
        if (i & (i - 1)) == 0:  # Potencia de 2: posición de bit de control
            continue
        elif j < 240:
            bit = (p >> (239 - j)) & 1  # Solo tomamos 240 bits
            res |= (bit << (256 - i))
            j += 1
        else:
            # Rellenamos con ceros del 241 al 247 (se agregan automáticamente al mantener res en 0)
            continue
    return codificacion_hamming_256(res)


# Éste método se utiliza como un módulo que engloba el seteo de los bits de control de hamming con el parity check, donde se llama al método calcular_bit_control con las posiciones potencias de 2 y el número a codificar, y luego se llama al método de calcular_bit_paridad para setear el bit de paridad.
def codificacion_hamming_256(p):
    for bit_pos in [1, 2, 4, 8, 16, 32, 64, 128]:
        control = calcular_bit_control(p, bit_pos)
        p |= (control << (256 - bit_pos))
    p=calcular_bit_paridad(p)
    return p


# Éste método se utiliza para calcular los bits de control mediante un for anidado, donde en el primero colocaremos los marcadores desde el cual se debe ir controlando cada bit consecutivo (es decir, para el bit en la posición 16, que controle los primeros 16 bits contando el marcador, y los segundos 16 no, y así sucesivamente), y en el segundo se vaya haciendo un xor con cada bit consecutivo a controlar, para realizar un control de paridad y colocarlo en el bit de control correspondiente.
def calcular_bit_control(p:int, pos:int) -> int:
    control = 0
    for i in range(pos, 256, pos * 2):
        for j in range(i, i + pos):
            control ^= (p >> (256 - j)) & 1
    return control


# Éste método se utiliza para calcular el parity check de todo el bloque codificado.
def calcular_bit_paridad(p):
    paridad=0
    for i in range (1,256):
        paridad ^= (p >> (256 - i)) & 1
    p^= paridad
    return p


# Éste método maneja la codificación de un archivo cuyo path se pasó como parámetro de entrada file_name_read y lo almacena en el archivo file_name_write. Ambos archivos los abrimos en binario para manejar los bytes crudos. Es importante alcarar que se reservan los primeros 5 bytes para poder almacenar el tamaño del archivo a codificar, y si el archivo no alcanza a los 30 bytes necesarios, se rellena con 0s el bloque.
def codificar_archivo_256(file_name_read, file_name_write):
    try:
        with open(file_name_read, "rb") as f, open(file_name_write, "wb") as wr:
            original_len = os.path.getsize(file_name_read)
            # Guardamos los primeros 5 bytes con la longitud original
            wr.write(original_len.to_bytes(5, byteorder='big'))
            while True:
                bloque = f.read(30)
                if len(bloque) == 0:
                    break
                valor = int.from_bytes(bloque, byteorder='big')
                valor <<= (8 * (30 - len(bloque)))  # Relleno si el bloque es menor a 30 bytes
                num = crear_numero_256(valor)
                wr.write(num.to_bytes(32, byteorder='big'))
    except FileNotFoundError as e:
        print("Ocurrió un error al abrir los archivos: ", e)
    except Exception as e:
        print("Error: ", e)


# Éste método se utiliza para manejar los errores y decodificar, llama a módulos para controlar el bit de paridad y para calcular el síndrome (control_hamming_256), para corregir el error en caso de que se lo necesite (corregir_error_256) y para decodificar el byte (decodificacion_hamming_256). El bloque de información obtenido puede no tener errores o tener 1 o 2 errores (en el caso de 2 errores, la primer posición del array devuelto se setea en 1).
def deshamminizacion_256(p,fix_module):
    decodificacion = control_hamming_256(p)
    num = (decodificacion["s7"] << 7) + (decodificacion["s6"] << 6) + (decodificacion["s5"] << 5) + (decodificacion["s4"] << 4) + (decodificacion["s3"] << 3) +(decodificacion["s2"] << 2) + (decodificacion["s1"] << 1) + (decodificacion["s0"] )
    if decodificacion["paridad"] == 0:
        if num==0:
            return [0,decodificacion_hamming_256(p)]
        else:
            return [1,decodificacion_hamming_256(p)] #Hay dos errores
    else:
        if num==0:
            #Hay error en el bit de paridad
            if fix_module == 1:
                p = corregir_error_256(p,255) 
                return [0,decodificacion_hamming_256(p)]
            else:
                return [0,decodificacion_hamming_256(p)]
        else:
            #Hay error en una posición que no es el bit de paridad
            if fix_module == 1:
                p = corregir_error_256(p,num) 
                return [0,decodificacion_hamming_256(p)]
            else:
                return [0,decodificacion_hamming_256(p)]


# Éste método calcula el síndrome y el bit de paridad para ser evaluados en deshamminizacion_256. Llama a un método calcular_bit_contro_deshamminizacion para calcular cada bit de control de hamming, que se colocan en posiciones potencias de 2.
def control_hamming_256(p):
    res={}
    for i,bit_pos in enumerate([1, 2, 4, 8, 16, 32, 64, 128]):
        control = calcular_bit_control(p, bit_pos)
        res[f"s{i}"]=control
    paridad=0
    for i in range (1,257):
        paridad ^= (p >> (256 - i)) & 1
    res[f"paridad"]=paridad
    return res


# Éste método se utiliza para corregir un error realizando un xor entre el número codificado y un número con un 1 en la posición error.
def corregir_error_256(p,error):
    return (p ^ (2**256 >> (error))) 


# Éste método se utiliza para extraer los bits de información del bloque codificado y retornar el número decodificado. Aquí se ignoran los bits en las posiciones potencias de 2 y los bits rellenados con 0s para que la codificación se haga efectiva.
def decodificacion_hamming_256(p):
    j = 0
    res = 0
    for i in range(1, 257):
        if (i & (i - 1)) == 0:
            continue
        if j >= 240:
            break
        bit = (p >> (256 - i)) & 1
        res |= (bit << (239 - j))
        j += 1
    return res


# Éste método maneja la decodificación del archivo, el cual extrae mediante el path pasado en file_name_read, realiza correcciones de errores si arreglar_archivo es 1, y lo escribe en un archivo cuyo path se envía en file_name_write. Es importante aclarar que se extraen los primeros 5 bytes del archivo para escribir la misma cantidad de bytes del archivo que fue codificado. Si hay doble error en el archivo se retorna un 1, de lo contrario un 0.
def decodificar_archivo_256(file_name_read, file_name_write, arreglar_archivo):
    try:
        with open(file_name_read, "rb") as f, open(file_name_write, "wb") as wr:
            # Leer los primeros 5 bytes (tamaño original en bytes)
            original_len_bytes = f.read(5)
            if len(original_len_bytes) < 5:
                raise ValueError("El archivo codificado está corrupto o incompleto.")
            original_len = int.from_bytes(original_len_bytes, byteorder='big')

            total_decodificado = bytearray()
            
            doble_error_general = 0
            while True:
                bloque = f.read(32)
                if len(bloque) == 0:
                    break
                bloque_bytes = int.from_bytes(bloque, byteorder="big")
                doble_error,num = deshamminizacion_256(bloque_bytes, arreglar_archivo)
                doble_error_general = max(doble_error,doble_error_general)
                for i in range(30):
                    shift = 232 - (8 * i)
                    byte = (num >> shift) & 0xFF
                    total_decodificado.append(byte)

            # Cortar a longitud original y escribir como binario
            wr.write(total_decodificado[:original_len])
            
            return doble_error_general

    except FileNotFoundError as e:
        print("Ocurrió un error al abrir los archivos: ", e)
    except Exception as e:
        print("Error: ", e)


# Éste método propuesto por la cátedra permite el ingreso de 1 o dos errores por módulo, cuyas probabilidades son equiprobables.
def ingresar_error_256(file_name_read, file_name_write,errores):
    try:
        print(f'entra con {errores} errores')
        with open(file_name_read, 'rb') as f, open(file_name_write, 'wb') as wr:
            #Se sacan los primer 4 bytes por el tamaño
            tamaño = f.read(5)
            wr.write(tamaño)
            while True:
                bloque = f.read(32)
                if len(bloque) == 0:
                    break
                bloque_bytes = int.from_bytes(bloque, byteorder='big')
                for i in range(0,errores):
                    if random.randint(0, 1) == 1:
                        error = random.randint(0, 255)
                        mask = 1 << (255 - error)
                        bloque_bytes ^= mask
                wr.write(bloque_bytes.to_bytes(32, byteorder='big'))

    except Exception as e:
        print(f"Error al ingresar error: {e}")

