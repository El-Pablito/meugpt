from flask import Flask, request, abort
import hashlib
import hmac
import json
import subprocess
import os

app = Flask(__name__)
port = 5555
secret = "HUEVOS"
repo_path = "/home/pablito/gitHub/meugpt/meu_gpt"
branch = "refs/heads/main"
# systemctl_svc_name = 'webcripto'


@app.route("/github-webhook", methods=["POST"])
def github_webhook():
    try:
        signature = request.headers.get("X-Hub-Signature")
        if not signature:
            abort(403)

        mac = hmac.new(secret.encode("utf-8"), msg=request.data, digestmod=hashlib.sha1)
        if not hmac.compare_digest(f"sha1={mac.hexdigest()}", signature):
            abort(403)

        payload = json.loads(request.data)
        if request.headers.get("X-GitHub-Event") == "push" and payload["ref"] == branch:

            result = subprocess.run(["git", "pull"], cwd=repo_path, capture_output=True)
            print("Saida do git pull:", result.stdout.decode())
            print("Erro do git pull:", result.stderr.decode())

            try:
                with open(os.path.join(repo_path, "webhook_received.txt"), "w") as f:
                    f.write("Webhook recebido com sucesso!")
                print("Arquivo 'webhook_received.txt' criado com sucesso.")
            except Exception as e:
                print(f"Erro ao criar o arquivo: {e}")

#            try:
#                subprocess.run(
#                    [
#                        "ps",
#                        "aux",
#                        "|",
#                        "grep",
#                        "flask",
#                        "|",
#                        "awk",
#                        "'{print $2}'",
#                        "|",
#                        "kill",
#                    ]
#                )
#		app_file = repo_pah + "/app.py"
#                subprocess.run(["python3", "/home/pablito/gitHub/meugpt/meu_gpt/app.py"])
#                print(f"Servico reiniciado com sucesso.")
            except Exception as e:
                print(f"Erro  {e}")

        return "Webhook recebido com sucesso!", 200
    except Exception as e:
        print(f"Erro: {e}")
        abort(500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)
