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
import thread
import threading
import time
from os import walk

#Localiza se a data do trace pertence ao intervalo desejado
def EncontraData(dataNova, dicionarioData):
    for data in dicionarioData:
        if (data == dataNova):
            return True
    return False

#Escreve matriz em arquivo
def EscreveArquivo(registros,numArquivo):
    for registro in registros:
        with open("Bruno_videosUsuario_"+str(numArquivo)+".txt", "a") as arquivo:
            try:
                registro = str(registro).replace("'","")
                registro = str(registro).replace("[","")
                registro = str(registro).replace(",","")
                registro = str(registro).replace("]","")
                arquivo.write(str(registro)+"\n")
            except: 
                EscreveLogErro("Erro ao escrever: "+str(numArquivo))

#Escreve log em arquivo
def EscreveLog(mensagem):
    try:
        with open("Log.txt", "a") as arquivo:
            arquivo.write(str(mensagem)+"\n")
    except: 
        EscreveLogErro("Erro ao escrever logErro")

#Escreve log de erro em arquivo
def EscreveLogErro(mensagem):
    try:
        with open("LogErro.txt", "a") as arquivo:
            arquivo.write(str(mensagem)+"\n")
    except: 
        print("Erro no log de erro")

#Classe Thread para chamada multiprogramada
class VarreDiretorio(threading.Thread):
    def __init__(self, caminho, dicionarioData):
        threading.Thread.__init__(self)
        self.caminho = caminho
        self.dicionarioData = dicionarioData
    #Localiza todos os arquivos com extensão gz no diretório origem descompacta em arquivo na pasta destino
    def run(self):
        registros = []
        numArquivo = 1
        caminho = self.caminho
        dicionarioData = self.dicionarioData
        for conteudo in glob.glob(os.path.join(caminho, '*')):
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
                    EscreveLog("Inicio da leitura do arquivo"+str(conteudo))
                    base = os.path.basename(conteudo)
                    with gzip.open(conteudo, 'rb') as infile:
                        #Para cada linha do arquivo de entrada
                        total = 0
                        for linha in infile:
                            try:
                                vetorLinha = linha.split()
                                if(vetorLinha[10] != "/healthcheck\"]"):
                                    hashUsuario = vetorLinha[10].split("h=")[1][:69]
                                    #Localiza se existe registro de um determinado usuário
                                    idVideo = vetorLinha[10].split("_")[0][-7:]
                                    saida = [registro.append(vetorLinha[0]+ " " + vetorLinha[5] + " " + idVideo) for registro in registros if (registro[0] == hashUsuario)]
                                    if(saida == []):
                                        novoRegistro = []
                                        novoRegistro.append(hashUsuario)
                                        novoRegistro.append(vetorLinha[0]+ " " + vetorLinha[5] + " " + idVideo)
                                        registros.append(novoRegistro)
                            except:
                                pass
                    EscreveArquivo(registros,str(dicionarioData)+"_"+str(numArquivo))
                    numArquivo = numArquivo +1
        EscreveLog("Fim_da_Thread_"+str(dicionarioData))
        EscreveArquivo(registros,"Final"+"_"+str(dicionarioData))
        




EscreveLog("Inicio do script")
#Diretório com arquivos compactados
#caminhoOrigem = "/home/daniel/workplace/TracesGlobo/Vod"
caminhoOrigem = "/media/servertrace/vod/vod_20160212_20160313"

#Define datas do dicionário
#dicionarioData.append("20160304")   
#dicionarioData.append("20160305")
#dicionarioData.append("20160306")    
#dicionarioData.append("20160307")
#dicionarioData.append("20160308")  
#dicionarioData.append("20160309")
#dicionarioData.append("20160310")
#dicionarioData.append("20160311")
#dicionarioData.append("20160312")
#dicionarioData.append("20160313")

#Cria as threads para localizar traces e filtrar informações
dicionarioData = []
dicionarioData.append("20160304")
thread1 = VarreDiretorio(caminhoOrigem, dicionarioData)
dicionarioData = []
dicionarioData.append("20160305")
thread2 = VarreDiretorio(caminhoOrigem, dicionarioData)
dicionarioData = []
dicionarioData.append("20160306")
thread3 = VarreDiretorio(caminhoOrigem, dicionarioData)
dicionarioData = []
dicionarioData.append("20160307")
thread4 = VarreDiretorio(caminhoOrigem, dicionarioData)
dicionarioData = []
dicionarioData.append("20160308")
thread5 = VarreDiretorio(caminhoOrigem, dicionarioData)
dicionarioData = []
dicionarioData.append("20160309")
thread6 = VarreDiretorio(caminhoOrigem, dicionarioData)
dicionarioData = []
dicionarioData.append("20160310")
thread7 = VarreDiretorio(caminhoOrigem, dicionarioData)
dicionarioData = []
dicionarioData.append("20160311")
thread8 = VarreDiretorio(caminhoOrigem, dicionarioData)
dicionarioData = []
dicionarioData.append("20160312")
thread9 = VarreDiretorio(caminhoOrigem, dicionarioData)
dicionarioData = []
dicionarioData.append("20160313")
thread10 = VarreDiretorio(caminhoOrigem, dicionarioData)

thread1.start()
thread2.start()
thread3.start()
thread4.start()
#thread5.start()
#thread6.start()
#thread7.start()
#thread8.start()
#thread9.start()
#thread10.start()

EscreveLog("Fim do script")
