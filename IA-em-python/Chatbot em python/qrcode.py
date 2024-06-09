import qrcode

# URL do link de conversa com o bot
bot_link = "https://web.telegram.org/k/#@jadelenoir_bot"

# Gerar o código QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(bot_link)
qr.make(fit=True)

# Criar uma imagem do código QR
img = qr.make_image(fill_color="black", back_color="white")

# Salvar a imagem do código QR
img.save("bot_qr_code.png")

print("Código QR do bot gerado com sucesso!")