from django.test import Client
from event.views import AdminCustomerViewset, AdminContractViewset, AdminNoteViewset, AdminEventViewset
from management.models import Users
import pytest
import datetime
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from event.models import Customer, Event, Contract, Note, Company
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import Group
import json
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient

client = Client()
PASSWORD= "12345Test"


@pytest.mark.django_db
def create_saler():
    user = Users.objects.create_user(
        email="loic2.hernio@gmail.com",
        first_name="loic2",
        last_name="hernio",
        mobile=12345,
        phone=12345,
        type="SALER",
        is_active=True,
        password=PASSWORD
    )
    my_group, created = Group.objects.get_or_create(name='saler')
    my_group.user_set.add(user)
    return user

@pytest.mark.django_db
def create_support():
    user = Users.objects.create_user(
        email="loic3.hernio@gmail.com",
        first_name="loic3",
        last_name="hernio",
        mobile=12345,
        phone=12345,
        type="SUPPORT",
        is_active=True,
        password=PASSWORD)
    my_group, created = Group.objects.get_or_create(name='support')
    my_group.user_set.add(user)
    return user

@pytest.mark.django_db
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

@pytest.mark.django_db
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

@pytest.mark.django_db
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
def create_note():
    event = create_event()
    try:
        user = Users.objects.get(email="loic3.hernio@gmail.com")
    except Users.DoesNotExist:
        user = create_support()

    note = Note.objects.create(
        note = "lorem ipsum ....",
        support = user,
        event = event,
    )
    return note

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
def user_authentication_saler(client):
    try:
        user = Users.objects.get(email="loic2.hernio@gmail.com")
    except Users.DoesNotExist:
        user = create_saler()
    data = {"email": user.email, "password": PASSWORD}
    r = client.post("/login/", data=data, follow=True)
    response = r.json()
    auth_token = response["access"]
    token = f"Bearer {auth_token}"
    return token

@pytest.mark.django_db
def user_authentication_support(client):
    try:
        user = Users.objects.get(email="loic3.hernio@gmail.com")
    except Users.DoesNotExist:
        user = create_support()
    data = {"email": user.email, "password": PASSWORD}
    r = client.post("/login/", data=data, follow=True)
    response = r.json()
    auth_token = response["access"]
    token = f"Bearer {auth_token}"
    return token


@pytest.mark.django_db
def test_AdminCustomerViewset_list_saler(client):

    token = user_authentication_saler(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get("/customers", follow=True)
    assert rv.status_code == 201


@pytest.mark.django_db
def test_AdminCustomerViewset_list_support(client):

    token = user_authentication_support(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get("/customers", follow=True)
    assert rv.status_code == 201

@pytest.mark.django_db
def test_AdminCustomerViewset_get_saler(client):
    customer = create_customer()
    token = user_authentication_saler(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get(f"/customers/{customer.id}", follow=True)
    assert rv.status_code == 200


@pytest.mark.django_db
def test_AdminCustomerViewset_get_support(client):
    customer = create_customer()
    token = user_authentication_support(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get(f"/customers/{customer.id}", follow=True)
    assert rv.status_code == 200

@pytest.mark.django_db
def test_AdminCustomerViewset_delete_saler(client):
    customer = create_customer()
    token = user_authentication_saler(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.delete(f"/customers/{customer.id}", follow=True)
    assert rv.status_code == 200


@pytest.mark.django_db
def test_AdminCustomerViewset_delete_support(client):
    customer = create_customer()
    token = user_authentication_support(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.delete(f"/customers/{customer.id}", follow=True)
    print(rv.json())
    assert rv.status_code == 200

@pytest.mark.django_db
def test_AdminContractViewset_list_saler(client):

    token = user_authentication_saler(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get("/contracts", follow=True)
    assert rv.status_code == 201


@pytest.mark.django_db
def test_AdminContractViewset_list_support(client):

    token = user_authentication_support(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get("/contracts", follow=True)
    assert rv.status_code == 201

@pytest.mark.django_db
def test_AdminContractViewset_get_saler(client):
    contract = create_contract()
    token = user_authentication_saler(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get(f"/contracts/{contract.id}", follow=True)
    assert rv.status_code == 200


@pytest.mark.django_db
def test_AdminContractViewset_get_support(client):
    contract = create_contract()
    token = user_authentication_support(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get(f"/contracts/{contract.id}", follow=True)
    assert rv.status_code == 200

@pytest.mark.django_db
def test_AdminContractViewset_delete_saler(client):
    contract = create_contract()
    token = user_authentication_saler(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.delete(f"/contracts/{contract.id}", follow=True)
    assert rv.status_code == 200


@pytest.mark.django_db
def test_AdminContractViewset_delete_support(client):
    contract = create_contract()
    token = user_authentication_support(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.delete(f"/contracts/{contract.id}", follow=True)
    print(rv.json())
    assert rv.status_code == 200

@pytest.mark.django_db
def test_AdminEventViewset_list_saler(client):

    token = user_authentication_saler(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get("/events", follow=True)
    assert rv.status_code == 201


@pytest.mark.django_db
def test_AdminEventViewset_list_support(client):

    token = user_authentication_support(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get("/events", follow=True)
    assert rv.status_code == 201

@pytest.mark.django_db
def test_AdminEventViewset_get_saler(client):
    event = create_event()
    token = user_authentication_saler(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get(f"/events/{event.id}", follow=True)
    assert rv.status_code == 200


@pytest.mark.django_db
def test_AdminEventViewset_get_support(client):
    event = create_event()
    token = user_authentication_support(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get(f"/events/{event.id}", follow=True)
    assert rv.status_code == 200

@pytest.mark.django_db
def test_AdminEventViewset_delete_saler(client):
    event = create_event()
    token = user_authentication_saler(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.delete(f"/events/{event.id}", follow=True)
    assert rv.status_code == 200


@pytest.mark.django_db
def test_AdminEventViewset_delete_support(client):
    event = create_event()
    token = user_authentication_support(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.delete(f"/events/{event.id}", follow=True)
    print(rv.json())
    assert rv.status_code == 200

@pytest.mark.django_db
def test_AdminNoteViewset_list_saler(client):
    note = create_note()
    token = user_authentication_saler(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get(f"/events/{note.event.id}/notes", follow=True)
    assert rv.status_code == 201


@pytest.mark.django_db
def test_AdminNoteViewset_list_support(client):
    note = create_note()
    token = user_authentication_support(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get(f"/events/{note.event.id}/notes", follow=True)
    assert rv.status_code == 201

@pytest.mark.django_db
def test_AdminNoteViewset_get_saler(client):
    note = create_note()
    token = user_authentication_saler(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get(f"/events/{note.event.id}/notes/{note.id}", follow=True)
    assert rv.status_code == 201


@pytest.mark.django_db
def test_AdminEventViewset_get_support(client):
    note = create_note()
    token = user_authentication_support(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get(f"/events/{note.event.id}/notes/{note.id}", follow=True)
    assert rv.status_code == 201

@pytest.mark.django_db
def test_AdminEventViewset_delete_saler(client):
    note = create_note()
    token = user_authentication_saler(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get(f"/events/{note.event.id}/notes/{note.id}", follow=True)
    assert rv.status_code == 201


@pytest.mark.django_db
def test_AdminEventViewset_delete_support(client):
    note = create_note()
    token = user_authentication_support(client)
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=token)
    rv = client1.get(f"/events/{note.event.id}/notes/{note.id}", follow=True)
    print(rv.json())
    assert rv.status_code == 201