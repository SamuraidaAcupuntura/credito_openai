from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key='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')

@app.route('/chat', methods=['POST'])
def chat():
    email = request.json.get('email')
    mensagem = request.json.get('message')

    allowed_emails = ['aluno1@gmail.com', 'aluno2@gmail.com']

    if email not in allowed_emails:
        return jsonify({"error": "E-mail não autorizado."}), 403

    thread = client.beta.threads.create()

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role='user',
        content=mensagem
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id='asst_JuGSeUFtvvkiSCfav4LNQUqw'
    )

    while run.status not in ['completed', 'failed']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    resposta = messages.data[0].content[0].text.value

    return jsonify({'reply': resposta})

if __name__ == '__main__':
    app.run(debug=True)
