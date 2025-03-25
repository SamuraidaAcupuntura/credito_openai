from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Tenta pegar a chave da variável de ambiente
try:
    api_key = os.environ['OPENAI_API_KEY']
    client = OpenAI(api_key=api_key)
except Exception as e:
    api_key = None
    erro_api = str(e)

# Lista de e-mails permitidos
allowed_emails = [
    'paulocosta@samuraidaacupuntura.com.br',
    'alceuacosta@gmail.com',
    'andreiabioterapia@hotmail.com'
]

@app.route('/chat', methods=['POST'])
def chat():
    if api_key is None:
        return jsonify({"error": f"Erro na API Key: {erro_api}"}), 500

    data = request.json
    email = data.get('email')
    mensagem = data.get('message', '').strip()

    if email not in allowed_emails:
        return jsonify({"error": "E-mail não autorizado."}), 403

    if not mensagem:
        return jsonify({"error": "Mensagem ausente"}), 400

    try:
        resposta = client.chat.completions.create(
            model="gpt-4-turbo-2024-04-09",
            messages=[
                {"role": "system", "content": "Você é o Samurai da Acupuntura, mestre em Medicina Tradicional Chinesa. Responda com sabedoria, calma e profundidade."},
                {"role": "user", "content": mensagem}
            ],
            max_tokens=800,
            temperature=0.7
        )
        return jsonify({'reply': resposta.choices[0].message.content.strip()})
    
    except Exception as e:
        return jsonify({"error": f"Erro ao gerar resposta: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
