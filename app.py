from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    """
    Endpoint raíz de bienvenida.

    Retorna:
    str: Mensaje principal de la aplicación documentada.
    """
    return "Aplicación Flask con documentación automatizada mediante Doxygen"

@app.route("/hello")
def hello():
    """
    Endpoint para saludar al usuario.

    Parámetros:
    name (str): Nombre del usuario.

    Retorna:
    str: Mensaje de saludo.
    """
    name = request.args.get("name", "Mundo")
    return f"Hello, {name}!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)