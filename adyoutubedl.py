#! /usr/bin/env python
# -*- coding: latin1 -*-

from os import remove, rename, path, uname, getlogin, getenv, mkdir, getcwd
from sys import argv
from subprocess import call, check_output
import datetime, time

call("clear")

linhadecomando = ["youtube-dl", "-i", "-c", "-k", "-l"]
lista = argv[1:]
lista2 = []
nomedoscript = path.basename(argv[0])
arquivodeidsinv = nomedoscript + " - idsinválidos.bvp"
arquivodeback = "." + nomedoscript + " - back.bvp"
numinv = 0
filtro = ("0", "\n", "00","000","0000","00000", "", " ", "   ","    ","     ","      ", "[InternetShortcut]")

listadesim = ("s", "y", "sim", "yes", "si", "claro", "lógico", "logico", 
"vamo torah!", "com certeza", "certamente", 'demorou', 'demoro', 'fechou')

listadenao = ("n","não", "nao", "not", "nope", "no", "jamais", "never", 
"negativo", "negative", "negativ", "nega", 'deixa pra lá', 'nem afim', 
'nem aff', 'deixa quieto', 'dexa keto')
if uname()[0].strip().lower() == "linux": pastadousuario = getenv("HOME").strip()
#pastadousuario = "/home/" + getlogin()
nomedousuario = getlogin().capitalize()
pastadeconf = path.join(pastadousuario, "." + nomedoscript)
arqaudioconf = path.join(pastadeconf, "audio.txt")
moverSN = False
############################	FUNÇÕES		############################################################################################
def Divisor(n = 40):
	print "\n","-=-"*n,"\n"

def Link():
	global lista
	link = raw_input("Cole abaixo o link do video desejado e depois precione Enter.\n").strip()
	while not link:
		print "Esqueceu o link ¬¬"
		link = raw_input("Cole abaixo o link do video desejado e depois precione Enter.\n").strip()
	lista.extend(link.split(' '))

def ver_formato():
	mensagem_formato = "\n"+nomedousuario+", digite o formato para o qual o audio será extraído ap\
ós o download (sem \".\").\nSe não deseja extrair o audio, não preencha nada.\n"
	global formato
	formatos = ("mp3", "aac", "vorbis", "m4a", "opus", "wav", "best")
	while 1:
		formato = raw_input(mensagem_formato).lower().strip()
		if formato in formatos:
			linhadecomando.extend(("--extract-audio", "--audio-quality", "0", "--audio-format", formato))
			return True
		elif formato == "":
			return False
		else:
			print "\nO formato \"{}\" não é válido, os formatos válidos são: \"{}\" e \"{}\".".format(str(formato), '", "'.join(formatos[0:-1]), formatos[-1])

def ger_inv(baixando):
	objarquivodeidsinv = open("."+arquivodeidsinv,"a")
	objarquivodeidsinv.write(baixando+"\n")
	objarquivodeidsinv.close()
	print "\nAlgo saiu errado ao tentar baixar","\""+baixando+"\"."
	if numinv == 1:
		print numinv,"URL falhou até agora."
	else:
		print numinv,"URLs falharam até agora."

def ler_arquivo(arquivo):
	global lista
	objarquivo = open(arquivo)
	for cada_item in objarquivo.readlines():
		for cada_itemd in cada_item.split(" "):			
			if cada_itemd.strip() in filtro: continue
			lista.append(cada_itemd.strip())
	
	#	if cada_item.strip() in filtro: continue
	#	lista.append(cada_item.strip())
	objarquivo.close()
	remove(arquivo)

def decisao(mensagem, listatrue = listadesim, listafalse = listadenao, mensagemdeerro = "\nOpção inválida"):
	while 1:
		global resposta
		resposta = raw_input(mensagem).lower().strip()
		if resposta in listatrue:
			return True
		elif resposta in listafalse:
			return False
		else:
			print mensagemdeerro

def encontra_pasta_audio():
	def exite_pasta(pasta):
		if path.exists(pasta):
			global pastademusica
			pastademusica = pasta
			objarqaudioconf = open(arqaudioconf, "w")
			objarqaudioconf.write(pastademusica.strip() + "\n")
			objarqaudioconf.close()
			return True
		else:
			return False
	
	if uname()[0].strip().lower() == "linux":
		print "Procurando sua pasta de músicas..." # ainda não foi implementada."
		listadepastas = ["Music", "Musica", "Musicas", "Música", "Músicas", "Musics"]
		for iterpasta in listadepastas:
			for iiterpasta in [pastadousuario+"/"+iterpasta, pastadousuario+"/"+iterpasta.lower(), pastadousuario+"/"+iterpasta.upper()]:
				if exite_pasta(iiterpasta):
					print ('Achei :)')
					return True
		while 1:
			print "{}, não foi possivel detectar automaticamente onde está sua pasta de musicas.".format(nomedousuario)
			print "Digite, ou cole, o caminho absoluto de onde o audio extraído deverá ser movido (Isso não será necessário da próxima vez ;) )",
			print " ou entre com uma linha em branco para não mover o audio."
			pasta = raw_input("").strip()
			if pasta:
				if exite_pasta(pasta): return True
			else:
				return False
	else:
		print "Função que encontra a pasta de músicas ainda não foi implementada para a plataforma {}.".format(uname()[0].strip())
		return False

def motor(baixando):
	global linhadecomando, numinv, erroyoutube
	Divisor()
	if n+1 > 1 and erroyoutube != 0: print "Indo para a próxima..."
	
	print "\nBaixando o "+str(n+1)+"º","video de",str(len(lista))+":",baixando,"\n"
	linhadecomando.append(baixando)
	
	try:
		erroyoutube = call(linhadecomando)
	except KeyboardInterrupt:
		erroyoutube = 1
		print "\nInterrompido por comando do teclado!"
	if erroyoutube != 0:
		numinv = numinv+1
		ger_inv(baixando)
		linhadecomando.pop()
	elif moverSN:
		global formato
		Divisor()
		print "Preparando para mover o audio."
		if formato == "vorbis":
			formato = "ogg"
		elif formato == "best":
			formato = "m4a"
		audioextraido = check_output(["youtube-dl", "--get-filename", linhadecomando.pop()]).strip()
		audioextraido = audioextraido[:audioextraido.rfind("."[:])+1] + formato
		print "Movendo \"{}\" para a pasta \"{}\".".format(audioextraido, pastademusica)
		rename(getcwd() + "/" + audioextraido, pastademusica + "/" + audioextraido)
	else:
		linhadecomando.pop()
		
########################################################################################################################################

if len(lista) == 0:
	Link()
del Link

if path.exists(arquivodeidsinv) or path.exists(arquivodeback) or path.exists("."+arquivodeidsinv):
	print "Recuperando links de sua ultima sessão salva nesta pasta e mesclando-os com a lista atual. Aguarde."
	if path.exists(arquivodeidsinv):
		ler_arquivo(arquivodeidsinv)
	if path.exists(arquivodeback):
		ler_arquivo(arquivodeback)
	if path.exists("."+arquivodeidsinv):
		ler_arquivo("."+arquivodeidsinv)
del ler_arquivo	
print len(lista),"Links encontrados. Filtrando os repetidos ..."
for cada_item in lista:
	if cada_item in filtro: continue
	if cada_item[0:4] == "URL=":
		cada_item = cada_item[4:]
	if len(cada_item) < 9 : continue	
	if cada_item not in lista2: lista2.append(cada_item)
lista = lista2
del lista2

#cria um arquivo de backup da lista em cwd 
objarquivodeback = open(arquivodeback,"a")
for linha in lista:
	objarquivodeback.write(linha+"\n")
objarquivodeback.close()

Divisor()
print "\tLista de URLs à serem baixadas:\n"
for n, url in enumerate(lista):
	print str(n+1)+")",url
Divisor()

# Verifica se o audio deverá ser extraído.

if ver_formato() and uname()[0].strip().lower() == "linux":
	moverSN = decisao("\nMover o audio extraído para sua pasta de musicas?\n")
call("clear")
#del formato

# Verifica para onde o audio deverá ser movido após ser extraído.
if moverSN:
	pastademusica = False
	if path.exists(arqaudioconf):
		with open(arqaudioconf) as objarqaudioconf:
			pastademusica = objarqaudioconf.readlines()[0].strip()
		if not path.exists(pastademusica):
			del pastademusica
			moverSN = encontra_pasta_audio()
	else:
		if not path.exists(pastadeconf): mkdir(pastadeconf)
		moverSN = encontra_pasta_audio()
del encontra_pasta_audio

################   principal	#########################
ts1 = datetime.datetime.now()
for n,baixando in enumerate(lista):
	try:
		motor(baixando)
	except KeyboardInterrupt:
		print ""

ts2 = datetime.datetime.now() - ts1
del motor
remove(arquivodeback)

# Mostra a lista dos links que falharam.
if numinv != 0:
	#if not moverSN or erroyoutube != 0: Divisor()
	call("clear")
	Divisor()
	print 'Tempo transcorrido: {}'.format(ts2)
	Divisor()
	if numinv == 1:
		print "\tA seguinte URL não foi baixada corretamente (talvez seja inválida):\n"
	else:
		print "\tAs",numinv,"URLs seguintes não foram baixadas corretamente. (talvez sejam inválidas):\n"
	with open("."+arquivodeidsinv) as objarquivodeidsinv:
		for n, link in enumerate(objarquivodeidsinv):
			print str(n+1)+")",link,
		Divisor()
	if decisao("Deseja salvar a lista de URLs inválidas?\n"):
		print "Salvando lista de URLs inválidas com o nome","\""+arquivodeidsinv+"\"."
		rename("."+arquivodeidsinv, arquivodeidsinv)
	else:
		print "Então, a lista de URLs inválidas NÃO será salva."
		remove("."+arquivodeidsinv)
else:
	print 'Tempo transcorrido: {}'.format(ts2)

print "\nFim da execução :3\n"
