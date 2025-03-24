from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

try:
    api_key = os.environ['OPENAI_API_KEY']
    client = OpenAI(api_key=api_key)
except Exception as e:
    api_key = None
    erro_api = str(e)

allowed_emails = [
    'paulocosta@samuraidaacupuntura.com.br',
    'alceuacosta@gmail.com',
    'andreiabioterapia@hotmail.com'
]

@app.route('/chat', methods=['POST'])
def chat():
    if api_key is None:
        return jsonify({"error": f"Erro na API Key: {erro_api}"}), 500

    email = request.json.get('email')
    mensagem = request.json.get('message')
    imagem_base64 = request.json.get('image')  # opcional

    if email not in allowed_emails:
        return jsonify({"error": "E-mail não autorizado."}), 403

    try:
        if imagem_base64:
            messages = [
                {
                    "role": "system",
                    "content": "Você é o Samurai da Acupuntura, especialista em Medicina Tradicional Chinesa. Analise a imagem e responda com base nos ensinamentos da Jornada do Samurai."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": mensagem},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{imagem_base64}"
                            }
                        }
                    ]
                }
            ]
            resposta = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=messages,
                max_tokens=800
            )
        else:
            resposta = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "Você é o Samurai da Acupuntura, especialista em Medicina Tradicional Chinesa."},
                    {"role": "user", "content": mensagem}
                ],
                max_tokens=800
            )

        return jsonify({'reply': resposta.choices[0].message.content.strip()})

    except Exception as e:
        return jsonify({"error": f"Erro ao gerar resposta: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
