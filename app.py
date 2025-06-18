from flask import Flask, render_template, request, redirect, jsonify
from database.db import *
import os
from werkzeug.utils import secure_filename
from utils.validations import validar_formulario, validar_comentario



app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route("/")
def index():
    ultimas_actividades = get_ultimas_actividades()
    return render_template("index.html", ultimas_actividades=ultimas_actividades)



@app.route("/actividades")
def actividades():
    pagina = int(request.args.get("pagina", 1))
    por_pagina = 5
    offset = (pagina - 1) * por_pagina

    actividades = get_actividades_paginadas(offset, por_pagina)
    total_actividades = get_total_actividades()
    total_paginas = (total_actividades + por_pagina - 1) // por_pagina  # redondeo

    return render_template("actividades.html", actividades=actividades, pagina=pagina, total_paginas=total_paginas)


@app.route("/agregar_actividad", methods=["GET", "POST"])
def agregar_actividad():
    if request.method == "POST":
        errores = validar_formulario(request.form, request.files)
        if errores:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre FROM region")
            regiones = cursor.fetchall()
            cursor.execute("SELECT id, nombre, region_id FROM comuna")
            comunas = cursor.fetchall()
            cursor.close()
            conn.close()

            return render_template("formulario.html", errores=errores, regiones=regiones, comunas=comunas)
  
        comuna_id = request.form["comuna_id"]  
        sector = request.form["sector"]
        nombre = request.form["nombre"]
        email = request.form["correo"]
        celular = request.form["numero"]
        fecha_inicio = request.form["fecha_inicio"]
        fecha_termino = request.form["fecha_termino"]
        descripcion = request.form["descripcion"]

    
        actividad_id = insertar_actividad(
            comuna_id, sector, nombre, email, celular,
            fecha_inicio, fecha_termino, descripcion
        )

        
        contactarpor = request.form["contactarpor"]
        identificador = request.form.get("contacto_id") 
        insertar_contacto(contactarpor, identificador, actividad_id)

        

        
        tema = request.form["tema"]
        otro_tema = request.form.get("otro_tema")
        tema_final = "otro" if tema == "otro" else tema
        glosa = otro_tema if tema == "otro" else None
        insertar_tema(tema_final, glosa, actividad_id)

       
        fotos = request.files.getlist("foto")

        if not (1 <= len(fotos) <= 5):
            return "Debes subir entre 1 y 5 fotos", 400

        for foto in fotos:
            if foto.filename == '':
                continue 
            if not allowed_file(foto.filename):
                return f"Archivo inválido: {foto.filename}", 400

            filename = secure_filename(foto.filename)
            ruta = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            foto.save(ruta)
            insertar_foto(ruta, filename, actividad_id)

        return redirect("/")

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre FROM region")
    regiones = cursor.fetchall()

    cursor.execute("SELECT id, nombre, region_id FROM comuna")
    comunas = cursor.fetchall()

    cursor.close()
    conn.close()


    return render_template("formulario.html", regiones=regiones, comunas=comunas)

def get_fotos_por_actividad(actividad_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ruta_archivo FROM foto WHERE actividad_id = %s
    """, (actividad_id,))
    fotos = cursor.fetchall()
    cursor.close()
    conn.close()
    return fotos

@app.route("/actividad/<int:id>")
def detalle_actividad(id):
    actividad = get_actividad_por_id(id)
    fotos = get_fotos_por_actividad(id)
    comentarios = get_comentarios_por_actividad(id)
    if not actividad:
        return "Actividad no encontrada", 404
    return render_template("detalle.html", actividad=actividad, fotos=fotos, comentarios=comentarios, actividad_id=id)



@app.route("/api/comentarios/<int:actividad_id>", methods=["GET"])
def api_get_comentarios(actividad_id):
    comentarios = get_comentarios_por_actividad(actividad_id)
    return jsonify(comentarios)

@app.route("/api/comentarios/<int:actividad_id>", methods=["POST"])
def api_post_comentario(actividad_id):
    nombre = request.form.get("nombre", "").strip()
    texto = request.form.get("texto", "").strip()

    errores = {}
    if not 3 <= len(nombre) <= 80:
        errores["nombre"] = "El nombre debe tener entre 3 y 80 caracteres."
    if len(texto) < 5:
        errores["texto"] = "El comentario debe tener al menos 5 caracteres."

    if errores:
        return jsonify({"errores": errores}), 400

    insertar_comentario(actividad_id, nombre, texto)
    return jsonify({"mensaje": "Comentario agregado exitosamente"})






ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/estadistica")
def estadistica():
    return render_template("estadistica.html")

@app.route("/api/estadistica/actividades_por_dia")
def api_actividades_por_dia():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE(dia_hora_inicio) as fecha, COUNT(*) as cantidad
        FROM actividad
        GROUP BY DATE(dia_hora_inicio)
        ORDER BY fecha
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    data = [{"fecha": row[0].strftime("%Y-%m-%d"), "cantidad": row[1]} for row in resultados]
    return jsonify(data)


@app.route("/api/estadistica/actividades_por_tema")
def api_actividades_por_tema():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tema, COUNT(*) as cantidad
        FROM actividad_tema
        GROUP BY tema
        ORDER BY cantidad DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    data = [{"tema": row[0], "cantidad": row[1]} for row in resultados]
    return jsonify(data)

@app.route("/api/estadistica/actividades_por_franja")
def api_actividades_por_franja():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            DATE_FORMAT(dia_hora_inicio, '%Y-%m') AS mes,
            HOUR(dia_hora_inicio) AS hora
        FROM actividad
    """)
    filas = cursor.fetchall()
    cursor.close()
    conn.close()

    datos = {}

    for mes, hora in filas:
        if mes not in datos:
            datos[mes] = {"mañana": 0, "mediodia": 0, "tarde": 0}
        if hora < 12:
            datos[mes]["mañana"] += 1
        elif 12 <= hora < 18:
            datos[mes]["mediodia"] += 1
        else:
            datos[mes]["tarde"] += 1

    resultado = []
    for mes in sorted(datos.keys()):
        resultado.append({
            "mes": mes,
            "mañana": datos[mes]["mañana"],
            "mediodia": datos[mes]["mediodia"],
            "tarde": datos[mes]["tarde"]
        })

    return jsonify(resultado)


@app.route("/actividades_realizadas")
def actividades_realizadas():
    actividades = get_actividades_realizadas()
    return render_template("realizadas.html", actividades=actividades)




@app.route("/api/evaluar/<int:actividad_id>", methods=["POST"])
def api_evaluar_actividad(actividad_id):
    data = request.get_json()
    nota = data.get("nota")

    if not isinstance(nota, int) or not (1 <= nota <= 7):
        return jsonify({"error": "Nota inválida"}), 400

    promedio = insertar_nota(actividad_id, nota)
    return jsonify({"mensaje": "Nota registrada", "promedio": promedio})



if __name__ == "__main__":
    app.run(debug=True)




