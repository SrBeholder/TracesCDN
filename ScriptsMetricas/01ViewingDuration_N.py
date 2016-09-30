# -*- coding: utf-8 -*-
from __future__ import division
import os
import math
import re
import gzip
import glob
import os.path
import shutil
import fnmatch
import zipfile
from os import walk

#Define dicionário de dispositivos móveis e não móveis
def defineDicionarios(dicionarioMobile):
    ArquivoMobile = open('Mobile.txt', 'r');
    for linha in ArquivoMobile:
        dicionarioMobile.append(linha.strip())
    return dicionarioMobile

#Escreve matriz em arquivo
def EscreveArquivo(registros,numArquivo):
    for registro in registros:
        try:
            with open("ViewingDuration_"+str(numArquivo)+".txt", "a") as arquivo:
                arquivo.write(str(registro)+"\n")
        except: 
            EscreveLogErro("Erro escrita em disco")

#Escreve log em arquivo
def EscreveLog(mensagem):
    try:
        with open("Log.txt", "a") as arquivo:
            arquivo.write(str(mensagem)+"\n")
    except: 
        EscreveLogErro("Erro no log")

#Escreve log de erro em arquivo
def EscreveLogErro(mensagem):
    try:
        with open("LogErro.txt", "a") as arquivo:
            arquivo.write(str(mensagem)+"\n")
    except: 
        print("Erro no log de erro")


#Localiza se um termo pertence ao dicionário Mobile
def EncontraMobile(linha,dicionarioMobile):
    achou = False
    try:
        for termo in dicionarioMobile:
            if (linha.find(termo) != -1):
                achou = True
                break
    except: 
        EscreveLogErro("Erro na busca")
    return achou

#Localiza todos os arquivos com extensão gz no diretório origem descompacta em arquivo na pasta destino
def VarreDiretorio(caminho,dicionarioMobile, registros):
    total = 0
    numArquivo = 1 
    for conteudo in glob.glob(os.path.join(caminho, '*')):
        if os.path.isdir(conteudo):
            contadores = VarreDiretorio(conteudo)
        if fnmatch.fnmatch(conteudo, '*.gz'):
            base = os.path.basename(conteudo)
            EscreveLog("Inicio da leitura do arquivo"+str(conteudo))
            #A cada 30 arquivos salva em arquivo
            total = total + 1
            if(total == 30):
                EscreveArquivo(registros, numArquivo)
                numArquivo = numArquivo +1
                total = 0

            with gzip.open(conteudo, 'rb') as infile:
                #Para cada linha do arquivo de entrada
                for linha in infile:
                    try:
                        #Transforma linha em vetor
                        vetorLinha = linha.split()
                        #Exclui todos as colunas antes da 20ª
                        linhaLimpa = ' '.join(vetorLinha[20::])
                        #Busca termos do dicionário Mobile na linha
                        mobile = EncontraMobile(linhaLimpa,dicionarioMobile)
                        if(mobile):
                            registros.append(str(vetorLinha[9]))
                    except: 
                        EscreveLogErro("Erro leitura vetor linha")
            EscreveLog("Fim da leitura do arquivo "+str(conteudo))
    return registros

class Principal():
    registros = []
    dicionarioMobile = []

    #Coloca em memória os dicionários
    dicionarioMobile = defineDicionarios(dicionarioMobile)

    #Diretório com arquivos compactados
    caminhoOrigem = "/media/servertrace/live/live"
    #caminhoOrigem = "/home/daniel/workplace/TracesGlobo/Origem"
        
    #Localiza traces    
    registros = VarreDiretorio(caminhoOrigem,dicionarioMobile, registros)

    #Escreve resultados em arquivo
    EscreveArquivo(registros,"final")

    #Finaliza Log
    EscreveLog("Fim do script")
                 
    


