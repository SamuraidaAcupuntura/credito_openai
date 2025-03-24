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

    if email not in allowed_emails:
        return jsonify({"error": "E-mail não autorizado."}), 403

    try:
        resposta = client.chat.completions.create(
            model='gpt-4-turbo',
            messages=[
                {"role": "system", "content": "Você é o Samurai da Acupuntura, especialista em Medicina Tradicional Chinesa."},
                {"role": "user", "content": mensagem}
            ],
            max_tokens=500
        )
        return jsonify({'reply': resposta.choices[0].message.content.strip()})

    except Exception as e:
        return jsonify({"error": f"Erro ao gerar resposta: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
