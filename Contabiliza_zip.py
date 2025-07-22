'''Contabiliza a quantidade de arquivos dentro da pasta zipada
leva algumas condições para se referenciar quanto aos arquivos
cria um arquivo .xls na mesma pasta onde esta o arquivo zipado'''

import os
import pandas as pd
import zipfile
import re
import tempfile
import shutil
from pyunpack import Archive
import patoolib

def extract_archive(archive_path, extract_to):
    try:
        Archive(archive_path).extractall(extract_to)
        return True
    except Exception as e:
        print(f"Erro ao extrair {archive_path}: {e}")
        return False

def count_files_in_directory(directory):
    pattern = re.compile(r'^\d{3}-\d{5}-\d{3}')
    matching_count = 0
    non_matching_count = 0
    specific_names = []

    for root, _, files in os.walk(directory):
        for file in files:
            if pattern.match(file):
                matching_count += 1
            else:
                non_matching_count += 1

            full_path = os.path.join(root, file)
            if (
                '#1#' in full_path and
                '#00#000#' in full_path and
                full_path.find('#1#') < full_path.find('#00#000#') and
                full_path.endswith('.CATProduct')
            ):
                specific_names.append(file)

    return matching_count + non_matching_count, matching_count, non_matching_count, len(specific_names), '; '.join(specific_names)

def process_archive(archive_path):
    ext = os.path.splitext(archive_path)[1].lower()
    if ext == '.zip':
        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                with tempfile.TemporaryDirectory() as temp_dir:
                    zip_ref.extractall(temp_dir)
                    return count_files_in_directory(temp_dir)
        except Exception as e:
            print(f"Erro ao ler ZIP: {e}")
            return 'Erro', 'Erro', 'Erro', 'Erro', 'Erro'
    elif ext in ['.rar', '.7z']:
        with tempfile.TemporaryDirectory() as temp_dir:
            if extract_archive(archive_path, temp_dir):
                return count_files_in_directory(temp_dir)
            else:
                return 'Erro', 'Erro', 'Erro', 'Erro', 'Erro'
    else:
        return 'Erro', 'Erro', 'Erro', 'Erro', 'Erro'

def generate_file_list(base_directory):
    cd_number = input("Digite o número do CD: ").strip()
    output_directory = os.path.join(base_directory, cd_number)
    os.makedirs(output_directory, exist_ok=True)

    archive_files = []
    file_counts = []
    matching_counts = []
    non_matching_counts = []
    specific_string_counts = []
    specific_file_names = []

    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith(('.zip', '.rar', '.7z')):
                archive_path = os.path.join(root, file)
                if output_directory in archive_path:
                    continue
                archive_files.append(os.path.relpath(archive_path, base_directory))
                total, match, non_match, specific_count, names_str = process_archive(archive_path)
                file_counts.append(total)
                matching_counts.append(match)
                non_matching_counts.append(non_match)
                specific_string_counts.append(specific_count)
                specific_file_names.append(names_str)

    df = pd.DataFrame({
        'Nome Arquivo': archive_files,
        'Total de Arquivos': file_counts,
        'Total Padrão (PN)': matching_counts,
        'Total eLibrary': non_matching_counts,
        'Total file CONJ_GERAL': specific_string_counts,
        'Nome completo CONJ_GERAL': specific_file_names
    })

    output_file = os.path.join(output_directory, 'lista_de_arquivos.xlsx')
    df.to_excel(output_file, index=False)
    print(f"Arquivo 'lista_de_arquivos.xlsx' criado com sucesso em {output_directory}")

# Exemplo de uso:
# Caminho da pasta onde encontram-se as pastas zipadas
generate_file_list(r"C:\Users\jcmorais\Desktop\39067\4-Automacao\Projeto_Davi\001_zip")
