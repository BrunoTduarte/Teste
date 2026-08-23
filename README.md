# VulnerableApp — Demo PreviSwit

Aplicação Flask intencionalmente falha para demonstração do quarteto SAST do PreviSwit.

## Vulnerabilidades inclusas

### Semgrep (análise de código)
- SQL Injection via concatenação e f-string (`/user`, `/login`)
- Command Injection via `shell=True` (`/ping`, `/exec`)
- Path Traversal sem sanitização (`/download`, `/read`)
- Insecure Deserialization via `pickle.loads` (`/load`)
- SSTI/XSS via `render_template_string` com input do usuário (`/hello`)
- SSRF sem validação de URL (`/fetch`)
- YAML deserialization insegura via `yaml.load` sem Loader (`/config`)
- Hash fraco MD5 para senhas (`hash_password`)
- Debug endpoints expondo secrets (`/debug/env`, `/debug/config`)

### Gitleaks (segredos)
- AWS Access Key ID e Secret
- GitHub Personal Access Token
- Stripe Secret Key
- SendGrid API Key
- Chaves hardcoded de Flask, JWT e Redis

### Trivy (dependências com CVE)
- Flask 0.12.3 — CVE-2018-1000656 (DoS)
- requests 2.18.4 — CVE-2018-18074 (credential exposure)
- Pillow 8.0.0 — CVE-2021-27921, CVE-2021-25287 (heap overflow)
- PyYAML 5.1 — CVE-2019-20477 (code execution)
- Jinja2 2.10.1 — CVE-2019-10906, CVE-2019-8341
- cryptography 2.6.1 — múltiplos CVEs
- paramiko 2.4.1 — CVE-2018-1000805 (authentication bypass)

### Checkov (IaC)
- Dockerfile sem HEALTHCHECK (CKV_DOCKER_2)
- Container rodando como root (CKV_DOCKER_3)
- Secrets em ENV do Dockerfile (CKV_DOCKER_4)
- Porta do banco exposta diretamente no compose (CKV_DOCKER_8)
- Sem separação de volumes de dados

## USO

Esta aplicação é estritamente para fins de demonstração. Não executar em ambiente de produção.
