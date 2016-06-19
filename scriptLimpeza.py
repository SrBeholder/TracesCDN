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

#Localiza todos os arquivos e compara o nome com o passado na função
def VarreDiretorio(caminho,conteudoOriginal, conteudoOriginalCaminho):
    for conteudo in glob.glob(os.path.join(caminho, '*')):
        if(str(conteudo.replace(caminho,"")) == str(conteudoOriginal)):
                os.remove(conteudoOriginalCaminho)

class Principal():
    #Diretório para comparação
    caminhoOrigem = "/home/daniel/workplace/TracesGlobo/CopiaZica"
    caminhoComparacao = "/home/daniel/workplace/TracesGlobo/TraceNamoral"
    
    #Busca por arquivos repetidos para limpeza
    for conteudoCaminho in glob.glob(os.path.join(caminhoOrigem, '*')):
        if (os.path.isdir(conteudoCaminho) == False):
            conteudo = conteudoCaminho.replace(caminhoOrigem,"")
            VarreDiretorio(caminhoComparacao, conteudo, conteudoCaminho)

