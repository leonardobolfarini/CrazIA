import time
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# URL do banco (pode vir de uma variável de ambiente depois se quiser)
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
print("URL do banco:", DATABASE_URL) 
def testar_conexao():
    try:
        inicio = time.time()

        # Conectar ao banco
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cursor = conn.cursor()

        tempo_conexao = time.time() - inicio
        print(f"✅ Conexão bem-sucedida em {tempo_conexao:.2f} segundos.\n")

        # Buscar dados da tabela
        cursor.execute("SELECT * FROM remedios")
        resultados = cursor.fetchall()

        print(f"📦 {len(resultados)} resultados encontrados:\n")

        for remedio in resultados:
            print(f"🧪 ID: {remedio['id']}")
            print(f"📛 Nome: {remedio['nome']}")
            print(f"🏭 Fabricante: {remedio['fabricante']}")
            print(f"💊 Dosagem: {remedio['dosagem']}")
            print(f"💰 Preço: R${remedio['preco']}")
            print(f"📅 Criado em: {remedio['criado_em']}")
            print(f"⚠️ Tarja ID: {remedio['tarja_id']}")
            print("-" * 40)

    except Exception as e:
        print(f"❌ Erro ao conectar ou buscar dados: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("\n🔒 Conexão encerrada.")

if __name__ == "__main__":
    testar_conexao()
