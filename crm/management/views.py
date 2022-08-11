from rest_framework import mixins, viewsets, status
from .serializers import UsersDetailsSerializer, CustomTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Users
from .permissions import IsAuthorize, IsManagerCrm
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class UsersCreateViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
        Endpoint for create a new management
    """
    queryset = Users.objects.all()

    serializer_class = UsersDetailsSerializer
    permission_classes = [IsAuthorize, IsManagerCrm]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, pk=None, *args, **kwargs):
        user = get_object_or_404(self.queryset, pk=pk)
        if user is None:
            return Response({'error', 'user not  exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UsersDetailsSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        user = get_object_or_404(self.queryset, pk=pk)
        user.delete()
        return Response(data={'response': 'user deleted'}, status=status.HTTP_201_CREATED)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UsersListViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
           Endpoint for list all the users of the app. User must be authenticated
    """
    queryset = Users.objects.all()

    serializer_class = UserSerializer

    permission_classes = [IsAuthorize, IsManagerCrm]
