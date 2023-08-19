import pandas as pd
import warnings

def unir_arquivo_excel(caminhos):
    final = pd.DataFrame()

    for caminho in caminhos:
        warnings.filterwarnings('ignore')
        df = pd.read_excel(caminho, index_col = 0)
        
        final = final.append(df)
    
    return final

def unir_arquivo_csv(caminhos):
    final = pd.DataFrame()

    for caminho in caminhos:
        warnings.filterwarnings('ignore')
        df = pd.read_csv(caminho, sep = ";", index_col=None)
        
        final = final.append(df)
    
    return final