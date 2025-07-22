'''Programa recebe local com pastas de arquivos zipados e descompacta mantenho estrutura de pastas
indicar caminho no final do programa conforme instrução
Programa ignora, mas mantem os arquivos corrompidos na estrutura.
Inserido uma range maior de formatos de arquivos compactados'''

import os
import zipfile
import tarfile
import rarfile  # Certifique-se de instalar a biblioteca com: pip install rarfile
import py7zr    # Certifique-se de instalar a biblioteca com: pip install py7zr
import time

def extract_files(source_dir, destination_dir):
    # Itera por todos os arquivos no diretório de origem
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(root, source_dir)
            extract_path = os.path.join(destination_dir, relative_path, file.rsplit('.', 1)[0])  # Remove a extensão do nome da pasta

            # Verifica o tipo de arquivo e tenta descompactar
            try:
                if file.endswith('.zip'):
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_path)
                        print(f"Extraído {file_path} para {extract_path}")
                elif file.endswith('.rar'):
                    with rarfile.RarFile(file_path, 'r') as rar_ref:
                        rar_ref.extractall(extract_path)
                        print(f"Extraído {file_path} para {extract_path}")
                elif file.endswith(('.tar.gz', '.tar.bz2', '.tar.Z', '.tgz', '.gz', '.bz2')):
                    with tarfile.open(file_path, 'r:*') as tar_ref:
                        tar_ref.extractall(extract_path)
                        print(f"Extraído {file_path} para {extract_path}")
                elif file.endswith('.7z'):
                    with py7zr.SevenZipFile(file_path, mode='r') as sevenzip_ref:
                        sevenzip_ref.extractall(extract_path)
                        print(f"Extraído {file_path} para {extract_path}")
                else:
                    print(f"Tipo de arquivo não suportado: {file_path}")

            except (zipfile.BadZipFile, rarfile.Error, tarfile.TarError, py7zr.Bad7zFile) as e:
                # Ignora arquivos corrompidos e mantém na estrutura
                print(f"Arquivo corrompido ignorado: {file_path} | Erro: {e}")

# armazena data do sistema para contabilizar o tempo de execução do programa
tic = time.perf_counter()

# Coloque o caminho da origem e do destino
source_directory = r'C:\Users\jcmorais\Desktop\39067\4-Automacao\Projeto_Davi\001_zip'

# Coloque o caminho da destino dos arquivos descompactados
destination_directory = r'F:\transfer\julio'

extract_files(source_directory, destination_directory)

# Calcula e exibe tempo de execução
toc = time.perf_counter()
tictoc = (toc - tic) / 60
minutos = int(tictoc)
segundos = (tictoc - minutos) * 60
print(f"Tempo de execução: {toc - tic:0.3f} segundos.")
print(f"Tempo: {minutos} minutos e {segundos:0.2f} segundos. ")