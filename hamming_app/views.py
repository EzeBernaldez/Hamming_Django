from django.views.generic import TemplateView
from .algoritmos import hamming_8,hamming_256,hamming_4096
import os
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render


def index(request):
    return render(request,'index.html')


def response(request):

    if request.method == 'POST':

        archivo = request.FILES.get('archivo')  
        algoritmo = request.POST.get('Hamming')  
        error = request.POST.get('error')
        fix_module = request.POST.get('fix_module')
        fix_module = int(fix_module)
        context = {}

        if archivo and algoritmo and error:
            ruta = os.path.join(settings.MEDIA_ROOT, algoritmo)
            texto_path = os.path.join(ruta,'texto.txt')

            with open(texto_path, 'wb') as f:
                bloque = ""
                for chunk in archivo.chunks():
                    f.write(chunk)
                    bloque += chunk.decode('latin-1')
                context["texto_plano"] = bloque

            if algoritmo == 'ha1':
                codificacion_path = os.path.join(ruta, 'codificacion.HA1')
                decodificacion_path = os.path.join(ruta,'decodificacion.HA1')
                hamming_8.codificar_archivo(texto_path,codificacion_path)
                hamming_8.decodificar_archivo(codificacion_path,decodificacion_path,0)

                with open(codificacion_path,'rb') as f:
                    bloque = f.read().decode('latin-1')
                    context['texto_codificado'] = bloque
                
                with open(decodificacion_path,'rb') as f:
                    bloque = f.read().decode('latin-1')
                    context['texto_decodificado'] = bloque

                if error == '1':
                    codificacion_error_path = os.path.join(ruta,'codificacion_error.HA1')
                    decodificacion_error_path = os.path.join(ruta,'decodificacion_error.HA1')
                    hamming_8.ingresar_error(codificacion_path,codificacion_error_path)
                    hamming_8.decodificar_archivo(codificacion_error_path,decodificacion_error_path,fix_module)

                    with open(codificacion_error_path,'rb') as f:
                        bloque = f.read().decode('latin-1')
                        context['texto_codificado_error'] = bloque
                
                    with open(decodificacion_error_path,'rb') as f:
                        bloque = f.read().decode('latin-1')
                        context['texto_decodificado_error'] = bloque



            elif algoritmo == 'ha2':
                codificacion_path = os.path.join(ruta, 'codificacion.HA2')
                decodificacion_path = os.path.join(ruta,'decodificacion.HA2')
                hamming_256.codificar_archivo_256(texto_path,codificacion_path)
                hamming_256.decodificar_archivo_256(codificacion_path,decodificacion_path,0)

                with open(codificacion_path,'rb') as f:
                    bloque = f.read().decode('latin-1')
                    context['texto_codificado'] = bloque
                
                with open(decodificacion_path,'rb') as f:
                    bloque = f.read().decode('latin-1')
                    context['texto_decodificado'] = bloque

                if error == '1':
                    codificacion_error_path = os.path.join(ruta,'codificacion_error.HA2')
                    decodificacion_error_path = os.path.join(ruta,'decodificacion_error.HA2')
                    hamming_256.ingresar_error_256(codificacion_path,codificacion_error_path)
                    hamming_256.decodificar_archivo_256(codificacion_error_path,decodificacion_error_path,fix_module)

                    with open(codificacion_error_path,'rb') as f:
                        bloque = f.read().decode('latin-1')
                        context['texto_codificado_error'] = bloque
                
                    with open(decodificacion_error_path,'rb') as f:
                        bloque = f.read().decode('latin-1')
                        context['texto_decodificado_error'] = bloque


            else:
                codificacion_path = os.path.join(ruta, 'codificacion.HA3')
                decodificacion_path = os.path.join(ruta,'decodificacion.HA3')
                hamming_4096.codificar_archivo_4096(texto_path,codificacion_path)
                hamming_4096.decodificar_archivo_4096(codificacion_path,decodificacion_path,0)
        
                with open(codificacion_path,'rb') as f:
                    bloque = f.read().decode('latin-1')
                    context['texto_codificado'] = bloque
                
                with open(decodificacion_path,'rb') as f:
                    bloque = f.read().decode('latin-1')
                    context['texto_decodificado'] = bloque

                if error == '1':
                    codificacion_error_path = os.path.join(ruta,'codificacion_error.HA3')
                    decodificacion_error_path = os.path.join(ruta,'decodificacion_error.HA3')
                    hamming_4096.ingresar_error_4096(codificacion_path,codificacion_error_path)
                    hamming_4096.decodificar_archivo_4096(codificacion_error_path,decodificacion_error_path,fix_module)

                    with open(codificacion_error_path,'rb') as f:
                        bloque = f.read().decode('latin-1')
                        context['texto_codificado_error'] = bloque
                
                    with open(decodificacion_error_path,'rb') as f:
                        bloque = f.read().decode('latin-1')
                        context['texto_decodificado_error'] = bloque

        return render(request,'response.html',context)

    return HttpResponse("Error: No se ha enviado un archivo o algoritmo no válido.")
