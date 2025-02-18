from flask import Flask, render_template, request, jsonify
import pandas as pd
from transformers import pipeline

app = Flask(__name__)

# Cargar el modelo de NLP
sentiment_analyzer = pipeline("sentiment-analysis")

# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")

# Ruta para procesar el cuestionario
@app.route("/submit", methods=["POST"])
def submit():
    # Obtener respuestas del formulario
    responses = [
        request.form["open_area"],
        request.form["hidden_area"],
        request.form["blind_area"],
        request.form["unknown_area"]
    ]

    # Analizar respuestas con NLP
    suggestions = []
    for response in responses:
        result = sentiment_analyzer(response)[0]
        if result['label'] == 'NEGATIVE':
            suggestions.append("Considera trabajar en esta área para mejorar tu autoconciencia.")
        else:
            suggestions.append("¡Buen trabajo! Sigue fortaleciendo esta área.")

    # Guardar resultados en un CSV
    data = {
        'Área Abierta': [responses[0]],
        'Área Oculta': [responses[1]],
        'Área Ciega': [responses[2]],
        'Área Desconocida': [responses[3]],
        'Sugerencias': [", ".join(suggestions)]
    }
    df = pd.DataFrame(data)
    df.to_csv("results.csv", index=False)

    # Devolver sugerencias al usuario
    return jsonify(suggestions)

if __name__ == "__main__":
    app.run(debug=True)
