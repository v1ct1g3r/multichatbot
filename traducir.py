from deep_translator import GoogleTranslator


def en2es(string):
    return GoogleTranslator(source="en", target="es").translate(string)


def es2en(string):
    return GoogleTranslator(source="es", target="en").translate(string)