from rest_framework.serializers import ModelSerializer
from .models import Customer, Company, Event, Note
from management.serializers import UserSerializer


class CustomerCreateUpdateSerializer(ModelSerializer):
    """
       Serialize the model Customer
    """
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'date_updated', 'email', 'phone', 'mobile',
                  'company', 'saler']


class CustomerListSerializer(ModelSerializer):

    class Meta:
        model: Customer
        fields = '__all__'

    def get_company(self, request, instance):
        queryset = instance.company.all()
        serializer = CompanySerializer(queryset, many=True)
        return serializer.data

    def get_saler(self, request, instance):
        queryset = instance.users.all()
        serializer = UserSerializer(queryset, many=True)
        return serializer.data


class CompanySerializer(ModelSerializer):

    class Meta:
        model: Company
        fields = '__all__'


class ContractCreateUpdateSerializer(ModelSerializer):
    """
       Serialize the model Customer
    """
    class Meta:
        model = Customer
        fields = ['amount', 'payement_due', 'status', 'date_updated', 'customer', 'saler']


class ContractListSerializer(ModelSerializer):

    class Meta:
        model: Customer
        fields = '__all__'

    def get_customer(self, request, instance):
        queryset = instance.customer.all()
        serializer = CustomerListSerializer(queryset, many=True)
        return serializer.data

    def get_saler(self, request, instance):
        queryset = instance.users.all()
        serializer = UserSerializer(queryset, many=True)
        return serializer.data


class EventCreateUpdateSerializer(ModelSerializer):
    """
       Serialize the model Customer
    """
    class Meta:
        model = Event
        fields = ['attendees', 'date_event', 'status', 'date_updated', 'support', 'customer']


class EventListSerializer(ModelSerializer):

    class Meta:
        model: Event
        fields = '__all__'

    def get_customer(self, request, instance):
        queryset = instance.customer.all()
        serializer = CustomerListSerializer(queryset, many=True)
        return serializer.data

    def get_support(self, request, instance):
        queryset = instance.users.all()
        serializer = UserSerializer(queryset, many=True)
        return serializer.data


class NoteCreateUpdateSerializer(ModelSerializer):
    """
       Serialize the model Customer
    """
    class Meta:
        model = Note
        fields = ['note']



class NoteListSerializer(ModelSerializer):

    class Meta:
        model: Note
        fields = '__all__'

    def get_event(self, request, instance):
        queryset = event.customer.all()
        serializer = EventListSerializer(queryset, many=True)
        return serializer.data