import os
import sys
import time
import requests

def check_hibp(email, max_retries=3):
    api_key = os.getenv("HIBP_API_KEY")
    if not api_key:
        print("Erro: variável de ambiente HIBP_API_KEY não configurada.")
        return False

    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        "hibp-api-key": api_key,
        "user-agent": "leak-checker"
    }

    retries = 0
    wait_time = 1  # segundos, inicial

    while retries <= max_retries:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                return False
            elif response.status_code == 429:
                print(f"Recebido 429 - limite atingido. Tentando novamente em {wait_time} segundos...")
                time.sleep(wait_time)
                retries += 1
                wait_time *= 2  # espera exponencial
            else:
                print(f"HIBP erro: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Erro ao consultar HIBP: {e}")
            return False

    print("Número máximo de tentativas atingido. Não foi possível consultar HIBP.")
    return False

def check_mozilla_monitor(email):
    print("Mozilla Monitor utiliza Have I Been Pwned API - verificando via HIBP...")
    return check_hibp(email)

def check_cybernews(email):
    print("Consulta Cybernews não implementada - API privada ou paga")
    return None

def check_f_secure(email):
    print("Consulta F-Secure não implementada - API privada ou paga")
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python gs.py email")
        sys.exit(1)

    email = sys.argv[1]

    print(f"Verificando vazamentos para o email: {email}\n")

    hibp = check_hibp(email)
    print(f"Have I Been Pwned: {'Vazado!' if hibp else 'Não encontrado.'}")

    mozilla = check_mozilla_monitor(email)
    print(f"Mozilla Monitor: {'Vazado!' if mozilla else 'Não encontrado.'}")

    cybernews = check_cybernews(email)
    print(f"Cybernews: {'Vazado!' if cybernews else 'Não disponível.'}")

    fsecure = check_f_secure(email)
    print(f"F-Secure: {'Vazado!' if fsecure else 'Não disponível.'}")
