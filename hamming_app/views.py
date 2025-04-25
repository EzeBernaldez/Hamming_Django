from django.views.generic import TemplateView
from .algoritmos import hamming_8
import os
from django.http import HttpResponse
from django.conf import settings


class index(TemplateView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        archivo = request.FILES.get('archivo')  # El archivo subido
        algoritmo = request.POST.get('Hamming')  # El algoritmo seleccionado
        fix_module = request.POST.get('fix_module')

        if archivo and algoritmo == 'ha1':
            # Crear la ruta para el archivo codificado
            ruta = os.path.join(settings.MEDIA_ROOT, 'ha1')
            texto_path = os.path.join(ruta,'texto.txt')
            codificacion_path = os.path.join(ruta, 'codificacion.HA1')
            decodificacion_path = os.path.join(ruta,'decodificacion.HA1')

            # Guardar el archivo en la ruta de destino
            with open(texto_path, 'wb') as f:
                for chunk in archivo.chunks():
                    print(f'Guarda {chunk}')
                    f.write(chunk)

            hamming_8.codificar_archivo(texto_path,codificacion_path)
            hamming_8.decodificar_archivo(codificacion_path,decodificacion_path,fix_module)

            return HttpResponse(f"Éxito")

        return HttpResponse("Error: No se ha enviado un archivo o algoritmo no válido.")
