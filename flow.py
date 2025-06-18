import json
import random

# Cargar canciones y estructura de tags
def cargar_canciones(path="data/songs.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def cargar_estructura_tags(path="data/tags.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Calcular similitud por categoría (Jaccard)
def calcular_similitud(cancion_base, otra_cancion, pesos):
    score = 0
    for categoria in pesos:
        tags_base = set(cancion_base.get(categoria, []))
        tags_otra = set(otra_cancion.get(categoria, []))
        if tags_base and tags_otra:
            interseccion = len(tags_base & tags_otra)
            union = len(tags_base | tags_otra)
            jaccard = interseccion / union
            score += jaccard * pesos[categoria]
    return score

# Ajustar preferencias del usuario
def actualizar_preferencias(user_prefs, cancion, feedback, learning_rate=0.5):
    delta = 1 if feedback == "like" else -1 if feedback == "dislike" else 0
    if delta == 0:
        return user_prefs

    for categoria, tags in cancion.items():
        if categoria in user_prefs:
            for tag in tags:
                actual = user_prefs[categoria].get(tag, 0)
                user_prefs[categoria][tag] = actual + delta * learning_rate
    return user_prefs

# Score combinado: similitud + afinidad
def calcular_score_total(cancion, base, user_prefs, pesos):
    sim_tag = calcular_similitud(base, cancion, pesos)
    afinidad = 0
    for categoria in pesos:
        tags = cancion.get(categoria, [])
        for tag in tags:
            afinidad += user_prefs.get(categoria, {}).get(tag, 0)
    return sim_tag + 0.2 * afinidad

# Sugerencia siguiente canción
def sugerir_siguiente(cancion_actual, canciones, user_prefs, pesos):
    candidatos = [c for c in canciones if c["id"] != cancion_actual["id"]]
    ranked = sorted(candidatos, key=lambda c: calcular_score_total(c, cancion_actual, user_prefs, pesos), reverse=True)
    return ranked[0] if ranked else random.choice(canciones)

# Inicializar perfil vacío por usuario (puede serializarse en el futuro)
def init_user_preferences(tags_estructura):
    return {categoria: {} for categoria in tags_estructura}

if __name__ == "__main__":
    canciones = cargar_canciones()
    estructura_tags = cargar_estructura_tags()
    pesos = {
        "Temas_Espirituales": 0.6,
        "Estado_Emocional": 0.2,
        "Contexto": 0.1,
        "Genero_cancion": 0.1
    }
    user_prefs = init_user_preferences(estructura_tags)

    actual = canciones[0]
    while True:
        print("\nSiguiente sugerencia:", actual["titulo"])
        print("Autor(es):", ", ".join(actual["autor"]))
        accion = input("[l]ike / [d]islike / [s]kip / [q]uit: ").strip().lower()

        if accion == "q":
            break
        if accion in ["l", "d"]:
            feedback = "like" if accion == "l" else "dislike"
            user_prefs = actualizar_preferencias(user_prefs, actual, feedback)
        actual = sugerir_siguiente(actual, canciones, user_prefs, pesos)
