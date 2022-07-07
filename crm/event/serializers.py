from rest_framework.serializers import ModelSerializer
from .models import Customer, Company
from management.serializers import UserSerializer


class CustomerCreateUpdateSerializer(ModelSerializer):
    """
       Serialize the model Customer
    """
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'date_created', 'date_updated', 'email', 'phone', 'mobile',
                  'company', 'saler']


class CustomerListSerializer(ModelSerializer):

    class Meta:
        model: Customer
        fields = '__all__'

    def get_company(self, request, instance):
        queryset = instance.contributors.all()
        serializer = CompanySerializer(queryset, many=True)
        return serializer.data

    def get_saler(self, request, instance):
        queryset = instance.contributors.all()
        serializer = UserSerializer(queryset, many=True)
        return serializer.data


class CompanySerializer(ModelSerializer):

    class Meta:
        model: Company
        fields = '__all__'
