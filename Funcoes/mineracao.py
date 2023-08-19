import time
import pandas as pd
import xlsxwriter

def minerar_comentarios(login, nome, caminho, dataframe, limite_inferior, limite_superior):
    comentarios = list()
    repositorio = login.get_repo(caminho)

    for contagem, linha in enumerate(dataframe.values):
        if contagem < limite_inferior or contagem >= limite_superior: 
            pass

        else:
            issue = repositorio.get_issue(linha[6])
            
            for comentario in issue.get_comments():
                comentarios.append({
                    'ID_ISSUE': issue.id,
                    'ID_USUARIO_COMENTARIO': comentario.user.id,
                    'DATA_REGISTRO': comentario.created_at.strftime('%d/%m/%Y'),
                })

    pd.DataFrame(comentarios).to_csv(
        '{} - Comentarios {}-{}.csv'.format(nome, limite_inferior, limite_superior), 
        sep = ";"
        )



def minerar_commits(login, nome, caminho, limite_inferior, limite_superior):
    lista_commits = []

    for contagem, commit in enumerate(login.get_repo(caminho).get_commits()):
        if contagem < limite_inferior or contagem >= limite_superior:
            pass
        
        elif commit.author is not None:
            lista_commits.append({
                'ID_COMMIT': commit.sha,
                'ID_AUTOR': commit.author.id,
                'DATA_COMMIT': commit.commit.author.date.strftime('%d/%m/%Y')
            })

    pd.DataFrame(lista_commits).to_excel(
        '{} - Commits {}-{}.xlsx'.format(nome, limite_inferior, limite_superior),
        engine = 'xlsxwriter'
        )



def minerar_issues(login, nome, caminho, limite_inferior, limite_superior):
    lista_issue = []

    for contagem, issue in enumerate(login.get_repo(caminho).get_issues(state = 'all')):
        if contagem < limite_inferior:
            pass

        elif contagem >= limite_superior:
            break

        else:
            lista_issue.append({
                'ID_ISSUE': issue.id,
                'TITULO ISSUE': issue.title,
                'DATA_CRIAÇÃO': issue.created_at.strftime("%d/%m/%Y"),
                'DATA_FINALIZAÇÃO': issue.closed_at.strftime("%d/%m/%Y") if issue.closed_at is not None else "Não finalizada",
                'ID_AUTOR': issue.user.id,
                'PULL_REQUEST': "Verdadeiro" if issue.pull_request else "Falso",
                'NUMBER_ISSUE': issue.number
            })

    pd.DataFrame(lista_issue).to_excel(
        '{} - Issues {}-{}.xlsx'.format(nome, limite_inferior, limite_superior),
        engine = 'xlsxwriter'
        )