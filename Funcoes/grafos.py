from datetime import datetime
import pandas as pd
import networkx as nx
import PIL

def relacionamentos(comentarios, issues, limite_inferior, limite_superior):
    lista_relacionamentos = dict()

    for issue in issues.values:
        if datetime.strptime(issue[3], "%d/%m/%Y") < limite_inferior or datetime.strptime(issue[3], "%d/%m/%Y") >= limite_superior:
            pass
        
        else:
            participantes = [issue[5]]

            for comentario in comentarios[comentarios.ID_ISSUE == issue[1]].values:

                for usuario_anterior in participantes:
                    if comentario[1] > usuario_anterior: 
                        key = "{}/{}".format(comentario[1], usuario_anterior)
                    
                    elif comentario[1] < usuario_anterior: 
                        key = "{}/{}".format(usuario_anterior, comentario[1])
                    
                    else: 
                        key = None

                    is_pull, is_issue = (1, 0) if issue[6] == 'Verdadeiro' else (0, 1)

                    if key in lista_relacionamentos.keys():
                        lista_relacionamentos[key] = [
                            lista_relacionamentos[key][0] + 1,
                            lista_relacionamentos[key][1] + is_issue,
                            lista_relacionamentos[key][2] + is_pull,
                        ]

                    elif key is not None:
                        lista_relacionamentos[key] = [1, is_issue, is_pull]
                    
                participantes.append(comentario[1])
    
    return lista_relacionamentos


def rede_social(relacionamentos, imagem):
    relacoes = list()
    desenvolvedores = []

    for linha in relacionamentos.items():
        autorA, autorB = linha[0].split("/")

        if autorA not in desenvolvedores: 
            desenvolvedores.append(autorA) 

        if autorB not in desenvolvedores: 
            desenvolvedores.append(autorB)

        relacoes.append({'Source': autorA, 'Target': autorB, 'Strength': linha[1][0]})

    
    Grafo = nx.Graph()
    for dev in desenvolvedores:
        Grafo.add_node(dev, image = imagem, label = dev)

    for relacao in relacoes:
        Grafo.add_edge(
            relacao['Source'], 
            relacao['Target'], 
            weigth = relacao['Strength']
            )
    
    return Grafo