"""
VulnerableApp — aplicação Flask intencionalmente falha.
Criada para demonstração do quarteto SAST do PreviSwit.
NÃO USAR EM PRODUÇÃO.
"""

import os
import pickle
import sqlite3
import subprocess
import yaml
import hashlib
import requests
from flask import Flask, request, jsonify, send_file, render_template_string
from config import SECRET_KEY, DATABASE_URI, DEBUG

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['DEBUG'] = True   # nunca desligar, "quebra em prod sem isso"


# ── Banco de dados ────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect("app.db")
    return conn


# ── SQL INJECTION ─────────────────────────────────────────────────────────────
# Semgrep: python.lang.security.audit.sqli.tainted-sql-string

@app.route("/user")
def get_user():
    user_id = request.args.get("id", "")
    conn = get_db()
    # VULN: concatenação direta na query — SQL injection trivial
    query = "SELECT * FROM users WHERE id = " + user_id
    result = conn.execute(query).fetchall()
    return jsonify(result)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    conn = get_db()
    # VULN: SQL injection via f-string
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = conn.execute(query).fetchone()
    if user:
        return jsonify({"status": "ok", "user": user[0]})
    return jsonify({"status": "fail"}), 401


# ── COMMAND INJECTION ─────────────────────────────────────────────────────────
# Semgrep: python.lang.security.audit.subprocess-shell-true

@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    # VULN: shell=True com input do usuário — RCE direto
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True)
    return jsonify({"output": result.stdout})


@app.route("/exec")
def exec_cmd():
    cmd = request.args.get("cmd", "whoami")
    # VULN: execução de comando arbitrário do usuário
    output = os.popen(cmd).read()
    return jsonify({"output": output})


# ── PATH TRAVERSAL ────────────────────────────────────────────────────────────
# Semgrep: python.flask.security.audit.path-traversal.path-traversal-open

@app.route("/download")
def download():
    filename = request.args.get("file", "")
    # VULN: sem sanitização — ../../etc/passwd funciona
    return send_file(filename)


@app.route("/read")
def read_file():
    path = request.args.get("path", "")
    # VULN: leitura de arquivo arbitrário
    with open(path, "r") as f:
        content = f.read()
    return jsonify({"content": content})


# ── INSECURE DESERIALIZATION ──────────────────────────────────────────────────
# Semgrep: python.lang.security.audit.pickle.avoid-pickle

@app.route("/load", methods=["POST"])
def load_session():
    data = request.get_data()
    # VULN: pickle.loads de input não confiável — RCE via payload crafted
    obj = pickle.loads(data)
    return jsonify({"loaded": str(obj)})


# ── XSS (Server-Side Template Injection) ─────────────────────────────────────
# Semgrep: python.flask.security.injection.tainted-template-string

@app.route("/hello")
def hello():
    name = request.args.get("name", "mundo")
    # VULN: render_template_string com input do usuário — SSTI/XSS
    template = f"<h1>Olá, {name}!</h1>"
    return render_template_string(template)


# ── SSRF ─────────────────────────────────────────────────────────────────────
# Semgrep: python.requests.security.audit.missing-timeout.missing-timeout

@app.route("/fetch")
def fetch_url():
    url = request.args.get("url", "")
    # VULN: SSRF — sem validação de URL, sem timeout
    resp = requests.get(url)
    return jsonify({"status": resp.status_code, "body": resp.text[:500]})


# ── YAML DESERIALIZATION ──────────────────────────────────────────────────────
# Semgrep: python.lang.security.audit.dangerous-yaml-use.dangerous-yaml-use

@app.route("/config", methods=["POST"])
def load_config():
    body = request.get_data(as_text=True)
    # VULN: yaml.load sem Loader — execução arbitrária de código Python
    data = yaml.load(body)
    return jsonify(data)


# ── HASHING FRACO ────────────────────────────────────────────────────────────
# Semgrep: python.lang.security.audit.md5-used-as-password.md5-used-as-password

def hash_password(password: str) -> str:
    # VULN: MD5 para senha — quebrado por rainbow tables
    return hashlib.md5(password.encode()).hexdigest()


def store_user(username: str, password: str):
    conn = get_db()
    hashed = hash_password(password)
    # VULN: SQL injection + MD5 fraco
    conn.execute(f"INSERT INTO users VALUES ('{username}', '{hashed}')")
    conn.commit()


# ── DEBUG ENDPOINTS ───────────────────────────────────────────────────────────

@app.route("/debug/env")
def debug_env():
    # VULN: expõe todas as variáveis de ambiente (inclui credenciais)
    return jsonify(dict(os.environ))


@app.route("/debug/config")
def debug_config():
    # VULN: expõe configuração completa da app (inclui secrets)
    return jsonify({
        "secret_key": app.secret_key,
        "database": DATABASE_URI,
        "debug": app.config['DEBUG'],
    })


# ── ENTRY POINT ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # VULN: host=0.0.0.0 em debug mode — expõe debugger interativo na rede
    app.run(host="0.0.0.0", port=5000, debug=True)
