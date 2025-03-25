from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Inicializar cliente OpenAI
try:
    api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception as e:
    api_key = None
    erro_api = str(e)

# Lista de e-mails autorizados
allowed_emails = [
    "paulocosta@samuraidaacupuntura.com.br",
    "alceuacosta@gmail.com",
    "andreiabioterapia@hotmail.com"
]

@app.route("/chat", methods=["POST"])
def chat():
    if api_key is None:
        return jsonify({"error": f"Erro na API Key: {erro_api}"}), 500

    data = request.get_json()
    email = data.get("email", "").strip()
    mensagem = data.get("message", "").strip()
    imagem_base64 = data.get("image", None)

    if email not in allowed_emails:
        return jsonify({"error": "❌ E-mail não autorizado."}), 403

    if not mensagem and not imagem_base64:
        return jsonify({"error": "⚠️ Mensagem ausente."}), 400

    try:
        # Caso tenha imagem, usar o GPT-4 com vision
        if imagem_base64:
            content = []
            if mensagem:
                content.append({"type": "text", "text": mensagem})
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{imagem_base64}"
                }
            })

            resposta = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {"role": "system", "content": "Você é o Samurai da Acupuntura, especialista em Medicina Tradicional Chinesa."},
                    {"role": "user", "content": content}
                ],
                max_tokens=1000
            )
        else:
            # Apenas texto
            resposta = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "Você é o Samurai da Acupuntura, especialista em Medicina Tradicional Chinesa."},
                    {"role": "user", "content": mensagem}
                ],
                max_tokens=1000
            )

        return jsonify({"reply": resposta.choices[0].message.content.strip()})

    except Exception as e:
        return jsonify({"error": f"❌ Erro ao gerar resposta: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
