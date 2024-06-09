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
import threading
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    
    try:
        with open('jade-de-ari-jade-honkai-star-rail.gif', 'rb') as gif:
            bot.send_animation(message.chat.id, gif)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Desculpe, não consegui encontrar o GIF para enviar.")
    
    bot.send_message(message.chat.id, "Como já deve ver, meu nome é Jade. Estou aqui para ajudar você na sua jornada de cadastramento dentro do hospital.", timeout=120)

@bot.message_handler(regexp='iniciar')
def iniciar(message):
    salvar('iniciar.csv', [message.chat.id, message.from_user.username, message.text, datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    bot.send_message(message.chat.id, "Oi Bom dia, tudo bem com você?", timeout=120)

@bot.message_handler(regexp=r'tudo|sim|não')
def pergunta(message):
    bot.send_message(message.chat.id, "Se estiver tendo um dia ruim, apenas posso desejar melhoras, mas se estiver tendo um dia bom, que continue dessa forma :).", timeout=120)
    time.sleep(2)
    bot.send_message(message.chat.id, "Como deseja agendar sua consulta?\nDigite:\n1- Para cadastro na fila de atendimento\n2- Para atendimento online\n3- Para cancelar cadastramento\n4- Para sair\n5- Informações sobre doenças", timeout=120)
    set_timeout(message)

# Função para iniciar o cadastro na fila de atendimento
@bot.message_handler(func=lambda message: message.text == '1')
def start_cadastro(message):
    cancel_timeout(message)
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
    cancel_timeout(message)
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
    cancel_timeout(message)
    # Limpar os dados do usuário, se necessário
    if message.chat.id in user_data:
        del user_data[message.chat.id]
    
    time.sleep(2)
    bot.send_message(message.chat.id, "Seu cadastramento na fila de espera foi cancelado.", timeout=120)

# Função para oferecer convênio antes de sair
@bot.message_handler(func=lambda message: message.text == '4')
def oferecer_convenio(message):
    cancel_timeout(message)
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
        bot.send_animation(message.chat.id, open('honkai-star-rail-jade.gif', 'rb'))  # Enviar GIF do convênio
    else:
        bot.send_animation(message.chat.id, open('honkai-star-rail-jade.gif', 'rb'))  # Enviar GIF de saída
    
    time.sleep(2)
    bot.send_message(message.chat.id, "Obrigado por utilizar nossos serviços! Até a próxima.", timeout=120)


# Função para análise de dados e geração de gráficos
# Função para gerar gráfico de barras etc..
def gerar_grafico_doencas(tipo):
    # Exemplo de dados
    dados = {
        'Doença': ['Dengue', 'Diabetes', 'Hipertensão', 'Cancer'],
        'Casos': [150, 200, 120, 80]
    }
    df = pd.DataFrame(dados)
    cores = sns.color_palette("husl", len(df['Doença']))

    plt.figure(figsize=(10, 6))
    
    if tipo == 'bar':
        sns.barplot(x='Doença', y='Casos', data=df, palette=cores)
        plt.title('Casos de Doenças (Gráfico de Barras)')
    elif tipo == 'pie':
        plt.pie(df['Casos'], labels=df['Doença'], autopct='%1.1f%%', colors=cores)
        plt.title('Casos de Doenças (Gráfico de Pizza)')
    elif tipo == 'line':
        sns.lineplot(x='Doença', y='Casos', data=df, marker='o', color='blue')
        plt.title('Casos de Doenças (Gráfico de Linhas)')
    elif tipo == 'area':
        plt.fill_between(df['Doença'], df['Casos'], color='skyblue', alpha=0.4)
        plt.plot(df['Doença'], df['Casos'], color='Slateblue', alpha=0.6)
        plt.title('Casos de Doenças (Gráfico de Área)')
    elif tipo == 'scatter':
        plt.scatter(df['Doença'], df['Casos'], color='purple')
        plt.title('Casos de Doenças (Gráfico de Dispersão)')
    elif tipo == 'hist':
        plt.hist(df['Casos'], bins=10, color='green', alpha=0.7)
        plt.title('Casos de Doenças (Histograma)')
        plt.xlabel('Número de Casos')
        plt.ylabel('Frequência')
    elif tipo == 'box':
        sns.boxplot(y='Casos', data=df, color='orange')
        plt.title('Casos de Doenças (Gráfico de Caixas)')
        plt.ylabel('Número de Casos')
    else:
        # Caso o tipo especificado não seja reconhecido
        plt.text(0.5, 0.5, 'Tipo de gráfico não suportado', horizontalalignment='center', verticalalignment='center')
        plt.axis('off')
    
    plt.xlabel('Doença')
    plt.ylabel('Número de Casos')

    # Salvar gráfico
    plt.savefig('grafico_doencas.png')

# Função para enviar gráfico
@bot.message_handler(func=lambda message: message.text in ['bar', 'pie', 'line', 'area', 'scatter', 'hist', 'box'])
def enviar_grafico_doencas(message):
    gerar_grafico_doencas(message.text)
    bot.send_photo(message.chat.id, photo=open('grafico_doencas.png', 'rb'))
    bot.send_message(message.chat.id, f"Aqui está o gráfico informativo sobre doenças no formato {message.text}.", timeout=120)

# Função para enviar mensagem de orientação
@bot.message_handler(func=lambda message: message.text == '5')
def orientar_tipo_grafico(message):
    bot.send_message(message.chat.id, "Por favor, escolha o tipo de gráfico que deseja gerar: \n'bar' para gráfico de barras, \n'pie' para gráfico de pizza, \n'line' para gráfico de linhas, \n'area' para gráfico de área, \n'scatter' para gráfico de dispersão, \n'hist' para histograma ou 'box' para gráfico de caixas.")


# Dicionário para rastrear os timers
user_timers = {}

def set_timeout(message):
    chat_id = message.chat.id
    if chat_id in user_timers:
        user_timers[chat_id].cancel()

    timer = threading.Timer(30, timeout_message, [chat_id])
    user_timers[chat_id] = timer
    timer.start()

def cancel_timeout(message):
    chat_id = message.chat.id
    if chat_id in user_timers:
        user_timers[chat_id].cancel()
        del user_timers[chat_id]

def timeout_message(chat_id):
    bot.send_message(chat_id, "Por favor digite algumas das alternativas acima como dito antes para continuar.", timeout=120)

# Captura todas as outras mensagens que não correspondem às opções válidas
@bot.message_handler(func=lambda message: message.text not in ['1', '2', '3', '4', '5'])
def invalid_option(message):
    bot.send_message(message.chat.id, "Por favor, escolha uma das alternativas para continuar:\n1- Para cadastro na fila de atendimento\n2- Para atendimento online\n3- Para cancelar cadastramento\n4- Para sair\n5- Informações sobre doenças", timeout=120)
    set_timeout(message)

# Iniciar o bot
bot.polling(none_stop=True)
#sondagem, verificar se há mensagens