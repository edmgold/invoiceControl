import asyncio
import pytest
import ormar
import os
import pandas as pd
from fastapi.testclient import TestClient
from models.debt import Debts
from tests.base.debts import create_valid_debt, create_invalid_debt

def test_get_all_debts (client: TestClient) -> None:
    attributes = create_valid_debt()
    debt = Debts(**attributes)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(debt.save())
    
    response = client.get("/debts/")
    content = response.json()

    assert response.status_code == 200
    assert len(content) == 1

def test_get_all_debts_fail (client: TestClient) -> None:
    response = client.get("/debts/")
    content = response.json()

    assert response.status_code == 200
    assert not content

def test_get_one_debit (client: TestClient) -> None:
    attributes = create_valid_debt(100)
    debt = Debts(**attributes)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(debt.save())
    
    response = client.get("/debts/100")
    content = response.json()

    assert response.status_code == 200
    assert content["email"] == debt.email

def test_get_one_invalid_debit (client: TestClient) -> None:
    response = client.get("/debts/100")
    content = response.json()

    assert response.status_code == 404
    assert content["detail"] == "Entity not found"

def test_post_debit(client: TestClient) -> None:
    body = create_valid_debt()
    response = client.post("/debts/", json=body)
    content = response.json()
    assert response.status_code == 200
    assert content["email"] == body["email"]

def test_post_invalid_debit(client: TestClient) -> None:
    body = create_invalid_debt(['email'])
    response = client.post("/debts/", json=body)
    content = response.json()
    assert response.status_code == 422

def test_patch_debt(client: TestClient) -> None:
    attributes = create_valid_debt()
    debt = Debts(**attributes)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(debt.save())

    paid_by = 'test'
    attributes_for_patch = {'paidBy': paid_by}

    response = client.patch(f"/debts/{debt.id}", json=attributes_for_patch)
    content = response.json()
    updated_debt = loop.run_until_complete(Debts.objects.get(id=debt.id))

    assert response.status_code == 200
    assert content["paidBy"] == paid_by
    assert updated_debt.paidBy == paid_by 

def test_patch_invalid_debt(client: TestClient) -> None:
    paid_by = 'test'
    attributes_for_patch = {'paidBy': paid_by}

    response = client.patch(f"/debts/1", json=attributes_for_patch)
    content = response.json()

    assert response.status_code == 404
    assert content["detail"] == "Entity not found"
      
def test_delete_debt(client: TestClient) -> None:
    attributes = create_valid_debt()
    debt = Debts(**attributes)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(debt.save())

    response = client.delete(f"/debts/{debt.id}")

    with pytest.raises(ormar.exceptions.NoMatch): 
        loop.run_until_complete(Debts.objects.get(id=debt.id))

    assert response.status_code == 200        
         
def test_delete_invalid_debt(client: TestClient) -> None:
    response = client.delete(f"/debts/1")
    content = response.json()

    assert response.status_code == 404
    assert content["detail"] == "Entity not found"

def test_get_due_debts (client: TestClient) -> None:
    attributes = create_valid_debt()
    attributes['debtDueDate'] = "2020-01-03T22:33:11.155000"
    debt = Debts(**attributes)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(debt.save())
    
    response = client.get("/debts/due/1")
    content = response.json()
    
    assert response.status_code == 200
    assert content[0]['debtDueDate'] == "2020-01-03T22:33:11.155000"
    assert len(content) == 1

def test_get_invalid_due_debts (client: TestClient) -> None:
    response = client.get("/debts/due/1")
    content = response.json()

    assert response.status_code == 200
    assert not content

def test_upload(client: TestClient) -> None:
    data = {
        "name": ["John Doe"],
        "governmentId": ["11111111111"],
        "email": ["johndoe@kanastra.com.br"],
        "debtAmount": [1000000.00],
        "debtDueDate": ["2022-10-12"],
        "debtId": [8291]
    }
    df = pd.DataFrame(data)

    df.to_csv( "test.csv", sep=";", index=False)

    files = {'file': ('test.csv', open('test.csv', 'rb'))}
    response = client.post("/debts/upload", files=files)
    content = response.json()
    os.remove("test.csv")
    assert response.status_code == 200
    assert content["detail"][0]["email"] == data["email"][0]

def test_upload_empty_file(client: TestClient) -> None:
    with open('test.csv', 'w') as fp: 
        pass    

    files = {'file': ('test.csv', open('test.csv', 'rb'))}
    response = client.post("/debts/upload", files=files)
    content = response.json()
    os.remove("test.csv")
    assert response.status_code == 404
    assert content["detail"] == "Empty file"

def test_upload_invalid_file(client: TestClient) -> None:
    data = {
        "name": ["John Doe"],
        "governmentId": ["11111111111"],
        "email": ["johndoe@kanastra.com.br"],
        "debtAmount": [1000000.00],
        "debtDueDate": ["2022-10-12"],
        "debtId": [8291]
    }
    df = pd.DataFrame(data)

    df.to_html("test.csv")

    files = {'file': ('test.xml', open('test.csv', 'rb'))}
    response = client.post("/debts/upload", files=files)
    content = response.json()
    os.remove("test.csv")
    assert response.status_code == 404
    assert content["detail"] == "Invalid file"

def test_webhook(client: TestClient) -> None:
    attributes = create_valid_debt(100)
    debt = Debts(**attributes)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(debt.save())

    body = {
        "debtId": debt.debtId,
        "paidAt": "2022-06-09 10:00:00",
        "paidAmount": 100000.00,
        "paidBy": "John Doe"
    }
    
    response = client.post("/debts/webhook", json=body)
    content = response.json()
    print(content)
    assert response.status_code == 200
    assert content == "OK"

def test_webhook_invalid(client: TestClient) -> None:
    body = {
        "debtId": "10",
        "paidAt": "2022-06-09 10:00:00",
        "paidAmount": 100000.00,
        "paidBy": "John Doe"
    }
    
    response = client.post("/debts/webhook", json=body)
    content = response.json()
    print(content)
    assert response.status_code == 200
    assert content == "Parametros inválidos"    