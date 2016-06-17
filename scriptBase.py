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



dicionarioMobile = []
dicionarioDesktop = []

global totalRegistros
totalRegistros = 0
global totalMobile
totalMobile = 0
global totalDesktop
totalDesktop = 0

#Defini dicionário de dispositivos móveis e não móveis
def defineDicionarios():
    ArquivoMobile = open('Mobile.txt', 'r');
    for linha in ArquivoMobile:
        dicionarioMobile.append(linha.strip())

    ArquivoDesktop = open('Desktop.txt', 'r');
    for linha in ArquivoDesktop:
        dicionarioDesktop.append(linha.strip())

#Localiza se um termo dos dicionários para classificar registro
#Registros não classificados são marcados como 'undefined'
def EncontraTermo(linha,contadores):
    achou = False
    for termo in dicionarioMobile:
        if (linha.find(termo) != -1):
            contadores[0] = contadores[0] + 1
            achou = True
            break
    if(achou == False):
        for termo in dicionarioDesktop:
            if (linha.find(termo) != -1):
                contadores[1] = contadores[1] + 1
                achou = True
                break
    contadores[3] = achou
    return contadores

#Localiza todos os arquivos com extensão gz no diretório origem descompacta em arquivo na pasta destino
def VarreDiretorio(caminho,contadores):
    for conteudo in glob.glob(os.path.join(caminho, '*')):
        print(conteudo)
        if os.path.isdir(conteudo):
            print("diretorio")
            contadores = VarreDiretorio(conteudo,contadores)
        if fnmatch.fnmatch(conteudo, '*.gz'):
            print("arquivo")
            base = os.path.basename(conteudo)
            with gzip.open(conteudo, 'rb') as infile:
                with open('Undefined.txt', 'a') as outfile:
                    #Para cada linha do arquivo de entrada
                    for linha in infile:
                        contadores[2] = contadores[2] + 1
                        #Transforma linha em vetor
                        vetorLinha = linha.split()
                        #Exclui todos as colunas antes da 20ª
                        linhaLimpa = ' '.join(vetorLinha[20::])
                        #Busca termos dos dicionários na linha, caso não encontre, escrever no dicionário "Undefined"
                        contadores = EncontraTermo(linhaLimpa,contadores)
                        if(contadores[3] == False):
                            outfile.write(linhaLimpa+"\n")
    return contadores



class Principal():
    #Contadores [0]totalMobile [1]totalDesktop [2]totalRegistros
    contadores = [0,0,0,False]

    #Coloca em memória os dicionários
    defineDicionarios()

    #Diretório com arquivos compactados
    #caminhoOrigem = "/media/servertrace/live"
    caminhoOrigem = "/home/daniel/workplace/TracesGlobo/Origem"

    #Localiza traces    
    contadores = VarreDiretorio(caminhoOrigem, contadores)

    print(contadores)
                 
    


