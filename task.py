import httpx
import json
import os

from celery import Celery
from celery.schedules import crontab
from datetime import datetime
from utils.invoice import Invoice
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL', "http://localhost:8000")
BROKER = os.getenv('BROKER', "amqp://localhost")
# API_URL = "http://localhost:8000"
# BROKER =  "amqp://localhost"

app = Celery('task', broker=BROKER)

@app.task
def send_due_invoces(days):
    client = httpx.Client()
    response = client.get(f"{API_URL}/debts/due/{days}")
    response_json = json.loads(response.text)

    for x in response_json:
        invoice = Invoice(x["debtId"], x["debtDueDate"], x["debtAmount"])
        invoice.generate_pdf()
        invoice.send_by_email(x["email"])

        id = x["id"]
        patch_data = {"lastInvoiceSent": datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S")}
        client.patch(f"{API_URL}/debts/{id}", json=patch_data)

    return "send_due_invoces executed"


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, send_due_invoces.s(1))

    # # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )

@app.task
def test(arg):
    print(arg)

@app.task
def add(x, y):
    z = x + y
    print(z)