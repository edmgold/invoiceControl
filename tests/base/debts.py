
debt_base = {
    "name": "pedro",
    "governmentId": "11111111111",
    "email": "aaa@aaa.com.br",
    "debtAmount": 1000,
    "debtDueDate": "2023-01-02T19:24:07.653Z",
    "debtId": 1
}

def create_valid_debt(id=None):
    debt = debt_base.copy()

    if id:
        debt["id"] = id

    return debt.copy()

def create_invalid_debt(invalid_fields=[]):
    debt = debt_base.copy()
        
    if 'governmentId__size' in invalid_fields:
        debt['governmentId'] = "1212"

    if 'governmentId__format' in invalid_fields:
        debt['governmentId'] = "1111111111X"

    if 'email' in invalid_fields:
        debt['email'] = "eeee"

    return debt
