
from django.contrib import admin
import djoser.urls
from django.urls import path, include, re_path
from Travel.views import *
from account.views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path('auth/', include('djoser.urls.authtoken')),
    path("otp/<str:phone_number>/", OTPAPIView.as_view(), name="otp"),


    path("tickets/", TicketCreateView.as_view(), name= "ticket-create"),
    path("tickets/<int:pk>/", TicketApiView.as_view(), name = "ticket"),
    path("tickets/<int:pk>/pay/",  pay_for_ticket, name = "ticket-payment"),
    path("tickets/<int:pk>/payment-verify/", payment_verify,name = "ticket-payment-verify"),

    path("companies/", TransportCompanyCreateApiView.as_view(), name="transport_create"),
    path("companies/<int:pk>/", TransportCompanyApiView.as_view(), name="transport-crud"),
    path("companies/<int:pk>/reviews/", ReviewApiView.as_view(), name="review"),
    path("companies/<int:pk>/prices/", TransportPriceListCreateApiView.as_view(), name="price"),
    path("companies/<int:pk>/prices/<int:id>/", TransportPriceApiView.as_view(), name="price-crud"),
    path("companies/<int:pk>/reviews/", ReviewApiView.as_view(), name="review-create"),
    path("companies/<int:pk>/reviews/<int:id>/", ReviewIndividualApiView.as_view(), name="review-crud"),

    
    path("locations/", LocationCreateListApiView.as_view(), name="location-create-list"),
    path("locations/<int:pk>/", LocationApiView.as_view(), name="location-crud")


]   

