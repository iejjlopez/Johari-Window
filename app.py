from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import pandas as pd

app = Flask(__name__)

# Cargar el modelo de NLP
sentiment_analyzer = pipeline("sentiment-analysis")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    responses = [
        request.form["open_area"],
        request.form["hidden_area"],
        request.form["blind_area"],
        request.form["unknown_area"]
    pass
    ]
    suggestions = []
    for response in responses:
        result = sentiment_analyzer(response)[0]
        if result['label'] == 'NEGATIVE':
            suggestions.append("Considera trabajar en esta área para mejorar tu autoconciencia.")
        else:
            suggestions.append("¡Buen trabajo! Sigue fortaleciendo esta área.")
    data = {
        'Área Abierta': [responses[0]],
        'Área Oculta': [responses[1]],
        'Área Ciega': [responses[2]],
        'Área Desconocida': [responses[3]],
        'Sugerencias': [", ".join(suggestions)]
    }
    df = pd.DataFrame(data)
    df.to_csv("results.csv", index=False)
    return jsonify(suggestions)

if __name__ == "__main__":
    app.run(debug=True)
