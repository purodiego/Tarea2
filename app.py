from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/agregar_actividad")
def agregar_actividad():
    return render_template("formulario.html")

@app.route("/actividades")
def actividades():
    return render_template("actividades.html")

if __name__ == "__main__":
    app.run(debug=True)




