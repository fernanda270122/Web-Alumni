def calcular_match(palabras_cv, oferta):
    palabras_oferta = [
        oferta.palabra1,
        oferta.palabra2,
        oferta.palabra3,
        oferta.palabra4,
        oferta.palabra5
    ]

    palabras_oferta = [p.lower() for p in palabras_oferta if p]

    if not palabras_oferta or not palabras_cv:
        return 0

    coincidencias = 0

    for palabra in palabras_oferta:
        if palabra in palabras_cv:
            coincidencias += 1

    score = int((coincidencias / len(palabras_oferta)) * 100)

    return score


def obtener_palabras_cv(usuario):
    from .models import CVUsuario

    try:
        cv = CVUsuario.objects.get(usuario=usuario)

        palabras = [
            cv.palabra1, cv.palabra2, cv.palabra3, cv.palabra4, cv.palabra5,
            cv.palabra6, cv.palabra7, cv.palabra8, cv.palabra9, cv.palabra10
        ]

        return [p.lower() for p in palabras if p]

    except CVUsuario.DoesNotExist:
        return []

def obtener_matches_usuario(usuario):
    from .models import Oferta

    palabras_cv = obtener_palabras_cv(usuario)

    ofertas = Oferta.objects.filter(activa=True)

    resultados = []

    for oferta in ofertas:
        score = calcular_match(palabras_cv, oferta)

        if score > 0:
            resultados.append({
                "oferta": oferta,
                "score": score
            })

    resultados.sort(key=lambda x: x["score"], reverse=True)

    return resultados