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


def encontraTermos(linha):
	dicionario = []
	dicionario.append("Android");
	dicionario.append("iPhone");
	dicionario.append("iPad");

	achou = False
	for termo in dicionario:
		if(linha.find(termo) != -1):
			achou = True
	return achou

class Principal():
	
	#Diretório com arquivos compactados
	caminhoOrigem = "/home/daniel/Dropbox/Live_Characterization/SampleTraces/Origem"
	#Diretório de trabalho, é apagado no fim do código
	caminhoDestino = "/home/daniel/Dropbox/Live_Characterization/SampleTraces/Destino"	

	#Localiza todos os arquivos com extensão gz no diretório origem descompacta em arquivo na pasta destino
	for arquivoGZ in glob.glob(os.path.join(caminhoOrigem, '*.gz')):
	    base = os.path.basename(arquivoGZ)
	    dest_name = os.path.join(caminhoDestino, base[:-3])
	    with gzip.open(arquivoGZ, 'rb') as infile:
	        with open(dest_name, 'w') as outfile:
	            for line in infile:					
					#1)Escreve linha a linha
					if(encontraTermos(line) == False):
						outfile.write(line)

					#2)Avalia linha a linha
					#Escreve a linha como vetor
					#linha = line.split()
					#print(linha[20])
