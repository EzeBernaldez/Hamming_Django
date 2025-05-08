import random

def hamminizacion(p):
    primer=codificacion_hamming(int((ord(p)))>>4)
    segundo=codificacion_hamming(int((ord(p))% 16))
    return {"primer" : primer , "segundo" : segundo}


def codificacion_hamming(p):
    control1=(((p & 8) >> 3) + ((p & 4) >> 2)+ ((p & 1))) % 2
    control2=(((p & 8) >> 3) + ((p & 2) >> 1)+ ((p & 1))) % 2
    control3=(((p & 4) >> 2)+ ((p & 2) >> 1) + ((p & 1))) % 2
    paridad=(control1 + control2 + control3 + (((p & 8) >> 3) + ((p & 4) >> 2)+ ((p & 1)) + ((p & 2) >> 1)))%2
    num=0
    num = (control1 << 7) + (control2 << 6) + ((p & 8) << 2) + (control3 << 4) + ((p & 4) << 1) + ((p & 2) << 1) + ((p & 1) << 1) + paridad
    return num


def deshamminizacion(p,q,fix_module):
    decodificacion = control_hamming(p)
    if control_bit_paridad(p) == 0:
        if not decodificacion:
            result= {'primer': decodificacion_hamming(p)}
        else:
            return -1 #Hay dos errores
    else:
        if not decodificacion:
            #Hay error en el bit de paridad
            if fix_module == 1:
                p = corregir_error(p,8) 
                result = {'primer': decodificacion_hamming(p)}
            else:
                result= {'primer': decodificacion_hamming(p)}
        else:
            #Hay error en una posición que no es el bit de paridad
            if fix_module == 1:
                error = (decodificacion["s2"] << 2) + (decodificacion["s1"] << 1) + (decodificacion["s0"] )
                p = corregir_error(p,error) 
                result = {'primer': decodificacion_hamming(p)}
            else:
                result= {'primer': decodificacion_hamming(p)}


    decodificacion = control_hamming(q)
    if control_bit_paridad(q) == 0:
        if not decodificacion:
            result['segundo']= decodificacion_hamming(q)
        else:
            return -1 #Hay dos errores
    else:
        if not decodificacion:
            #Hay error en el bit de paridad
            if fix_module == 1:
                q = corregir_error(q,8) 
                result ['segundo'] =  decodificacion_hamming(q)
            else:
                result ['segundo'] =  decodificacion_hamming(q)
        else:
            #Hay error en una posición que no es el bit de paridad
            if fix_module == 1:
                error = (decodificacion["s2"] << 2) + (decodificacion["s1"] << 1) + (decodificacion["s0"] )
                q = corregir_error(q,error) 
                result ['segundo'] =  decodificacion_hamming(q)
            else:
                result ['segundo'] =  decodificacion_hamming(q)
    return (result['primer'] << 4) + (result['segundo'])


def control_hamming(p):
    s0 = ((p & 128) >> 7) ^ ((p & 32) >> 5) ^ ((p & 8) >> 3) ^ ((p & 2) >> 1)
    s1 = ((p & 64) >> 6) ^ ((p & 32) >> 5) ^ ((p & 4) >> 2) ^ ((p & 2) >> 1)
    s2 = ((p & 16) >> 4) ^ ((p & 8) >> 3) ^ ((p & 4) >> 2) ^ ((p & 2) >> 1)

    if (s0 or s1 or s2):
        return {"s0": s0, "s1": s1, "s2": s2}
    else:
        return {}


def control_bit_paridad(p):
    return ((p & 128) >> 7) ^ ((p & 64) >> 6) ^ ((p & 32) >> 5) ^ ((p & 16) >> 4) ^ ((p & 8) >> 3) ^ ((p & 4) >> 2) ^ ((p & 2) >> 1) ^ (p & 1)


def decodificacion_hamming(p):
    return ((p & 32) >> 2) + ((p & 8) >> 1) + ((p & 4) >> 1) + ((p & 2) >> 1)


def corregir_error(p, error):
    return (p ^ (256 >> error))



def codificar_archivo(file_name_read, file_name_write):
    try:
        with open(file_name_read, "rb") as f:
            contenido = f.read().decode('utf-8')
            with open(file_name_write, 'wb') as wr:
                for i in range(0,len(contenido)):
                    hamming = hamminizacion(contenido[i])
                    hamming = int.to_bytes(hamming['primer'],1,byteorder='big') + int.to_bytes(hamming['segundo'],1,byteorder='big')
                    wr.write(hamming)
    except FileNotFoundError as e:
        print("Ocurrió un error al abrir los archivos: ", e)
    except Exception as e:
        print("Error: ", e)


def decodificar_archivo(file_name_read, file_name_write, arreglar_archivo):
    try:
        with open(file_name_read, "rb") as f:
            contenido = f.read()
            longitud = len(contenido)
            if not contenido:
                return
            contenido = int.from_bytes(contenido,byteorder='big')
            with open(file_name_write, 'w') as wr:
                for i in range(1,longitud,2):
                    primer = (contenido >> (8 * (longitud-i))) & 0xFF
                    segundo = (contenido >> (8 * (longitud-(i+1)))) & 0xFF
                    if(deshamminizacion(primer,segundo,arreglar_archivo) == "\n"):
                        pass
                    else:
                        wr.write(f"{chr(deshamminizacion(primer,segundo,arreglar_archivo))}")
    except FileNotFoundError as e:
        print("Ocurrió un error al abrir los archivos: ", e)
    except Exception as e:
        print("Error al decodificar archivo: ", e)


def ingresar_error(file_name_read,file_name_write):
    try:
        with open(file_name_read, 'rb') as f, open(file_name_write, 'wb') as wr:
            while True:
                bloque = f.read(1)
                bloque_bytes = int.from_bytes(bloque,byteorder='big')
                if(len(bloque)==0):
                    break
                if random.randint(0,1) == 1:
                    error = random.randint(0,7)
                    mask = 1 << error
                    bloque_bytes^= mask
                wr.write(bloque_bytes.to_bytes(1,byteorder='big'))
        
    except Exception as e:
        print(f"Error al ingresar error: {e}")