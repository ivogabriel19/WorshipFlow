import json

# Cargar canciones desde JSON
def cargar_canciones(ruta="data/canciones.json"):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def similitud_jaccard(tags1, tags2):
    inter = tags1 & tags2
    union = tags1 | tags2
    return len(inter) / len(union)

def recomendar_por_tags(tags_referencia, canciones, ya_vistas=None):
    if ya_vistas is None:
        ya_vistas = []
    candidatas = [c for c in canciones if c["id"] not in ya_vistas]
    candidatas = sorted(
        candidatas,
        key=lambda c: similitud_jaccard(set(tags_referencia), set(c["tags"])),
        reverse=True
    )
    return candidatas[0] if candidatas else None
