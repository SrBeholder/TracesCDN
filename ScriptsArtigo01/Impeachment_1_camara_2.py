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


#Localiza se a data do trace pertence ao intervalo desejado
def EncontraData(dataNova, dicionarioData):
    for data in dicionarioData:
        if (data == dataNova):
            return True
    return False

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
            with open("Impeachment_"+str(numArquivo)+".txt", "a") as arquivo:
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
def VarreDiretorio(caminho,dicionarioMobile, dicionarioData):
    numArquivo = 1
    for conteudo in glob.glob(os.path.join(caminho, '*')):
        if os.path.isdir(conteudo):
            contadores = VarreDiretorio(conteudo)
        if fnmatch.fnmatch(conteudo, '*.gz'):
            #Limpa nome do arquivo
            dataArquivo = conteudo.replace("nginx-fe_access-","")
            dataArquivo = dataArquivo.replace("nginx-fe_monitor-","")
            dataArquivo = dataArquivo.replace("nginx-fe_crypto_access-","")
            dataArquivo = dataArquivo.replace(caminho,"")
            dataArquivo = dataArquivo.replace("/","")
            dataArquivo = dataArquivo[:8]
            #Localiza se data está no intervalo definido
            achou = EncontraData(dataArquivo, dicionarioData)
            if(achou == True):
                registros = []
                EscreveLog("Inicio da leitura do arquivo "+str(conteudo))
                base = os.path.basename(conteudo)                
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
                                #adicionar SESSÃO_6 USUÁRIO_0 REQUEST_TIME_9 TIME_STAMP_2 BODY_BYTES_11
                                registros.append(str(vetorLinha[6]) + " " + str(vetorLinha[0]) + " " + str(vetorLinha[9]) + " " + str(vetorLinha[2]) + " " + str(vetorLinha[11]))
                        except: 
                            EscreveLogErro("Erro leitura vetor linha")
                #A cada arquivo salva em arquivo
                EscreveArquivo(registros, numArquivo)
                numArquivo = numArquivo +1
                EscreveLog("Fim da leitura do arquivo "+str(conteudo))            

class Principal():
    EscreveLog("Inicío script")
    dicionarioMobile = []
    dicionarioData = []
    dicionarioData.append("20160418")

    #Coloca em memória os dicionários
    dicionarioMobile = defineDicionarios(dicionarioMobile)

    #Diretório com arquivos compactados
    caminhoOrigem = "/media/servertrace/live/live"
    #caminhoOrigem = "/home/daniel/workplace/TracesCDN/Origem"
        
    #Localiza traces    
    VarreDiretorio(caminhoOrigem,dicionarioMobile, dicionarioData)

    #Finaliza Log
    EscreveLog("Fim do script")
                 
    


