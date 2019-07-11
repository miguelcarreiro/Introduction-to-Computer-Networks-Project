import socket;
import time;
import sys;
ClientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
n = 0
iserverip = '127.0.0.1'
iserverport = 5005
buffer = 100
tab = []
jogando = False

def envia():
	ClientMsg = str(input("Introduza comando: "))
	ClientSock.sendto(ClientMsg.encode(), (iserverip, iserverport))

def envia_f(ClientMsg):
	ClientSock.sendto(ClientMsg.encode(), (iserverip, iserverport))

def recebe():
	(ServerMsg, (ServerIP, ServerPort)) = ClientSock.recvfrom(buffer)
	return (ServerMsg.decode(), ServerIP, ServerPort)

def regista():
	msg = str(input("Introduza o seu nome de utilizador: "))
	msg = "REGISTO " + msg
	envia_f(msg)
	print(recebe()[0])

def parametros():
	print("IP servidor: " + iserverip)
	print("Porta servidor: " + str(iserverport))
	print("Buffer: " + str(buffer))

def cria_tabuleiro():
	global tab
	tab = [[0,0,0],[0,0,0],[0,0,0]]

def convida_jogador():
	user = input("Insira o nome do utilizador a convidar: ")
	envia_f("CONVITE " + user)

def recebe_jogada(pos, sim):
	pos_ln = eval(pos[0])
	pos_cl = eval(pos[1])
	jogada((pos_ln, pos_cl), sim)

def jogada(pos, sim):
	global tab
	p1 = pos[0]
	p2 = pos[1]
	if p1 < len(tab) and p2 < len(tab) and tab[p1][p2] == 0:
		tab[p1][p2] = sim
	else:
		return -1

def tab_completo():
	#verifica se existem posições vazias
	for n in tab:
		if 0 in n:
			return False
	return True

def escreve_tabuleiro():
    for l in range(3):
        for c in range(3):
        	if tab[l][c] == 0:
        		print('[', ' ', ']', end=' ')
        	else:
        		print('[', tab[l][c], ']', end=' ')
        print()


def joga_galo(comeca):
	cria_tabuleiro()
	global tab
	s = False
	while s == False:
		if comeca == 1:
			jog = pede_jogada()
			recebe_jogada(jog, "o")
			print("Sua jogada")
			escreve_tabuleiro()
		else:
			print("Bem-vindo ao GaloOnline. Aguarde que o seu adversário se lembre de jogar")
		print()
		c = verifica_vitoria()
		if c != -1:
			envia_f("FIMJOGO " + str(c))
			print_res(c)
			return 1
		print("Aguarde a sua vez")
		print()
		tup_msg = recebe()[0].split()
		comeca = 1
		if tup_msg[0] == "JOGADA":
			recebe_jogada(tup_msg[1], "x")
			print("Jogada do adversário")
			escreve_tabuleiro()
			print()
		elif tup_msg[0] == "FIMJOGO":
			s = True
			print_res(tup_msg[1])
			return 1
	return 1

def print_res(res):
	if res == 2:
		print("Você ganhou!! Parabéns!!")
	elif res == 0:
		print("Você perdeu. ÓÓÓ")
	else:
		print("Você empatou, ou seja, ninguém ganhou nem ninguém perdeu.")


def verifica_vitoria():
	p1 = ("o", "Jogador 1")
	p2 = ("x", "Jogador 2")
    # Rows
	for row in tab:
	    if row[0] == row[1] == row[2] == p1[0]:
        	return 2
	    elif row[0] == row[1] == row[2] == p2[0]:
        	return 0
    # Colunas
	for i in range(3):
		if tab[0][i] == tab[1][i] == tab[2][i] == p1[0]:
			return 2
		elif tab[0][i] == tab[1][i] == tab[2][i] == p2[0]:
			return 0
    # Diagonal 1
	if tab[0][0] == tab[1][1] == tab[2][2] == p1[0]:
		return 2
	elif tab[0][0] == tab[1][1] == tab[2][2] == p2[0]:
		return 0
    # Diagonal 2
	elif tab[2][0] == tab[1][1] == tab[0][2] == p1[0]:
		return 2
	elif tab[2][0] == tab[1][1] == tab[0][2] == p2[0]:
		return 0
	t = tab_completo()
	if t == True:
		return 1
	else:
		return -1

def convida_jogador():
	user = input("Insira o nome do utilizador a convidar: ")
	envia_f("CONVITE " + user)
	msg_s = recebe()[0]
	msg = msg_s.split()
	if msg[0] == "CONVITEACEITE":
		return True
	else:
		print(msg_s)
		return False


def pede_jogada():
	print("Insira a sua jogada")
	jog = input("Formato : xy | x - linha, y - coluna -> ")
	while jog[0] != "0" and jog[0] != "1" and jog[0] != "2" and jog[1] != "0" and jog[1] != "1" and jog[1] != "2":
		print("Jogada incorreta. Tente outra vez")
		print("Insira a sua jogada")
		jog = input("Formato : xy | x - linha, y - coluna -> ")
	envia_f("JOGADA " + jog)
	return jog
		
def espera_convite():
	c = False
	while c == False:
		msg = recebe()[0].split()
		if msg[0] == "CONVITE":
			c == True
			print("Recebeu um convite de: " + msg[1])
			r = input("Pretende jogar com ele?\nS - Sim | N - Não -> ")
			if r == "S":
				envia_f("CONVITEACEITE " + msg[1])
				joga_galo(1)
				return 1

#menu incompleto
def menu():
	s = False
	while s == False:
		print("Escolha uma das seguintes opções:")
		print("1 - Registar novo utilizador")
		print("2 - Jogar")
		print("3 - Obter lista de utilizadores registados")
		print("4 - Enviar comando personalizado")
		print("5 - Parâmetros de ligação")
		print("6 - Convites")
		print("7 - Sair")
		n = input("--> ")
		if n == "1":
			regista()
			s == True
		elif n == "2":
			c = convida_jogador()
			if c == True:
				joga_galo(0)
			else:
				print("Convite recusado")
		elif n == "3":
			envia_f("LISTA")
			print(recebe()[0])
		elif n == "4":
			envia()
			print(recebe()[0])
			s == True
		elif n == "5":
			parametros()
		elif n == "6":
			j = espera_convite()
		elif n == "7":
			print("Obrigado por jogar. Adeus")
			envia_f("SAIR")
			print(recebe()[0])
			sys.exit()
		else:
			print("Opção inválida. Tente de novo")

while True:
	menu()


ClientSock.close()