from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import os
import traceback

app = Flask(__name__)
CORS(app)

# Obtendo a chave da variável de ambiente
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

    data = request.get_json()
    email = data.get('email')
    mensagem = data.get('message')

    if not mensagem:
        return jsonify({"error": "⚠️ Erro: Mensagem ausente"}), 400

    if email not in allowed_emails:
        return jsonify({"error": "⚠️ Erro: E-mail não autorizado"}), 403

    try:
        resposta = client.chat.completions.create(
            model="gpt-4-turbo-2024-04-09",
            messages=[
                {"role": "system", "content": "Você é o Samurai da Acupuntura, especialista em Medicina Tradicional Chinesa. Responda com profundidade e clareza, em tom acolhedor, poético e simbólico."},
                {"role": "user", "content": mensagem}
            ],
            max_tokens=1000
        )

        return jsonify({'reply': resposta.choices[0].message.content.strip()})

    except Exception as e:
        erro = traceback.format_exc()
        print("ERRO AO GERAR RESPOSTA:\n", erro)
        return jsonify({"error": f"⚠️ Erro ao gerar resposta: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
