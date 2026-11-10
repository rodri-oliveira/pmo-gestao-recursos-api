"""Verifica a conexão com um PostgreSQL de desenvolvimento usando variáveis de ambiente."""

import os
import psycopg2

REQUIRED = ("DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME")


def main():
    missing = [key for key in REQUIRED if not os.getenv(key)]
    if missing:
        print("Configuração incompleta: " + ", ".join(missing))
        return 1

    try:
        with psycopg2.connect(
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            connect_timeout=5,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                if cursor.fetchone() == (1,):
                    print("Conexão de teste bem-sucedida.")
                    return 0
    except (psycopg2.Error, ValueError):
        print("Não foi possível validar a conexão. Confira a configuração do ambiente.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
