from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Customer, Company, Event, Note
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


class CustomerUpdateSerializer(ModelSerializer):
    """
       Serialize the model Customer
    """
    company = CompanySerializer(read_only=True)
    saler = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'date_updated', 'email', 'phone', 'mobile',
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
        model = Customer
        fields = ['amount', 'payement_due', 'status', 'customer', 'saler']


class ContractUpdateSerializer(ModelSerializer):
    """
       Serialize the model Customer
    """
    saler = UserSerializer(read_only=True)
    customer = CustomerListSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['amount', 'payement_due', 'status', 'date_updated', 'customer', 'saler']


class ContractListSerializer(ModelSerializer):

    saler = UserSerializer(read_only=True)
    customer = CustomerListSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'


class EventCreateSerializer(ModelSerializer):
    """
       Serialize the model Customer
    """
    support = UserSerializer(read_only=True)
    customer = CustomerListSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['attendees', 'date_event', 'status', 'date_updated', 'support', 'customer']


class EventUpdateSerializer(ModelSerializer):
    """
       Serialize the model Customer
    """
    support = UserSerializer(read_only=True)
    customer = CustomerListSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['attendees', 'date_event', 'status', 'date_updated', 'support', 'customer']


class EventListSerializer(ModelSerializer):

    support = UserSerializer(read_only=True)
    customer = CustomerListSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


class NoteCreateUpdateSerializer(ModelSerializer):
    """
       Serialize the model Customer
    """
    class Meta:
        model = Note
        fields = ['note']



class NoteListSerializer(ModelSerializer):

    class Meta:
        model = Note
        fields = '__all__'

    def get_event(self, request, instance):
        queryset = event.customer.all()
        serializer = EventListSerializer(queryset, many=True)
        return serializer.data