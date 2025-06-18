from flask import Flask, render_template, request, redirect, url_for, session
import json
from flow import (
    cargar_canciones,
    cargar_estructura_tags,
    init_user_preferences,
    sugerir_siguiente,
    actualizar_preferencias
)

app = Flask(__name__)
app.secret_key = "supersecretkey"

canciones = cargar_canciones()
estructura_tags = cargar_estructura_tags()
pesos = {
    "Temas_Espirituales": 0.6,
    "Estado_Emocional": 0.2,
    "Contexto": 0.1,
    "Genero_cancion": 0.1
}

@app.before_request
def init_session():
    if "prefs" not in session:
        session["prefs"] = init_user_preferences(estructura_tags)
    if "actual_id" not in session:
        session["actual_id"] = canciones[0]["id"]

@app.route("/")
def index():
    actual = next((c for c in canciones if c["id"] == session["actual_id"]), canciones[0])
    return render_template("index.html", cancion=actual)

@app.route("/feedback/<tipo>")
def feedback(tipo):
    actual = next((c for c in canciones if c["id"] == session["actual_id"]), canciones[0])
    if tipo in ["like", "dislike"]:
        prefs = session["prefs"]
        prefs = actualizar_preferencias(prefs, actual, tipo)
        session["prefs"] = prefs

    siguiente = sugerir_siguiente(actual, canciones, session["prefs"], pesos)
    session["actual_id"] = siguiente["id"]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)