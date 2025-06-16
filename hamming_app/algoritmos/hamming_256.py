import random
import os

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


def codificacion_hamming_256(p):
    for bit_pos in [1, 2, 4, 8, 16, 32, 64, 128]:
        control = calcular_bit_control(p, bit_pos)
        p |= (control << (256 - bit_pos))
    p=calcular_bit_paridad(p)
    return p



def calcular_bit_control(p:int, pos:int) -> int:
    control = 0
    for i in range(pos, 256, pos * 2):
        for j in range(i, i + pos):
            control ^= (p >> (256 - j)) & 1
    return control



def calcular_bit_paridad(p):
    paridad=0
    for i in range (1,256):
        paridad ^= (p >> (256 - i)) & 1
    p^= paridad
    return p



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




def deshamminizacion_256(p,fix_module):
    decodificacion = control_hamming_256(p)
    num = (decodificacion["s7"] << 7) + (decodificacion["s6"] << 6) + (decodificacion["s5"] << 5) + (decodificacion["s4"] << 4) + (decodificacion["s3"] << 3) +(decodificacion["s2"] << 2) + (decodificacion["s1"] << 1) + (decodificacion["s0"] )
    if decodificacion["paridad"] == 0:
        if num==0:
            return decodificacion_hamming_256(p)
        else:
            return -1 #Hay dos errores
    else:
        if num==0:
            #Hay error en el bit de paridad
            if fix_module == 1:
                p = corregir_error_256(p,255) 
                return decodificacion_hamming_256(p)
            else:
                return decodificacion_hamming_256(p)
        else:
            #Hay error en una posición que no es el bit de paridad
            if fix_module == 1:
                p = corregir_error_256(p,num) 
                return decodificacion_hamming_256(p)
            else:
                return decodificacion_hamming_256(p)



def corregir_error_256(p,error):
    return (p ^ (2**256 >> (error))) 


def control_hamming_256(p):
    res={}
    for i,bit_pos in enumerate([1, 2, 4, 8, 16, 32, 64, 128]):
        control = calcular_bit_control_deshamminizacion(p, bit_pos)
        res[f"s{i}"]=control
    paridad=0
    for i in range (1,257):
        paridad ^= (p >> (256 - i)) & 1
    res[f"paridad"]=paridad
    return res



def calcular_bit_control_deshamminizacion(p:int, pos:int) -> int:
    control = 0
    for i in range(pos, 256, pos * 2):
        for j in range(i, i + pos):
            control ^= ((p >> (256 - j)) & 1)
    return control


def decodificacion_hamming_256(p):
    j = 0
    res = 0
    #print(bin(p))
    for i in range(1, 257):
        if (i & (i - 1)) == 0:
            continue
        if j >= 240:
            break
        bit = (p >> (256 - i)) & 1
        res |= (bit << (239 - j))
        j += 1
    return res


def decodificar_archivo_256(file_name_read, file_name_write, arreglar_archivo):
    try:
        with open(file_name_read, "rb") as f, open(file_name_write, "wb") as wr:
            # Leer los primeros 5 bytes (tamaño original en bytes)
            original_len_bytes = f.read(5)
            if len(original_len_bytes) < 5:
                raise ValueError("El archivo codificado está corrupto o incompleto.")
            original_len = int.from_bytes(original_len_bytes, byteorder='big')

            total_decodificado = bytearray()

            while True:
                bloque = f.read(32)
                if len(bloque) == 0:
                    break
                bloque_bytes = int.from_bytes(bloque, byteorder="big")
                num = deshamminizacion_256(bloque_bytes, arreglar_archivo)

                for i in range(30):
                    shift = 232 - (8 * i)
                    byte = (num >> shift) & 0xFF
                    total_decodificado.append(byte)

            # Cortar a longitud original y escribir como binario
            wr.write(total_decodificado[:original_len])

    except FileNotFoundError as e:
        print("Ocurrió un error al abrir los archivos: ", e)
    except Exception as e:
        print("Error: ", e)


#Estamos leyendo mal el archivo

'''----------------------------------------------------------------------------------------------------------------'''

def ingresar_error_256(file_name_read, file_name_write,errores):
    try:
        with open(file_name_read, 'rb') as f, open(file_name_write, 'wb') as wr:
            #Se sacan los primer 4 bytes por el tamaño
            tamaño = f.read(5)
            wr.write(tamaño)
            while True:
                bloque = f.read(32)
                if len(bloque) == 0:
                    break
                bloque_bytes = int.from_bytes(bloque, byteorder='big')
                for i in range(1,errores):
                    if random.randint(0, 1) == 1:
                        error = random.randint(0, 255)
                        mask = 1 << (255 - error)
                        bloque_bytes ^= mask
                wr.write(bloque_bytes.to_bytes(32, byteorder='big'))

    except Exception as e:
        print(f"Error al ingresar error: {e}")

