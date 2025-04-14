from db import conectar

def buscar_medicamento(nome_medicamento: str):
    conn = conectar()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        query = """
            SELECT nome, preco, fabricante, dosagem, tarja_id
            FROM remedios
            WHERE LOWER(nome) LIKE %s
            LIMIT 1
        """
        cursor.execute(query, (f"%{nome_medicamento.lower().strip()}%",))
        resultado = cursor.fetchone()
        return resultado
    except Exception as e:
        print(f"[Erro DB] Falha na consulta: {e}")
        return None
    finally:
        conn.close()
