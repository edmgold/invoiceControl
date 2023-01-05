from tests.base.debts import create_valid_debt, create_invalid_debt
from models.debt import Debts
import pytest

def test_create_valid_debt() -> None:
    attributes = create_valid_debt()
    print(attributes)
    Debts(**attributes)

def test_create_debt_with_government_id_wrong_size() -> None:
    with pytest.raises(ValueError, match='Government Id need to have 11 digits'):
        attributes = create_invalid_debt(['governmentId__size'])
        Debts(**attributes)
 
def test_create_debt_with_government_id_wrong_format() -> None:
    with pytest.raises(ValueError, match='Government Id need to be numeric'):
        attributes = create_invalid_debt(['governmentId__format'])
        Debts(**attributes)       
 
def test_create_debt_with_invalid_email() -> None:
    with pytest.raises(ValueError, match='Email format is invalid'):
        attributes = create_invalid_debt(['email'])
        Debts(**attributes)  


        