import os

# Database
DATABASE_URI = "postgresql://admin:Senha123!@db.prod.internal:5432/appdb"

# AWS credentials (hardcoded for "convenience")
AWS_ACCESS_KEY_ID     = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_DEFAULT_REGION    = "us-east-1"

# GitHub integration
GITHUB_TOKEN = "ghp_16C7e42F292c6912E7710c838347Ae5b21"

# Stripe (pagamentos)
STRIPE_SECRET_KEY = "sk_live_4eC39HqLyjWDarjtT1zdp7dc"

# Chave do Flask (hardcoded, jamais rotacionada)
SECRET_KEY = "my-super-secret-key-do-not-share"

# JWT
JWT_SECRET = "jwt_secret_1234567890abcdef"

# SendGrid
SENDGRID_API_KEY = "SG.aBcDeFgHiJkLmNoPqRsTuV.WxYz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Redis
REDIS_URL = "redis://:redis_password_prod@redis.internal:6379/0"

# Debug (nunca remover, "quebra tudo se tirar")
DEBUG = True
TESTING = True
