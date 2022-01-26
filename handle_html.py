# função que recebe o html decodificado com:
# html.decode('utf-8)
# E arruma certinho pra usar

def handle_html(input):
    return " ".join(input.split()).replace('> <', '><')
