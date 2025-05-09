from flask import Flask, render_template, request, redirect
from database.db import *
import os
from werkzeug.utils import secure_filename
from utils.validations import validar_formulario



app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route("/")
def index():
    return render_template("index.html")



@app.route("/actividades")
def actividades():
    actividades = get_actividades()
    return render_template("actividades.html", actividades=actividades)


@app.route("/agregar_actividad", methods=["GET", "POST"])
def agregar_actividad():
    if request.method == "POST":
        errores = validar_formulario(request.form, request.files)
        if errores:
            # Vuelve al formulario mostrando los errores
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre FROM region")
            regiones = cursor.fetchall()
            cursor.execute("SELECT id, nombre, region_id FROM comuna")
            comunas = cursor.fetchall()
            cursor.close()
            conn.close()

            return render_template("formulario.html", errores=errores, regiones=regiones, comunas=comunas)

        region_id = request.form["region_id"]  
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

        return redirect("/actividades")

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre FROM region")
    regiones = cursor.fetchall()

    cursor.execute("SELECT id, nombre, region_id FROM comuna")
    comunas = cursor.fetchall()

    cursor.close()
    conn.close()


    return render_template("formulario.html", regiones=regiones, comunas=comunas)


@app.route("/actividad/<int:id>")
def detalle_actividad(id):
    actividad = get_actividad_por_id(id)
    if not actividad:
        return "Actividad no encontrada", 404
    return render_template("detalle.html", actividad=actividad)



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS







if __name__ == "__main__":
    app.run(debug=True)




