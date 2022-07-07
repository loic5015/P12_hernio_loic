from rest_framework.serializers import ModelSerializer
from .models import Customer, Company
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
        serializer = CompanySerializer(queryset, many=True)
        return serializer.data

    def get_saler(self, request, instance):
        queryset = instance.users.all()
        serializer = UserSerializer(queryset, many=True)
        return serializer.data
