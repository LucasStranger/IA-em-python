#pip3 install pyTelegramBotAPI
#pip3 install --upgrade pyTelegramBotAPI
#pip3 install telebot
#pip3 install python-decouple
import telebot
import csv
from decouple import config
import time
from datetime import datetime
import random

NAME, EMAIL = range(2)
user_data = {}
token = config("TOKEN_BOT")

bot = telebot.TeleBot(token)

# Função para salvar as conversas
def salvar(arquivo, conversa: list):
    with open(arquivo, 'a') as chat:
        e = csv.writer(chat)
        e.writerow(conversa)

# Função para iniciar a conversa com o BOT
@bot.message_handler(commands=['start', 'iniciar'])
def start(message):
    bot.send_message(message.chat.id, "Oi Bom dia, tudo bem com você?", timeout=120)

@bot.message_handler(regexp='iniciar')
def iniciar(message):
    salvar('iniciar.csv', [message.chat.id, message.from_user.username, message.text, datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    bot.send_message(message.chat.id, "Oi Bom dia, tudo bem com você?", timeout=120)

@bot.message_handler(regexp=r'tudo|sim|não')
def pergunta(message):
    bot.send_message(message.chat.id, "Se estiver tendo um dia ruim, apenas posso desejar melhoras, mas se estiver tendo um dia bom, que continue dessa forma :).", timeout=120)
    time.sleep(2)
    bot.send_message(message.chat.id, "Como deseja agendar sua consulta?\nDigite:\n1 para cadastro na fila de atendimento\n2 para atendimento online\n3 para cancelar cadastramento\n4 para sair", timeout=120)

# Função para iniciar o cadastro na fila de atendimento
@bot.message_handler(func=lambda message: message.text == '1')
def start_cadastro(message):
    msg = bot.send_message(message.chat.id, "Vamos começar o cadastro. Por favor, digite seu nome:", timeout=120)
    bot.register_next_step_handler(msg, get_name)

def get_name(message):
    user_data[message.chat.id] = {'name': message.text}
    time.sleep(2)
    msg = bot.send_message(message.chat.id, "Obrigado! Agora, por favor, digite seu e-mail:", timeout=120)
    bot.register_next_step_handler(msg, get_email)

def get_email(message):
    user_data[message.chat.id]['email'] = message.text
    name = user_data[message.chat.id].get('name')
    email = user_data[message.chat.id].get('email')
    time.sleep(2)
    bot.send_message(message.chat.id, f'Cadastro realizado com sucesso!\nNome: {name}\nE-mail: {email}', timeout=120)

# Função para iniciar o atendimento online
@bot.message_handler(func=lambda message: message.text == '2')
def start_online(message):
    msg = bot.send_message(message.chat.id, "Vamos começar o cadastro para o atendimento online. Por favor, digite seu nome:", timeout=120)
    bot.register_next_step_handler(msg, get_name_online)

def get_name_online(message):
    user_data[message.chat.id] = {'name': message.text}
    time.sleep(2)
    msg = bot.send_message(message.chat.id, "Obrigado! Agora, por favor, digite seu e-mail:", timeout=120)
    bot.register_next_step_handler(msg, get_email_online)

def get_email_online(message):
    user_data[message.chat.id]['email'] = message.text
    name = user_data[message.chat.id].get('name')
    email = user_data[message.chat.id].get('email')
    time.sleep(2)
    
    # Gerar ID, senha e link do Zoom (exemplo simplificado)
    zoom_id = random.randint(100000, 999999)
    zoom_password = random.randint(1000, 9999)
    zoom_link = f"https://zoom.us/j/{zoom_id}?pwd={zoom_password}"

    bot.send_message(message.chat.id, f'Cadastro para atendimento online realizado com sucesso!\nNome: {name}\nE-mail: {email}\nID do Zoom: {zoom_id}\nSenha do Zoom: {zoom_password}\nLink do Zoom: {zoom_link}', timeout=120)

# Função para cancelar o cadastramento
@bot.message_handler(func=lambda message: message.text == '3')
def cancelar_cadastro(message):
    # Limpar os dados do usuário, se necessário
    if message.chat.id in user_data:
        del user_data[message.chat.id]
    
    time.sleep(2)
    bot.send_message(message.chat.id, "Seu cadastramento na fila de espera foi cancelado.", timeout=120)

# Função para oferecer convênio antes de sair
@bot.message_handler(func=lambda message: message.text == '4')
def oferecer_convenio(message):
    response = ("Você gostaria de conhecer o nosso convênio hospitalar antes de sair?\n"
                "Digite 'sim' para mais informações ou 'não' para sair.")
    msg = bot.send_message(message.chat.id, response, timeout=120)
    bot.register_next_step_handler(msg, handle_convenio_response)

def handle_convenio_response(message):
    if message.text.lower() == 'sim':
        time.sleep(2)
        convenio_info = ("Nosso convênio hospitalar oferece uma série de benefícios, incluindo:\n"
                         "- Consultas médicas gratuitas\n"
                         "- Descontos em exames laboratoriais\n"
                         "- Atendimento prioritário\n"
                         "- Acesso a programas de bem-estar e saúde\n"
                         "Para mais informações, visite nosso site: [link do site].")
        bot.send_message(message.chat.id, convenio_info, timeout=120)
        time.sleep(2)
    bot.send_message(message.chat.id, "Obrigado por utilizar nossos serviços! Até a próxima.", timeout=120)

# Iniciar o bot
bot.polling(none_stop=True)


'''
@bot.message_handler(regexp='bora')
def download(message):
    doc = open("Aulas\\Dadoteca.pdf","rb")
    bot.send_message(message.chat.id, "Show! Partiu download!",timeout=120)
    time.sleep(2)
    bot.send_document(message.chat.id, doc, timeout=120)
    time.sleep(4)
    bot.send_message(message.chat.id, "Obrigado pelo download! Apreveite o livro! Querendo reinicar nossa conversa digite iniciar",timeout=120)
    time.sleep(2)
    bot.send_message(message.chat.id, "Tmj e boas análises!",timeout=120)
'''
'''
@bot.message_handler(regexp='depois')
def convencimento(message):
    time.sleep(6)
    bot.send_message(message.chat.id, "É sério? Tu não vai querer? Vou te dar mais uma chance de saber tudo e mais um pouco sobre metodologias de projetos de BI. Bora fazer fazer o download?",timeout=120)
    time.sleep(6)
    bot.send_message(message.chat.id, "Tu já sabe o que tem que digitar, né? rssss Mas, vou te lembrar, por via das dúvidas. Digite Bora para receber esse arquivo! Do contrário, digite Tchau, vou ficar triste, mas fazer o que :(",timeout=120)

@bot.message_handler(regexp='tchau')
def tchau(message):
    time.sleep(2)
    bot.send_message(message.chat.id, "Teimosão, hein!",timeout=120)
    time.sleep(6)
    bot.send_message(message.chat.id, "Rsssss brincadeiras a parte, se quser reforçar o seu conhecimento em projetos de BI, assista a playlist gratuita, no link https://youtube.com/playlist?list=PLPP4r1UqnhGp13iYi4C1WN99o3SSgCpXJ",timeout=120)
    time.sleep(2)
    bot.send_message(message.chat.id, "Caso mude de ideia, basta digitar iniciar, para iniciar o papo e realizar o download.",timeout=120)
    time.sleep(2)
    bot.send_message(message.chat.id, "Tmj e boas análises!",timeout=120)
'''
#sondagem, verificar se há mensagens