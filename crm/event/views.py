from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerCreateUpdateSerializer, CustomerListSerializer, ContractCreateUpdateSerializer,\
    ContractListSerializer
from management.permissions import IsAuthorize
from management.models import Users
from .models import Company, Customer, Contract


class AdminCustomerViewset(ModelViewSet):
    """
    Define all the endpoints and permission for a instance Customer
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerCreateUpdateSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'get':
            permission_classes = [IsAuthorize]
        elif self.action == 'create':
            permission_classes = [IsAuthorize]
        else:
            permission_classes = [IsAuthorize]

        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        serializer = CustomerListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        user = Users.objects.get(email=request.data['saler'])
        company = Company.objects.get(name=request.data['company'])
        if company is None:
            company = Company.objects.create(
                name=request.data['company'],
            )
            company.save()
        customer = Customer(saler=user, company=company)
        serializer = CustomerCreateUpdateSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, *args, **kwargs):
        queryset = get_object_or_404(self.queryset, pk=pk)
        if queryset is None:
            return Response({'error', 'customer not  exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomerListSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        customer = get_object_or_404(self.queryset, pk=pk)
        if customer is None:
            return Response({'error', 'customer not  exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = Users.objects.get(email=request.data['saler'])
        company = Company.objects.get(name=request.data['company'])
        if company is None:
            company = Company.objects.create(
                name=request.data['company'],
            )
            company.save()
        customer.saler = user
        customer.company = company
        serializer = CustomerCreateUpdateSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        customer = get_object_or_404(self.queryset, pk=pk)
        customer.delete()
        return Response(data={'response': 'customer deleted'}, status=status.HTTP_201_CREATED)


class AdminContractViewset(ModelViewSet):
    """
    Define all the endpoints and permission for a instance Customer
    """
    queryset = Contract.objects.all()
    serializer_class = ContractCreateUpdateSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'get':
            permission_classes = [IsAuthorize]
        elif self.action == 'create':
            permission_classes = [IsAuthorize]
        else:
            permission_classes = [IsAuthorize]

        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        serializer = ContractListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        user = Users.objects.get(email=request.data['saler'])
        customer = Customer.objects.get(name=request.data['customer'])
        if customer is None:
            return Response({'error', 'customer not  exists'}, status=status.HTTP_400_BAD_REQUEST)
        contract = Contract(saler=user, customer=customer)
        serializer = ContractCreateUpdateSerializer(contract, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, *args, **kwargs):
        queryset = get_object_or_404(self.queryset, pk=pk)
        if queryset is None:
            return Response({'error', 'contract not  exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ContractListSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        contract = get_object_or_404(self.queryset, pk=pk)
        if contract is None:
            return Response({'error', 'contract not  exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = Users.objects.get(email=request.data['saler'])
        customer = Company.objects.get(name=request.data['customer'])
        if customer is None:
            return Response({'error', 'customer not exists'}, status=status.HTTP_400_BAD_REQUEST)

        contract.saler = user
        contract.customer = customer
        serializer = ContractCreateUpdateSerializer(contract, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        contract = get_object_or_404(self.queryset, pk=pk)
        contract.delete()
        return Response(data={'response': 'contract deleted'}, status=status.HTTP_201_CREATED)