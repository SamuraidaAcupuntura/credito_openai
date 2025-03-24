from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key='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')

allowed_emails = [
    'paulocosta@samuraidaacupuntura.com.br', 
    'alceuacosta@gmail.com', 
    'andreiabioterapia@hotmail.com'
]

@app.route('/chat', methods=['POST'])
def chat():
    email = request.json.get('email')
    mensagem = request.json.get('message')

    if email not in allowed_emails:
        return jsonify({"error": "E-mail não autorizado."}), 403

    # Chamada direta rápida para GPT-4 (sem threads lentas):
    resposta = client.chat.completions.create(
        model='gpt-4-turbo',
        messages=[
            {"role": "system", "content": "Você é o Samurai da Acupuntura, especialista em Medicina Tradicional Chinesa."},
            {"role": "user", "content": mensagem}
        ],
        max_tokens=500
    )

    return jsonify({'reply': resposta.choices[0].message.content.strip()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
