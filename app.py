from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Inicializa o cliente OpenAI com a API key do ambiente
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("⚠️ OPENAI_API_KEY não está definida no ambiente.")
client = OpenAI(api_key=api_key)

# Lista de e-mails autorizados
allowed_emails = [
    "paulocosta@samuraidaacupuntura.com.br",
    "alceuacosta@gmail.com",
    "andreiabioterapia@hotmail.com"
]

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        email = data.get("email")
        message = data.get("message")
        image_base64 = data.get("image")  # opcional

        if not email or email not in allowed_emails:
            return jsonify({"error": "E-mail não autorizado."}), 403

        if not message and not image_base64:
            return jsonify({"error": "Mensagem ausente."}), 400

        messages = [
            {
                "role": "system",
                "content": "Você é o Samurai da Acupuntura, especialista em Medicina Tradicional Chinesa, espiritualidade e sabedoria oriental. Responda de forma poética, profunda e acolhedora, mas com base sólida."
            }
        ]

        if image_base64:
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": message or "Analise esta imagem."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            })
            model = "gpt-4-vision-preview"
        else:
            messages.append({
                "role": "user",
                "content": message
            })
            model = "gpt-4"

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1000
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": f"Erro ao gerar resposta: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
