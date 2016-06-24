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

#Localiza se uma data já foi adicionada
def EncontraTermo(dataNova):
    with open('Data.txt', 'r') as arquivo:
        for data in arquivo:
            if (data != dataNova):
                return True
    return False


#Localiza todos os arquivos com extensão gz no diretório origem descompacta em arquivo na pasta destino
def VarreDiretorio(caminho):
    for conteudo in glob.glob(os.path.join(caminho, '*')):
        if fnmatch.fnmatch(conteudo, '*.gz'):
            conteudo = conteudo.replace("nginx-fe_access-","")
            conteudo = conteudo.replace("nginx-fe_monitor-","")
            conteudo = conteudo.replace(caminho,"")
            conteudo = conteudo.replace("/","")
            conteudo = conteudo[:8]
            print(conteudo)
            if(EncontraTermo(conteudo) == False):
                with open('Data.txt', 'a') as outfile:
                    outfile.write(conteudo+"\n")

class Principal():
    #Diretório com arquivos compactados
    #caminhoOrigem = "/media/servertrace/live/live_20151230_20160126"
    caminhoOrigem = "/home/daniel/workplace/TracesGlobo/Origem"

    #Localiza traces    
    contadores = VarreDiretorio(caminhoOrigem)

    print("fim")
                 
    


