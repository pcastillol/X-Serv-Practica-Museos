from django.contrib import admin
from .models import Museo, Comentario, Seleccionado, CSS

# Register your models here.

admin.site.register(Museo)
admin.site.register(Comentario)
admin.site.register(Seleccionado)
admin.site.register(CSS)
