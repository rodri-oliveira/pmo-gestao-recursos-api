"""Diagnóstico de conexão com um banco PostgreSQL próprio.

Configure DB_USER, DB_PASSWORD, DB_HOST, DB_PORT e DB_NAME no ambiente.
O script não imprime credenciais nem a string de conexão.
"""
import asyncio
import os
import asyncpg

VARS = ("DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME")


async def test_connection():
    missing = [name for name in VARS if not os.getenv(name)]
    if missing:
        print("Variáveis ausentes: " + ", ".join(missing))
        return

    connection = None
    try:
        connection = await asyncpg.connect(
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            host=os.environ["DB_HOST"],
            port=int(os.environ["DB_PORT"]),
            database=os.environ["DB_NAME"],
            timeout=5,
        )
        await connection.execute("SELECT 1")
        print("Conexão de teste bem-sucedida.")
    except (Exception) as error:
        print(f"Falha na conexão ({type(error).__name__}). Verifique as configurações.")
    finally:
        if connection is not None:
            await connection.close()


if __name__ == "__main__":
    asyncio.run(test_connection())
