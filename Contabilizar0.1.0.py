import os
import pandas as pd
import re

# Função para contar arquivos e aplicar condições
def count_files_and_conditions(root_dir, pattern):
    data = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if filenames:
            folder_name = os.path.basename(dirpath)
            file_count = len(filenames)
            
            # Contagem por regex
            regex_match_count = sum(1 for filename in filenames if pattern.match(filename))
            non_regex_match_count = file_count - regex_match_count
            
            # Condição personalizada
            condition_match_filenames = [
                filename for filename in filenames
                if '#1#' in filename and '#00#000#' in filename and
                filename.index('#1#') < filename.index('#00#000#') and
                filename.endswith('.CATProduct')
            ]
            condition_match_count = len(condition_match_filenames)
            
            data.append([
                folder_name,
                file_count,
                regex_match_count,
                non_regex_match_count,
                condition_match_count,
                ', '.join(condition_match_filenames)
            ])
    
    return data

# Caminho raiz (altere conforme necessário)
root_directory = r'C:\\Users\\jcmorais\\Desktop\\39067\\4-Automacao\\Projeto_Davi\\001_zip\\resultado'

# Regex para nomes de arquivos
pattern = re.compile(r'^\d{3}-\d{5}-\d{3}')

# Coleta os dados
data = count_files_and_conditions(root_directory, pattern)

# Cria o DataFrame
df = pd.DataFrame(data, columns=[
    'Nome da Pasta',
    'Total Arquivos',
    'Total com PN',
    'total de eLibrary',
    'Total CONJ GERAL',
    'Nome CONJ GERAL'
])

# Defina o caminho completo do arquivo de saída (altere conforme necessário)
output_file = r'C:\\Users\\jcmorais\\Desktop\\39067\\4-Automacao\\Projeto_Davi\\001_zip\\resultado\\file_counts.xlsx'

# Salva o Excel
df.to_excel(output_file, index=False)

print(f"O arquivo {output_file} foi criado com sucesso.")
