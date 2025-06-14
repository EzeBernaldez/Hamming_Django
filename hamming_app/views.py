from django.views.generic import TemplateView
from .algoritmos import hamming_8,hamming_256,hamming_4096
from .algoritmos.huffman import compactacion_archivo, descompactacion_archivo,ver_estadistica
import os
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
import mimetypes
from django.templatetags.static import static
import base64

def index(request):
    return render(request,'index.html')

def hamming(request):
    return render(request,'hamming.html')

def hamming_response(request):

    if request.method == 'POST':
        
        rutas = [os.path.join(settings.MEDIA_ROOT, 'ha1'), os.path.join(settings.MEDIA_ROOT, 'ha2'), os.path.join(settings.MEDIA_ROOT, 'ha3') ]
        
        for ruta in rutas:
            for nombre_archivo in os.listdir(ruta):
                ruta_completa = os.path.join(ruta, nombre_archivo)
                if os.path.isfile(ruta_completa):
                    os.remove(ruta_completa)

        archivo = request.FILES.get('archivo')  
        algoritmo = request.POST.get('Hamming')  
        error = request.POST.get('error')
        fix_module = request.POST.get('fix_module')
        fix_module = int(fix_module)
        context = {'error':error}

        if archivo and algoritmo and error:
            ruta = os.path.join(settings.MEDIA_ROOT, algoritmo)
            file_name = archivo.name
            texto_path = os.path.join(ruta,file_name)

            with open(texto_path, 'wb') as f:
                for chunk in archivo.chunks():
                    f.write(chunk)
                mime,_ = mimetypes.guess_type(texto_path)

                if mime is not None:
                    mime = mimetypes.guess_extension(mime)
                else:
                    # valor por defecto si no se pudo determinar el MIME
                    mime = 'application/octet-stream'
                    
                context["texto_plano"] = {'mime': mime,'url': static(f'{algoritmo}/{file_name}')}

            if algoritmo == 'ha1':
                codificacion_path = os.path.join(ruta, 'codificacion.HA1')
                decodificacion_path = os.path.join(ruta,f'decodificacion{mimetypes.guess_extension(mime)}')
                
                with open(decodificacion_path,'w') as f:
                    pass
                
                hamming_8.codificar_archivo(texto_path,codificacion_path)
                hamming_8.decodificar_archivo(codificacion_path,decodificacion_path,0)

                with open(codificacion_path,'rb') as f:
                    bloque = f.read().decode('latin-1')
                    context['texto_codificado'] = bloque
                
                context['texto_decodificado'] = {'mime': mime,'url': static(f'{algoritmo}/decodificacion{mimetypes.guess_extension(mime)}')}

                if error == '1' or error == '2':
                    context['errores'] = "HE1"
                    
                    if fix_module==1:
                        context['fix'] = "DC1"
                        
                        codificacion_error_path = os.path.join(ruta,'codificacion_error.HE1')
                        decodificacion_error_path = os.path.join(ruta,f'decodificacion_sin_error{mimetypes.guess_extension(mime)}')
                        
                        with open(decodificacion_error_path,'w') as f:
                            pass
                        
                        hamming_8.ingresar_error(codificacion_path,codificacion_error_path,int(error))
                        hamming_8.decodificar_archivo(codificacion_error_path,decodificacion_error_path,fix_module)

                        with open(codificacion_error_path,'rb') as f:
                            bloque = f.read().decode('latin-1')
                            context['texto_codificado_error'] = bloque
                            
                        context['texto_decodificado_sin_error'] = {'mime': mime,'url': static(f'{algoritmo}/decodificacion_sin_error{mimetypes.guess_extension(mime)}')}
                        

                    else:
                        context['fix'] = "DE1"
                        codificacion_error_path = os.path.join(ruta,'codificacion_error.HE1')
                        decodificacion_error_path = os.path.join(ruta,f'decodificacion_con_error{mimetypes.guess_extension(mime)}')
                        
                        with open(decodificacion_error_path,'w') as f:
                            pass
                        
                        hamming_8.ingresar_error(codificacion_path,codificacion_error_path,int(error))
                        hamming_8.decodificar_archivo(codificacion_error_path,decodificacion_error_path,fix_module)

                        with open(codificacion_error_path,'rb') as f:
                            bloque = f.read().decode('latin-1')
                            context['texto_codificado_error'] = bloque

                        context['texto_decodificado_con_error'] = {'mime': mime,'url': static(f'{algoritmo}/decodificacion_con_error{mimetypes.guess_extension(mime)}')}

            
            elif algoritmo == 'ha2':
                codificacion_path = os.path.join(ruta, 'codificacion.HA2')
                decodificacion_path = os.path.join(ruta,f'decodificacion{mimetypes.guess_extension(mime)}')
                        
                with open(decodificacion_error_path,'w') as f:
                            pass
                        
                hamming_256.codificar_archivo_256(texto_path,codificacion_path)
                hamming_256.decodificar_archivo_256(codificacion_path,decodificacion_path,0)

                with open(codificacion_path,'rb') as f:
                    bloque = f.read().decode('latin-1')
                    context['texto_codificado'] = bloque
                    
                context['texto_decodificado'] = {'mime': mime,'url': static(f'{algoritmo}/decodificacion{mimetypes.guess_extension(mime)}')}
                

                if error == '1' or error == '2':
                    context['errores'] = "HE2"
                    if fix_module==1:
                        context['fix'] = "DC2"
                        codificacion_error_path = os.path.join(ruta,'codificacion_error.HE2')
                        decodificacion_error_path = os.path.join(ruta,f'decodificacion_sin_error{mimetypes.guess_extension(mime)}')
                        
                        with open(decodificacion_error_path,'w') as f:
                            pass
                            
                        hamming_256.ingresar_error_256(codificacion_path,codificacion_error_path, int(error))
                        hamming_256.decodificar_archivo_256(codificacion_error_path,decodificacion_error_path,fix_module)

                        with open(codificacion_error_path,'rb') as f:
                            bloque = f.read().decode('latin-1')
                            context['texto_codificado_error'] = bloque
                        
                        context['texto_decodificado_sin_error'] = {'mime': mime,'url': static(f'{algoritmo}/decodificacion_sin_error{mimetypes.guess_extension(mime)}')}
                        
                    
                    else:
                        context['fix'] = "DE2"
                        codificacion_error_path = os.path.join(ruta,'codificacion_error.HE2')
                        decodificacion_error_path = os.path.join(ruta,f'decodificacion_con_error{mimetypes.guess_extension(mime)}')
                        
                        with open(decodificacion_error_path,'w') as f:
                            pass
                        
                        hamming_256.ingresar_error_256(codificacion_path,codificacion_error_path, int(error))
                        hamming_256.decodificar_archivo_256(codificacion_error_path,decodificacion_error_path,fix_module)

                        with open(codificacion_error_path,'rb') as f:
                            bloque = f.read().decode('latin-1')
                            context['texto_codificado_error'] = bloque
                    
                        context['texto_decodificado_con_error'] = {'mime': mime,'url': static(f'{algoritmo}/decodificacion_con_error{mimetypes.guess_extension(mime)}')}
                        

            else:
                codificacion_path = os.path.join(ruta, 'codificacion.HA3')
                decodificacion_error_path = os.path.join(ruta,f'decodificacion{mimetypes.guess_extension(mime)}')
                        
                with open(decodificacion_error_path,'w') as f:
                    pass
                
                hamming_4096.codificar_archivo_4096(texto_path,codificacion_path)
                hamming_4096.decodificar_archivo_4096(codificacion_path,decodificacion_path,0)
        
                with open(codificacion_path,'rb') as f:
                    bloque = f.read().decode('latin-1')
                    context['texto_codificado'] = bloque

                context['texto_decodificado'] = {'mime': mime,'url': static(f'{algoritmo}/decodificacion{mimetypes.guess_extension(mime)}')}

                if error == '1' or error == '2':
                    context['errores'] = "HE3"
                    if fix_module==1:
                        context['fix'] = "DC3"
                        codificacion_error_path = os.path.join(ruta,'codificacion_error.HE3')
                        decodificacion_error_path = os.path.join(ruta,f'decodificacion_sin_error{mimetypes.guess_extension(mime)}')
                        
                        with open(decodificacion_error_path,'w') as f:
                            pass
                        
                        hamming_4096.ingresar_error_4096(codificacion_path,codificacion_error_path, int(error))
                        hamming_4096.decodificar_archivo_4096(codificacion_error_path,decodificacion_error_path,fix_module)

                        with open(codificacion_error_path,'rb') as f:
                            bloque = f.read().decode('latin-1')
                            context['texto_codificado_error'] = bloque
                            
                        context['texto_decodificado_sin_error'] = {'mime': mime,'url': static(f'{algoritmo}/decodificacion_sin_error{mimetypes.guess_extension(mime)}')}
                        
                    
                    else:
                        context['fix'] = "DE3"
                        codificacion_error_path = os.path.join(ruta,'codificacion_error.HE3')
                        decodificacion_error_path = os.path.join(ruta,f'decodificacion_con_error{mimetypes.guess_extension(mime)}')
                        
                        with open(decodificacion_error_path,'w') as f:
                            pass
                        
                        hamming_4096.ingresar_error_4096(codificacion_path,codificacion_error_path, int(error))
                        hamming_4096.decodificar_archivo_4096(codificacion_error_path,decodificacion_error_path,fix_module)

                        with open(codificacion_error_path,'rb') as f:
                            bloque = f.read().decode('latin-1')
                            context['texto_codificado_error'] = bloque
                            
                        context['texto_decodificado_con_error'] = {'mime': mime,'url': static(f'{algoritmo}/decodificacion_con_error{mimetypes.guess_extension(mime)}')}
                        


        context['MEDIA_URL'] = settings.MEDIA_URL
        context['algoritmo'] = algoritmo
        return render(request,'hamming_response.html',context)

    return HttpResponse("Error: No se ha enviado un archivo o algoritmo no válido.")

def hamming_response_decodificar(request):
    
    context = {}
    
    if request.method=='POST':
        archivo = request.FILES.get('archivo')
        fix_module = request.POST.get('fix_module_decodificar')
        
        if archivo and fix_module:
            
            fix_module = int(fix_module)
            
            name_archivo = os.path.basename(archivo.name)
            
            extension = os.path.splitext(name_archivo)[1][1:].lower()
            
            ruta = os.path.join(settings.MEDIA_ROOT, f'ha{extension[2:]}')
            
            if extension == f'ha{extension[2:]}':
                codificacion_path = os.path.join(ruta, f'codificacion.{extension}')
                
            else:
                codificacion_path = os.path.join(ruta, f'codificacion_error.{extension.upper()}')
            
            with open(codificacion_path,'wb') as f:
                for chunk in archivo.chunks():
                    f.write(chunk)

            if fix_module == 1:
                decodificar_path = os.path.join(ruta, f'resultado_decodificado.{extension}')
            else:
                decodificar_path = os.path.join(ruta, f'resultado_decodificado.{extension}')
            
            if extension[2:] == '1':
                hamming_8.decodificar_archivo(codificacion_path,decodificar_path,fix_module)
            elif extension[2:] == '2':
                hamming_256.decodificar_archivo_256(codificacion_path, decodificar_path,fix_module)
            else:
                hamming_4096.decodificar_archivo_4096(codificacion_path, decodificar_path,fix_module)
                
            with open(decodificar_path,'w'):
                pass
            
            mime,_ = mimetypes.guess_type(decodificar_path)
            
            mime, _ = mimetypes.guess_type(archivo_path)

            if mime is not None:
                mime = mimetypes.guess_extension(mime)
            else:
                # valor por defecto si no se pudo determinar el MIME
                mime = 'application/octet-stream'
            
            if fix_module == 0:
                context['texto_decodificado_con_error'] = {'mime': mime,'url': static(f'ha{extension[2:]}/resultado_decodificado{mimetypes.guess_extension(mime)}')}
            else:
                context['texto_decodificado_sin_error'] = {'mime': mime,'url': static(f'ha{extension[2:]}/resultado_decodificado{mimetypes.guess_extension(mime)}')}
            
        return render(request, 'hamming_response_decodificar.html', context)


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
                bloque = b''
                for chunk in archivo.chunks():
                    f.write(chunk)
                    bloque = base64.b64encode(chunk).decode('utf-8')
                context['texto_plano'] = bloque
                    

            compresion_path = os.path.join(ruta, 'compresion.huf')
            compactacion_archivo(texto_path,compresion_path)

            with open(compresion_path, 'rb') as f:
                bloque = base64.b64encode(f.read()).decode('utf-8')
                context['texto_comprimido'] = bloque

    
    tam=ver_estadistica(texto_path,compresion_path)
    
    context["tamaño_original"]=tam["original"] /1000
    context["tamaño_compactado"]=tam["compactado"] /1000
    context["porcentaje"]=tam["porcentaje"]
    
    context['MEDIA_URL'] = settings.MEDIA_URL
    return render(request, 'huffman_response.html', context)



def huffman_response_descomprimir(request):
    context = {}
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')

        if archivo:
            ruta = os.path.join(settings.MEDIA_ROOT, 'huff')
            compresion_path = os.path.join(ruta, 'descomprimir.huf')
            
            with open(compresion_path, 'wb') as f:
                for chunk in archivo.chunks():
                    f.write(chunk)

            descompresion_path = os.path.join(ruta, 'resultado_descomprimido.dhu')
            descompactacion_archivo(compresion_path, descompresion_path)
            
            with open(descompresion_path,'rb') as f:
                bloque = f.read().decode('utf-8')
                context['texto_descomprimido'] = bloque

    context['MEDIA_URL'] = settings.MEDIA_URL
    return render(request, 'huffman_response_descomprimir.html', context)