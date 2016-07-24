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

#Defini dicionário de dispositivos móveis e não móveis
def defineDicionarios():
    ArquivoMobile = open('Mobile.txt', 'r');
    for linha in ArquivoMobile:
        dicionarioMobile.append(linha.strip())

#Localiza se um termo pertence ao dicionário Mobile
def EncontraMobile(linha):
    achou = False
    for termo in dicionarioMobile:
        if (linha.find(termo) != -1):
            achou = True
            break
    return achou

#Localiza todos os arquivos com extensão gz no diretório origem descompacta em arquivo na pasta destino
def VarreDiretorio(caminho):
    for conteudo in glob.glob(os.path.join(caminho, '*')):
        if os.path.isdir(conteudo):
            contadores = VarreDiretorio(conteudo)
        if fnmatch.fnmatch(conteudo, '*.gz'):
            base = os.path.basename(conteudo)
            with gzip.open(conteudo, 'rb') as infile:
                #Para cada linha do arquivo de entrada
                for linha in infile:
                    #Transforma linha em vetor
                    vetorLinha = linha.split()
                    #Exclui todos as colunas antes da 20ª
                    linhaLimpa = ' '.join(vetorLinha[20::])
                    #Busca termos do dicionário Mobile na linha
                    mobile = EncontraMobile(linhaLimpa)
                    if(mobile):
                        print(str(vetorLinha[9]))

class Principal():
    #Coloca em memória os dicionários
    defineDicionarios()

    #Diretório com arquivos compactados
    caminhoOrigem = "/media/servertrace/live/live"
    
    #Localiza traces    
    VarreDiretorio(caminhoOrigem)

    print("fim")
                 
    


