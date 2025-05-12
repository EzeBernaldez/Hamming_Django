from django.views.generic import TemplateView
from .algoritmos import hamming_8,hamming_256,hamming_4096, huffman
from .algoritmos.huffman import compactacion_archivo, descompactacion_archivo
import os
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render


def index(request):
    return render(request,'index.html')

def hamming(request):
    return render(request,'hamming.html')

def hamming_response(request):

    if request.method == 'POST':

        archivo = request.FILES.get('archivo')  
        algoritmo = request.POST.get('Hamming')  
        error = request.POST.get('error')
        fix_module = request.POST.get('fix_module')
        fix_module = int(fix_module)
        context = {'error':error}

        if archivo and algoritmo and error:
            ruta = os.path.join(settings.MEDIA_ROOT, algoritmo)
            texto_path = os.path.join(ruta,'texto.txt')

            with open(texto_path, 'wb') as f:
                bloque = ""
                for chunk in archivo.chunks():
                    f.write(chunk)
                    bloque += chunk.decode('utf-8')
                context["texto_plano"] = bloque

            if algoritmo == 'ha1':
                codificacion_path = os.path.join(ruta, 'codificacion.HA1')
                decodificacion_path = os.path.join(ruta,'decodificacion.txt')
                hamming_8.codificar_archivo(texto_path,codificacion_path)
                hamming_8.decodificar_archivo(codificacion_path,decodificacion_path,0)

                with open(codificacion_path,'rb') as f:
                    bloque = f.read().decode('latin-1')
                    context['texto_codificado'] = bloque
                
                with open(decodificacion_path,'rb') as f:
                    bloque = f.read().decode('utf-8')
                    context['texto_decodificado'] = bloque

                if error == '1':
                    context['errores'] = "HE1"
                    if fix_module==1:
                        context['fix'] = "DC1"
                        
                        codificacion_error_path = os.path.join(ruta,'codificacion_error.HE1')
                        decodificacion_error_path = os.path.join(ruta,'decodificacion_sin_error.DC1')
                        hamming_8.ingresar_error(codificacion_path,codificacion_error_path)
                        hamming_8.decodificar_archivo(codificacion_error_path,decodificacion_error_path,fix_module)

                        with open(codificacion_error_path,'rb') as f:
                            bloque = f.read().decode('latin-1')
                            context['texto_codificado_error'] = bloque
                    
                        with open(decodificacion_error_path,'rb') as f:
                            bloque = f.read().decode('utf-8')
                            context['texto_decodificado_sin_error'] = bloque
                    else:
                        context['fix'] = "DE1"
                        codificacion_error_path = os.path.join(ruta,'codificacion_error.HE1')
                        decodificacion_error_path = os.path.join(ruta,'decodificacion_con_error.DE1')
                        hamming_8.ingresar_error(codificacion_path,codificacion_error_path)
                        hamming_8.decodificar_archivo(codificacion_error_path,decodificacion_error_path,fix_module)

                        with open(codificacion_error_path,'rb') as f:
                            bloque = f.read().decode('latin-1')
                            context['texto_codificado_error'] = bloque
                    
                        with open(decodificacion_error_path,'rb') as f:
                            bloque = f.read().decode('utf-8')
                            context['texto_decodificado_con_error'] = bloque
            
            elif algoritmo == 'ha2':
                codificacion_path = os.path.join(ruta, 'codificacion.HA2')
                decodificacion_path = os.path.join(ruta,'decodificacion.txt')
                hamming_256.codificar_archivo_256(texto_path,codificacion_path)
                hamming_256.decodificar_archivo_256(codificacion_path,decodificacion_path,0)

                with open(codificacion_path,'rb') as f:
                    bloque = f.read().decode('latin-1')
                    context['texto_codificado'] = bloque
                
                with open(decodificacion_path,'rb') as f:
                    bloque = f.read().decode('utf-8')
                    context['texto_decodificado'] = bloque

                if error == '1':
                    context['errores'] = "HE2"
                    if fix_module==1:
                        context['fix'] = "DC2"
                        codificacion_error_path = os.path.join(ruta,'codificacion_error.HE2')
                        decodificacion_error_path = os.path.join(ruta,'decodificacion_sin_error.DC2')
                        hamming_256.ingresar_error_256(codificacion_path,codificacion_error_path)
                        hamming_256.decodificar_archivo_256(codificacion_error_path,decodificacion_error_path,fix_module)

                        with open(codificacion_error_path,'rb') as f:
                            bloque = f.read().decode('latin-1')
                            context['texto_codificado_error'] = bloque
                    
                        with open(decodificacion_error_path,'rb') as f:
                            bloque = f.read().decode('utf-8')
                            context['texto_decodificado_sin_error'] = bloque
                    else:
                        context['fix'] = "DE2"
                        codificacion_error_path = os.path.join(ruta,'codificacion_error.HE2')
                        decodificacion_error_path = os.path.join(ruta,'decodificacion_con_error.DE2')
                        hamming_256.ingresar_error_256(codificacion_path,codificacion_error_path)
                        hamming_256.decodificar_archivo_256(codificacion_error_path,decodificacion_error_path,fix_module)

                        with open(codificacion_error_path,'rb') as f:
                            bloque = f.read().decode('latin-1')
                            context['texto_codificado_error'] = bloque
                    
                        with open(decodificacion_error_path,'rb') as f:
                            bloque = f.read().decode('utf-8')
                            context['texto_decodificado_con_error'] = bloque

            else:
                codificacion_path = os.path.join(ruta, 'codificacion.HA3')
                decodificacion_path = os.path.join(ruta,'decodificacion.txt')
                hamming_4096.codificar_archivo_4096(texto_path,codificacion_path)
                hamming_4096.decodificar_archivo_4096(codificacion_path,decodificacion_path,0)
        
                with open(codificacion_path,'rb') as f:
                    bloque = f.read().decode('latin-1')
                    context['texto_codificado'] = bloque
                
                with open(decodificacion_path,'rb') as f:
                    bloque = f.read().decode('utf-8')
                    context['texto_decodificado'] = bloque

                if error == '1':
                    context['errores'] = "HE3"
                    if fix_module==1:
                        context['fix'] = "DC3"
                        codificacion_error_path = os.path.join(ruta,'codificacion_error.HE3')
                        decodificacion_error_path = os.path.join(ruta,'decodificacion_sin_error.DC3')
                        hamming_4096.ingresar_error_4096(codificacion_path,codificacion_error_path)
                        hamming_4096.decodificar_archivo_4096(codificacion_error_path,decodificacion_error_path,fix_module)

                        with open(codificacion_error_path,'rb') as f:
                            bloque = f.read().decode('latin-1')
                            context['texto_codificado_error'] = bloque
                    
                        with open(decodificacion_error_path,'rb') as f:
                            bloque = f.read().decode('utf-8')
                            context['texto_decodificado_sin_error'] = bloque
                    else:
                        context['fix'] = "DE3"
                        codificacion_error_path = os.path.join(ruta,'codificacion_error.HE3')
                        decodificacion_error_path = os.path.join(ruta,'decodificacion_con_error.DE3')
                        hamming_4096.ingresar_error_4096(codificacion_path,codificacion_error_path)
                        hamming_4096.decodificar_archivo_4096(codificacion_error_path,decodificacion_error_path,fix_module)

                        with open(codificacion_error_path,'rb') as f:
                            bloque = f.read().decode('latin-1')
                            context['texto_codificado_error'] = bloque
                    
                        with open(decodificacion_error_path,'rb') as f:
                            bloque = f.read().decode('utf-8')
                            context['texto_decodificado_con_error'] = bloque


        context['MEDIA_URL'] = settings.MEDIA_URL
        context['algoritmo'] = algoritmo
        return render(request,'hamming_response.html',context)

    return HttpResponse("Error: No se ha enviado un archivo o algoritmo no válido.")

def huffman(request):
    return render(request,'huffman.html')


def huffman_response(request):
    context = {}
    
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')

        if archivo:
            ruta = os.path.join(settings.MEDIA_ROOT, 'huff')         
            texto_path = os.path.join(ruta, 'texto.txt')
            
            with open(texto_path, 'wb') as f:
                bloque = ""
                for chunk in archivo.chunks():
                    f.write(chunk)
                    bloque += chunk.decode('utf-8')
                context["texto_plano"] = bloque


            compresion_path = os.path.join(ruta, 'compresion.huf')
            descompresion_path = os.path.join(ruta,'descompresion.dhu')
            compactacion_archivo(texto_path,compresion_path)
            descompactacion_archivo(compresion_path,descompresion_path)

            with open(compresion_path,'rb') as f:
                bloque = f.read().decode('latin-1')
                context['texto_comprimido'] = bloque
                
            with open(descompresion_path,'rb') as f:
                bloque = f.read().decode('utf-8')
                context['texto_descomprimido'] = bloque
    
    context['MEDIA_URL'] = settings.MEDIA_URL
    return render(request, 'huffman_response.html', context)
