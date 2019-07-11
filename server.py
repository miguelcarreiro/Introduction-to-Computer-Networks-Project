import socket;
n = 0
ServerSock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
ServerSock.bind(('', 5005))
msg = ""
users = []
jogos_atuais = []
def leitor():
	while True:
		(ClientMsg, (ClientIP, ClientPort)) = ServerSock.recvfrom(100)
		ClientMsg = ClientMsg.decode().split()
		if ClientMsg[0] == "REGISTO":
			msg = regista(ClientMsg[1], ClientIP, ClientPort)
			envia(msg, ClientIP, ClientPort)
		elif ClientMsg[0] == "LISTA":
			msg = lista(ClientIP)
			envia(msg, ClientIP, ClientPort)
		elif ClientMsg[0] == "CONVITE":
			convite(ClientMsg[1], ClientIP, ClientPort)
		elif ClientMsg[0] == "CONVITEACEITE":
			comeca_jogo(ClientMsg[1], ClientIP, ClientPort)
		elif ClientMsg[0] == "JOGADA":
			jogada(ClientMsg[1], ClientIP, ClientPort)
		elif ClientMsg[0] == "FIMJOGO":
			acaba_jogo(ClientMsg, ClientIP, ClientPort)
		elif ClientMsg[0] == "SAIR":
			apaga_user(ClientIP, ClientPort)
		else:
			msg = "Comando inválido" 


def envia(msg, ClientIP, ClientPort):
	ServerSock.sendto(msg.encode(), (ClientIP, ClientPort))

def regista(user, ClientIP, ClientPort):
	for i in users:
		if i[0] == user:
			return "ERROREGISTO - nome já existente"
	u = ip_obtem_user(ClientIP, ClientPort)
	if u != -1:
		users[u] = [user, ClientIP, ClientPort, 1]
	else:
		us = [user, ClientIP, ClientPort, 1]
		users.append(us)
	return "OKREGISTO " + user

def ip_obtem_user(ClientIP, ClientPort):
	for i in range(len(users)):
		if users[i][1] == ClientIP and users[i][2] == ClientPort:
			return i
	return -1

def obtem_user(user):
	for i in range(len(users)):
		if users[i][0] == user:
			return i
	return -1

def lista(ClientIP):
	c = False
	if len(users) == 1 and users[0][1] == ClientIP:
		lst = users[0][0] + ":" + str(users[0][3])
		c = True
	if len(users) > 1:
		p = users[0]
		lst = p[0] + ":" + str(p[3])
		if p[1] == ClientIP:
			c = True
		for n in users[1:]:
			lst += "\n" + n[0] + ":" + str(n[3])
			if n[1] == ClientIP:
				c = True
	if c == False:
		return "ERROLISTA - acesso negado"
	return lst

def convite(ClientMsg, ClientIP, ClientPort):
	msg = ""
	pOrigem = ip_obtem_user(ClientIP, ClientPort)
	pDestino = obtem_user(ClientMsg)
	if pOrigem == -1:
		msg = "ERROCONVITE " + ClientMsg + " - você não está registado"
	elif pDestino == -1:
		msg = "ERROCONVITE " + ClientMsg + " - utilizador não encontrado"
	elif users[pDestino][3] == 0:
		msg = "ERROCONVITE " + ClientMsg + " - utilizador ocupado"
	else:
		msg = "CONVITE " + str(users[pOrigem][0])
		ClientIP = users[pDestino][1]
		ClientPort = users[pDestino][2]


	envia(msg, ClientIP, ClientPort)

def comeca_jogo(user_org, ip_dest, port_dest):
	pos_org = obtem_user(user_org)
	pos_dest = ip_obtem_user(ip_dest, port_dest)
	users[pos_org][3] = 0
	users[pos_dest][3] = 0
	jogos_atuais.append((users[pos_org][0], users[pos_dest][0]))
	msg = "CONVITEACEITE " + users[pos_dest][0]
	envia(msg, users[pos_org][1], users[pos_org][2])

def jogada(msg, ip_org, port_org):
	pos_org = ip_obtem_user(ip_org, port_org)

	for i in jogos_atuais:
		if users[pos_org][0] in i:
			if i[0] != users[pos_org][0]:
				pos_dest = obtem_user(i[0])
			else:
				pos_dest = obtem_user(i[1])
	msg = "JOGADA " + msg
	envia(msg, users[pos_dest][1], users[pos_dest][2])

def acaba_jogo(msg, ip_org, port_org):
	pos_org = ip_obtem_user(ip_org, port_org)
	for i in range(len(jogos_atuais)):
		if users[pos_org][0] in jogos_atuais[i]:
			if jogos_atuais[i][0] != users[pos_org][0]:
				pos_dest = obtem_user(jogos_atuais[i][0])
			else:
				pos_dest = obtem_user(jogos_atuais[i][1])
			del(jogos_atuais[i])
	msg_s = "FIMJOGO" + msg[1]
	envia(msg_s, users[pos_dest][1], users[pos_dest][2])

def apaga_user(ClientIP, ClientPort):
	pos = ip_obtem_user(ClientIP, ClientPort)
	if pos != -1:
		del(users[pos])
	envia("SAIROK", ClientIP, ClientPort)


leitor()
ServerSock.close()
