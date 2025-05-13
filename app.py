import os
import ocrmypdf
import multiprocessing

# 🔧 DEFINA AQUI OS CAMINHOS DAS PASTAS
PASTA_ENTRADA = r"C:\Users\Digital\Desktop\NF1001\202201"
PASTA_SAIDA   = r"C:\Users\Digital\Desktop\NF1001\202201ocr"

# Função para processar cada arquivo individualmente
def processar_ocr(caminho_entrada, caminho_saida):
    try:
        ocrmypdf.ocr(
            caminho_entrada,
            caminho_saida,
            lang='por',
            deskew=True,
            force_ocr=True,
            jobs=4,               # Cada instância usa 1 núcleo (cada processo será um núcleo)
            progress_bar=True
        )
        print(f"✅ Salvo: {os.path.basename(caminho_saida)}")
    except Exception as e:
        print(f"❌ Erro ao processar {os.path.basename(caminho_entrada)}: {e}")

def processar_arquivos_ocr(pasta_entrada, pasta_saida):
    os.makedirs(pasta_saida, exist_ok=True)

    arquivos = [f for f in os.listdir(pasta_entrada) if os.path.isfile(os.path.join(pasta_entrada, f))]

    # Detecta automaticamente o número de núcleos
    num_processadores = multiprocessing.cpu_count()
    print(f"🚀 Usando {num_processadores} processadores para OCR.")

    # Cria um pool de processos para paralelizar
    with multiprocessing.Pool(processes=num_processadores) as pool:
        for nome_arquivo in arquivos:
            caminho_entrada = os.path.join(pasta_entrada, nome_arquivo)
            nome, ext = os.path.splitext(nome_arquivo)
            ext = ext.lower()

            if ext in ['.pdf', '.jpg', '.jpeg', '.png', '.tif', '.tiff']:
                caminho_saida = os.path.join(pasta_saida, f"{nome}_ocr.pdf")
                pool.apply_async(processar_ocr, (caminho_entrada, caminho_saida))
            else:
                print(f"⚠️ Formato não suportado: {nome_arquivo}")

        # Espera que todos os processos finalizem
        pool.close()
        pool.join()

if __name__ == "__main__":
    print("📝 Iniciando OCR nos arquivos da pasta...")
    processar_arquivos_ocr(PASTA_ENTRADA, PASTA_SAIDA)
    print("✅ OCR finalizado.")
    input("\nPressione Enter para sair...")  # Mantém o console aberto
