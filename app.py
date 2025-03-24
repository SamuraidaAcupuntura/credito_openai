from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

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
