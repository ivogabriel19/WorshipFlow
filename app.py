from flask import Flask, render_template, request
from flow import cargar_canciones, recomendar_por_tags

app = Flask(__name__)
canciones = cargar_canciones()
historial = []

@app.route("/", methods=["GET", "POST"])
def index():
    global historial

    if request.method == "POST":
        accion = request.form.get("accion")
        if accion == "iniciar":
            historial = []
            cancion_id = request.form.get("cancion")
            cancion = next((c for c in canciones if c["id"] == cancion_id), None)
        elif accion == "tag":
            historial = []
            tag = request.form.get("tag")
            cancion = recomendar_por_tags([tag], canciones, historial)
        elif accion == "skip":
            historial.append(request.form.get("actual_id"))
            actual_tags = request.form.get("actual_tags").split(",")
            cancion = recomendar_por_tags(actual_tags, canciones, historial)
        else:
            cancion = None
    else:
        cancion = None

    return render_template("index.html", cancion=cancion, canciones=canciones)
