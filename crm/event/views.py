from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerCreateSerializer, CustomerListSerializer, ContractCreateSerializer,\
    ContractListSerializer, EventCreateSerializer, EventListSerializer, NoteCreateUpdateSerializer, \
    NoteListSerializer
from management.permissions import IsAuthorize
from management.models import Users
from .models import Company, Customer, Contract, Event, Note
import datetime

class AdminCustomerViewset(ModelViewSet):
    """
    Define all the endpoints and permission for a instance Customer
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerCreateSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'get':
            permission_classes = [IsAuthorize]
        elif self.action == 'create':
            permission_classes = [IsAuthorize]
        else:
            permission_classes = [IsAuthorize]

        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        serializer = CustomerListSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        user = Users.objects.get(email=request.data['saler'])
        try:
            company = Company.objects.get(name=request.data['company'])
        except Company.DoesNotExist:
            company = Company.objects.create(name=request.data['company'],)
            company.save()
        customer = Customer(saler=user, company=company)
        serializer = CustomerCreateSerializer(customer, data=request.data)
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
        try:
            company = Company.objects.get(name=request.data['company'])
        except Company.DoesNotExist:
            company = Company.objects.create(name=request.data['company'], )
            company.save()
        customer.saler = user
        customer.company = company
        customer.date_updated = datetime.datetime.now()
        serializer = CustomerCreateSerializer(customer, data=request.data)
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
    Define all the endpoints and permission for a instance Contract
    """
    queryset = Contract.objects.all()
    serializer_class = ContractCreateSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'get':
            permission_classes = [IsAuthorize]
        elif self.action == 'create':
            permission_classes = [IsAuthorize]
        else:
            permission_classes = [IsAuthorize]

        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        serializer = ContractListSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        try:
            user = Users.objects.get(email=request.data['saler'])
        except Users.DoesNotExist:
            return Response({'error', 'saler not  exists'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = Customer.objects.get(email=request.data['customer'])
        except Customer.DoesNotExist:
            return Response({'error', 'customer not  exists'}, status=status.HTTP_400_BAD_REQUEST)
        contract = Contract(saler=user, customer=customer)
        serializer = ContractCreateSerializer(contract, data=request.data)
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
        try:
            user = Users.objects.get(email=request.data['saler'])
        except Users.DoesNotExist:
            return Response({'error', 'saler not  exists'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = Customer.objects.get(email=request.data['customer'])
        except Customer.DoesNotExist:
            return Response({'error', 'customer not  exists'}, status=status.HTTP_400_BAD_REQUEST)
        if customer is None:
            return Response({'error', 'customer not exists'}, status=status.HTTP_400_BAD_REQUEST)

        contract.saler = user
        contract.customer = customer
        contract.date_updated = datetime.datetime.now()
        serializer = ContractCreateSerializer(contract, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        contract = get_object_or_404(self.queryset, pk=pk)
        contract.delete()
        return Response(data={'response': 'contract deleted'}, status=status.HTTP_201_CREATED)


class AdminEventViewset(ModelViewSet):
    """
    Define all the endpoints and permission for a instance Event
    """
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'get':
            permission_classes = [IsAuthorize]
        elif self.action == 'create':
            permission_classes = [IsAuthorize]
        else:
            permission_classes = [IsAuthorize]

        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        serializer = EventListSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        try:
            user = Users.objects.get(email=request.data['support'])
        except Users.DoesNotExist:
            return Response({'error', 'support not  exists'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = Customer.objects.get(email=request.data['customer'])
        except Customer.DoesNotExist:
            return Response({'error', 'customer not  exists'}, status=status.HTTP_400_BAD_REQUEST)
        event = Event(support=user, customer=customer)
        serializer = EventCreateSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, *args, **kwargs):
        queryset = get_object_or_404(self.queryset, pk=pk)
        if queryset is None:
            return Response({'error', 'event not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = EventListSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        event = get_object_or_404(self.queryset, pk=pk)
        if event is None:
            return Response({'error', 'event not  exists'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Users.objects.get(email=request.data['support'])
        except Users.DoesNotExist:
            return Response({'error', 'saler not  exists'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = Customer.objects.get(email=request.data['customer'])
        except Customer.DoesNotExist:
            return Response({'error', 'customer not  exists'}, status=status.HTTP_400_BAD_REQUEST)

        event.support = user
        event.customer = customer
        event.date_updated = datetime.datetime.now()
        serializer = EventCreateSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        event = get_object_or_404(self.queryset, pk=pk)
        event.delete()
        return Response(data={'response': 'event deleted'}, status=status.HTTP_201_CREATED)


class AdminNoteViewset(ModelViewSet):
    """
    Define all the endpoints and permission for a instance Note
    """
    queryset = Note.objects.all()
    serializer_class = NoteCreateUpdateSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'get':
            permission_classes = [IsAuthorize]
        elif self.action == 'create':
            permission_classes = [IsAuthorize]
        else:
            permission_classes = [IsAuthorize]

        return [permission() for permission in permission_classes]

    def list(self, request, note_pk=None, issue_pk=None, *args, **kwargs):
        queryset = self.queryset.filter(note=note_pk)
        serializer = NoteListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, project_pk=None, issue_pk=None, *args, **kwargs):
        events = Event.objects.all()
        event = get_object_or_404(events, pk=event_pk)
        if event is not None:
            note = Note(event=event)
            serializer = NoteCreateUpdateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'error': 'event unknow'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, event_pk=None, pk=None, *args, **kwargs):
        note = get_object_or_404(self.queryset, pk=pk)
        serializer = NoteCreateUpdateSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, event_pk=None, pk=None, *args, **kwargs):
        note = get_object_or_404(self.queryset, pk=pk)
        if note is not None:
            note.delete()
            return Response(data={'response': 'note deleted'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'error': 'note unknow'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        note = get_object_or_404(self.queryset, pk=pk)
        serializer = NoteListSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)