"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from management.views import UsersCreateViewset, UsersListViewset
from event.views import AdminCustomerViewset, AdminContractViewset, AdminEventViewset, AdminNoteViewset
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested import routers



router = routers.SimpleRouter()
router.register('management/create_user', UsersCreateViewset, basename='create-user')
router.register('management/list_users', UsersListViewset, basename='list-users')
router.register('customers', AdminCustomerViewset, basename='customers')
router.register('contracts', AdminContractViewset, basename='contracts')
router.register('events', AdminEventViewset, basename='events')

root_router = routers.NestedSimpleRouter(
    router,
    r'events',
    lookup='event')

root_router.register(
    r'notes',
    AdminNoteViewset,
    basename='notes'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('', include(root_router.urls)),
]
