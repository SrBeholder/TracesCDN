# -*- coding: utf-8 -*-
from __future__ import division
import os
import math
import re
import gzip
import glob
import os.path
import shutil
from os import walk

dicionarioMobile = []
dicionarioDesktop = []

totalRegistros = 0;
totalMobile = 0;
totalDesktop = 0;

def defineDicionarios():
    ArquivoMobile = open('Mobile.txt', 'r');
    for linha in ArquivoMobile:
        dicionarioMobile.append(linha.strip())

    ArquivoDesktop = open('Desktop.txt', 'r');
    for linha in ArquivoDesktop:
        dicionarioDesktop.append(linha.strip())

def EncontraTermo(linha):
    achou = False
    for termo in dicionarioMobile:
        if (linha.find(termo) != -1):
            global totalMobile
            totalMobile = totalMobile + 1
            achou = True
            break
    if(achou == False):
        for termo in dicionarioDesktop:
            if (linha.find(termo) != -1):
                global totalDesktop
                totalDesktop = totalDesktop + 1
                achou = True
                break
    return achou

class Principal():
    #Coloca em memória os dicionários
    defineDicionarios()

    totalRegistros = 0;
    totalMobile = 0;
    totalDesktop = 0;

    #Diretório com arquivos compactados
    #caminhoOrigem = "/home/daniel/Dropbox/Live_Characterization/SampleTraces/Origem"
    #caminhoOrigem = "/home/posgrad/dvasconcelos/Downloads/SampleTraces"
    caminhoOrigem = "/home/daniel/workplace/TracesGlobo/Origem"

    #Diretório de trabalho, é apagado no fim do código
    #caminhoDestino = "/home/posgrad/dvasconcelos/Downloads/SampleTraces"    
    caminhoDestino = "/home/daniel/workplace/TracesGlobo"

    #Localiza todos os arquivos com extensão gz no diretório origem descompacta em arquivo na pasta destino
    for arquivoGZ in glob.glob(os.path.join(caminhoOrigem, '*.gz')):
        base = os.path.basename(arquivoGZ)
        with gzip.open(arquivoGZ, 'rb') as infile:
            with open('Undefined.txt', 'a') as outfile:
                #Para cada linha do arquivo de entrada
                for linha in infile:
                    global totalRegistros
                    totalRegistros = totalRegistros + 1
                    #Transforma linha em vetor
                    vetorLinha = linha.split()
                    #Exclui todos as colunas antes da 20ª
                    linhaLimpa = ' '.join(vetorLinha[20::])
                    #Busca termos dos dicionários na linha, caso não encontre, escrever no dicionário "Undefined"
                    if(EncontraTermo(linhaLimpa) == False):
                        outfile.write(linhaLimpa+"\n")

    global totalMobile
    global totalDesktop
    global totalRegistros
    print(totalMobile)
    print(totalDesktop)
    print(totalRegistros)
                 
    


