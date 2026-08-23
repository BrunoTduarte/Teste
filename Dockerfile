FROM python:3.9

WORKDIR /app

# Checkov: CKV_DOCKER_2 — sem HEALTHCHECK
# Checkov: CKV_DOCKER_3 — sem instrução USER (roda como root)
# Checkov: CKV_DOCKER_7 — FROM sem tag fixa (usa latest implícito de 3.9)

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Checkov: CKV_DOCKER_4 — secrets em variável de ambiente no Dockerfile
ENV SECRET_KEY="my-super-secret-key-do-not-share"
ENV DATABASE_URI="postgresql://admin:Senha123!@db.prod.internal:5432/appdb"
ENV AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
ENV AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# Sem USER — container roda como root
EXPOSE 5000

CMD ["python", "app.py"]
