import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(str(Path(__file__).parent.parent) + "/.env")

SMTP = os.getenv('SMTP')
PORT = os.getenv('PORT', 587)
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')

class Invoice:
    def __init__(self, debtId, dueDate, amount):
        self.debtId = debtId
        self.dueDate = dueDate
        self.amount = amount
    
    def generate_pdf(self):
        canvas = Canvas("boleto.pdf", pagesize=A4)

        canvas.drawString(50, 750, f"Número do boleto: {self.debtId}")
        canvas.drawString(50, 700, f"Vencimento: {self.dueDate}")
        canvas.drawString(50, 650, f"Valor: R$ {self.amount:.2f}")

        canvas.save()

        return True


    def send_by_email(self, destinatario):
        try:
            server = smtplib.SMTP(host=SMTP, port=PORT)
            
            server.login(SMTP_USER, SMTP_PASS)
            
            mensagem = MIMEMultipart()
            mensagem["From"] = "Boleto 1.0"
            mensagem["To"] = destinatario
            mensagem["Subject"] = "Boleto Vencido"
            
            with open("boleto.pdf", "rb") as arquivo:
                anexo = MIMEApplication(arquivo.read(), _subtype="pdf")
                anexo.add_header("Content-Disposition", "attachment", filename="boleto.pdf")
                mensagem.attach(anexo)
            
            server.sendmail("cobranca@boleto10.com.br", destinatario, mensagem.as_string())
            
            server.quit()
        except Exception as ex:
            print(ex) 

        return True

