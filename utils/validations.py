import re
from datetime import datetime


def validar_name(value):
    return value and len(value) > 0 and len(value) <= 200

def validar_sector(value):
    return len(value) <= 100

def validar_email(value):
    return "@" in value and "." in value and len(value) <= 100 

def validar_celular(value):
    return bool(re.match(r'^\+569\d{8}$', value.strip()))

def validar_contactarpor(tipo, valor):
    if tipo == "whatsapp":
        return bool(re.match(r'^\+569\d{8}$', valor.strip()))
    else:
        return 4 <= len(valor.strip()) <= 50

def validar_fecha_fin(fecha_inicio, fecha_fin):
    try:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        return fin > inicio
    except ValueError:
        return False
    
def validar_descripcion(value):
    return len(value) > 0
    

def validar_fotos(lista_archivos):
    lista_filtrada = [f for f in lista_archivos if f.filename.strip() != '']
    if not (1 <= len(lista_filtrada) <= 5):
        return False
    for archivo in lista_filtrada:
        if '.' not in archivo.filename:
            return False
        ext = archivo.filename.rsplit('.', 1)[1].lower()
        if ext not in {'png', 'jpg', 'jpeg', 'gif'}:
            return False
    return True




def validar_formulario(form, files):
    errores = []

    if not validar_name(form.get("nombre", "")):
        errores.append("Nombre inválido")

    if not validar_email(form.get("correo", "")):
        errores.append("Correo inválido")

    if not validar_sector(form.get("sector", "")):
        errores.append("Sector inválido")

    if not validar_celular(form.get("numero", "")):
        errores.append("Celular inválido (+569XXXXXXXX)")

    if not validar_descripcion(form.get("descripcion", "")):
        errores.append("Descripción obligatoria")

    if not validar_contactarpor(form.get("contactarpor", ""), form.get("contacto_id", "")):
        errores.append("Método de contacto inválido")

    if not validar_fecha_fin(form.get("fecha_inicio", ""), form.get("fecha_termino", "")):
        errores.append("Fecha de término debe ser posterior a la de inicio")

    if not validar_fotos(files.getlist("foto")):
        errores.append("Debes subir entre 1 y 5 imágenes válidas")

    return errores
