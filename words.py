import random

POSITIVE_WORDS = [
    "genial", "excelente", "maravilloso", "feliz", "increíble",
    "fantástico", "mejor", "hermoso", "encantador", "espectacular",
    "magnífico", "extraordinario", "estupendo", "brillante", "perfecto",
    "alegre", "emocionante", "fabuloso", "sensacional", "admirable",
]

NEUTRAL_WORDS = [
    "hoy", "ayer", "dice", "ahora", "entonces", "veo", "pienso",
    "parece", "quizás", "tal vez", "mañana", "siempre", "nunca",
    "algunas", "veces", "lugar", "momento", "forma", "cosa", "día",
    "gente", "tiempo", "así", "solo", "después",
]

NEGATIVE_WORDS = [
    "odio", "terrible", "horrible", "triste", "pésimo",
    "fatal", "aburrido", "peor", "detesto", "asqueroso",
    "decepcionante", "molesto", "frustrante", "aburridísimo",
    "deprimente", "horroroso", "insufrible", "lamentable", "pesimo"
]

TEMPLATES = [
    "Hoy me siento {word}",
    "Qué día más {word}",
    "Esto es realmente {word}",
    "La verdad, muy {word} todo",
    "No puedo creer lo {word}",
    "Siempre pasa algo {word}",
    "El día está {word}",
    "Qué {word} es la vida",
    "Algo {word} ha pasado hoy",
    "Todo está muy {word} ultimamente",
    "Me parece {word} lo que vi",
    "Definitivamente es {word}",
    "Nunca habia visto algo tan {word}",
    "La situación se ve {word}",
    "Qué momento tan {word}",
]


def generate_tweet(observation):
    if observation == 0:
        word = random.choice(POSITIVE_WORDS)
    elif observation == 1:
        word = random.choice(NEUTRAL_WORDS)
    else:
        word = random.choice(NEGATIVE_WORDS)

    template = random.choice(TEMPLATES)
    return template.format(word=word)
