from flask import Flask, request, render_template, session
from flask_session import Session
from openai import OpenAI
from redis import Redis
import os

app = Flask(__name__)
app.config["SECRET_KEY"] =os.getenv("SECRET_KEY")
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

cache = Redis(host='localhost', port=6379, db=0)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORGANIZATION")
)

def get_cached_response(message, session_id):
    """
    Busca a resposta no cache ou faz uma chamada à API se não estiver cacheada.
    """
    cache_key = f"chat_response_{session_id}_{message}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response
    else:
        response = client.chat.completions.create(model="gpt-3.5-turbo-1106",
                                                  messages=[{"role": "user", "content": message}])
        response_content = response.choices[0].message.content
        # Armazenando a resposta no cache com um timeout de 1 hora (3600 segundos)
        cache.set(cache_key, response_content, ex=3600)
        return response_content

@app.route("/", methods=["GET", "POST"])
def home():
    session_id = session.get("session_id", None)
    if not session_id:
        # Cria um novo session_id se não existir
        session["session_id"] = os.urandom(24).hex()
        session_id = session["session_id"]
    
    if request.method == "POST":
        user_message = request.form["user_message"]
        if "messages" not in session:
            session["messages"] = []
        session["messages"].append({"role": "user", "content": user_message})

        # Utilizando a função de cache para obter a resposta
        response_content = get_cached_response(user_message, session_id)

        # Atualizando session["messages"] com a resposta cacheada ou da API
        session["messages"].append({"role": "assistant", "content": response_content})
        session.modified = True

    return render_template("chat.html", messages=session.get("messages", []))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001,  debug=True)	
