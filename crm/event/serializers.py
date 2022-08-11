from rest_framework.serializers import ModelSerializer
from .models import Customer, Company, Event, Note, Contract
from management.serializers import UserSerializer


class CompanySerializer(ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class CustomerCreateSerializer(ModelSerializer):
    """
       Serialize the model Customer
    """
    company = CompanySerializer(read_only=True)
    saler = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'mobile',
                  'company', 'saler']


class CustomerListSerializer(ModelSerializer):
    company = CompanySerializer(read_only=True)
    saler = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'


class ContractCreateSerializer(ModelSerializer):
    """
       Serialize the model Customer
    """
    saler = UserSerializer(read_only=True)
    customer = CustomerListSerializer(read_only=True)

    class Meta:
        model = Contract
        fields = ['amount', 'payement_due', 'status', 'customer', 'saler']


class ContractListSerializer(ModelSerializer):

    saler = UserSerializer(read_only=True)
    customer = CustomerListSerializer(read_only=True)

    class Meta:
        model = Contract
        fields = '__all__'


class EventCreateSerializer(ModelSerializer):
    """
       Serialize the model Customer
    """
    support = UserSerializer(read_only=True)
    customer = CustomerListSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['attendees', 'date_event', 'status', 'support', 'customer', 'contract']


class EventListSerializer(ModelSerializer):

    support = UserSerializer(read_only=True)
    customer = CustomerListSerializer(read_only=True)
    contract = ContractListSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


class NoteCreateUpdateSerializer(ModelSerializer):
    """
       Serialize the model Customer
    """
    support = UserSerializer(read_only=True)
    customer = CustomerListSerializer(read_only=True)

    class Meta:
        model = Note
        fields = ['note', 'support', 'customer']


class NoteListSerializer(ModelSerializer):
    support = UserSerializer(read_only=True)
    customer = CustomerListSerializer(read_only=True)

    class Meta:
        model = Note
        fields = '__all__'
