from django.test import Client
from event.views import AdminCustomerViewset, AdminContractViewset, AdminNoteViewset, AdminEventViewset
from management.models import Users
import pytest
import datetime
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from event.models import Customer, Event, Contract, Note, Company
from rest_framework.authtoken.models import Token

client = Client()




def create_saler():
    user = Users.objects.create(
        email="loic2.hernio@gmail.com",
        first_name="loic2",
        last_name="hernio",
        password="12345Test",
        mobile=12345,
        phone=12345,
        type="SALER", )
    return user

def create_support():
    user = Users.objects.create(
        email="loic3.hernio@gmail.com",
        first_name="loic3",
        last_name="hernio",
        password="12345Test",
        mobile=12345,
        phone=12345,
        type="SUPPORT", )
    return user

def create_customer():
    company = Company.objects.create(
        name="Apple"
    )
    saler = create_saler()
    customer = Customer.objects.create(
        email="steve.jobs@gmail.com",
        first_name="steve",
        last_name="jobs",
        mobile=12345,
        phone=12345,
        company=company,
        saler=saler
    )
    return customer

def create_contract():
    customer =create_customer()
    saler = Users.objects.get(email="loic2.hernio@gmail.com")
    contract = Contract.objects.create(
        status = "SIGNE",
        amount = 100.0,
        payement_due = 200.0,
        customer = customer,
        saler = saler,
    )
    return contract

def create_event():
    contract = create_contract()
    support = create_support()
    customer = Customer.objects.get(email="steve.jobs@gmail.com")

    event = Event.objects.create(
        status = "SIGNE",
        attendees = "loic, daniel",
        date_event = datetime.datetime.now(),
        customer = customer,
        contract = contract,
        support = support,
    )
    return event

@pytest.mark.django_db
def test_user_model():
    user = Users.objects.create(
               email = "loic.hernio@gmail.com",
            first_name = "loic",
            last_name = "hernio",
            password = "12345Test",
            mobile = 12345,
            phone = 12345,
            type = "SUPPORT",)
    expected_value = "loic hernio"
    assert str(user) == expected_value

@pytest.mark.django_db
def test_company_model():
    company = Company.objects.create(
        name = "Apple"
    )
    expected_value = "Apple"
    assert str(company) == expected_value

@pytest.mark.django_db
def test_customer_model():
    customer = create_customer()
    expected_value = "steve jobs"
    assert str(customer) == expected_value

@pytest.mark.django_db
def test_contract_model():
    contract = create_contract()
    expected_value = "customer: steve jobs saler: loic2 hernio"
    assert str(contract) == expected_value

@pytest.mark.django_db
def test_event_model():
    event = create_event()
    expected_value = "support: loic3 hernio  event: 1"
    assert str(event) == expected_value

@pytest.mark.django_db
def test_AdminCustomerViewset_list(client):
    user = Users.objects.create(
        email="loic.hernio@gmail.com",
        first_name="loic",
        last_name="hernio",
        password="12345Test",
        mobile=12345,
        phone=12345,
        type="SUPPORT", )
    refresh = RefreshToken.for_user(user)
    headers_dict = {"Authorization": "Bearer "+ str(refresh.access_token)}
    rv = client.get(f'/customers/', {}, headers=headers_dict, follow=True)

    assert rv.status_code == 201

@pytest.mark.django_db
def test_AdminContractViewset_list(client):
    user = Users.objects.create(
        email="loic.hernio@gmail.com",
        first_name="loic",
        last_name="hernio",
        password="12345Test",
        mobile=12345,
        phone=12345,
        type="SUPPORT", )
    """refresh = RefreshToken.for_user(user)
    headers_dict = {"authorization": "Bearer "+ str(refresh.access_token)}
    print(headers_dict)"""
    token, created = Token.objects.get_or_create(user=user)
    client = Client(HTTP_AUTHORIZATION='Bearer ' + token.key)

    rv = client.get(f'/contracts', {}, follow=True)
    assert rv.status_code == 201

"""@pytest.mark.django_db
def test_login(client):
    user = create_saler()
    data=dict(email=user.email, password=user.password)
    rv = client.post(f'/login', data, follow=True)
    assert rv.status_code == 201"""

