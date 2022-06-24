
from rest_framework import filters
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from djoser import permissions
from .serializers import *
from rest_framework.views import APIView 
from rest_framework import generics
from rest_framework import authentication, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .models import Ticket
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from djoser.permissions import CurrentUserOrAdminOrReadOnly
from .payment_handler import TicketPayment,verify_transaction
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOnly, IsOwnerOrReadOnly
from rest_framework.decorators import permission_classes
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction
from django.views.decorators.cache import cache_control, cache_page
from .decorators import FilterSearchPaginate
# Create your views here.

params=[openapi.Parameter(name="company_id",
                            required=True,
                            type="integer",
                            in_="path",
                            description="A unique ID identifying the Company")                           
]


params2=[openapi.Parameter(name="id",
                            required=True,
                            type="integer",
                            in_="path",
                            description="A unique ID identifying the Company")                           
]



def index(request):
    return render(request, "index.html")


@FilterSearchPaginate(
             filterset_fields = ["name","park","park__city", "park__state","park__address"]
            ,search_fields=["name","park__city", "park__state","park__address"])
class TransportCompanyCreateApiView(generics.ListCreateAPIView):
    serializer_class = TransportCompanyWriteSerializer
    queryset = TransportCompany.objects.all()
    authentication_classes = [JWTAuthentication, BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "company_id"
    


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
    
    def get_serializer(self, *args, **kwargs):
        if self.request.method == "GET":
            serializer = TransportCompanyReadSerializer
            kwargs.setdefault('context', self.get_serializer_context())
            return serializer(*args,**kwargs)
        return super().get_serializer(*args, **kwargs)
        
    
@method_decorator(name="get", decorator=cache_page(timeout=5))
class TransportCompanyApiView(
    generics.RetrieveUpdateDestroyAPIView
    ):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication, BasicAuthentication, authentication.SessionAuthentication]
    serializer_class = TransportCompanyWriteSerializer
    queryset= TransportCompany.objects.all()


    def get_object(self):
        company_id = self.kwargs.get("company_id")
        try:
            obj = self.get_queryset().get(id = company_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        return obj

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "GET":
            serializer = TransportCompanyReadSerializer
            kwargs.setdefault('context', self.get_serializer_context())
            return serializer(*args,**kwargs)
        return super().get_serializer(*args, **kwargs)


@method_decorator(name="get", decorator=cache_page(timeout=60*5))
class LocationCreateListApiView(generics.ListCreateAPIView):
    permission_classes= [permissions.IsAuthenticatedOrReadOnly,permissions.IsAdminUser]
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["state", "address", "city"]
    search_fields = ["search", "address","fields"]

 
'''
    def get_queryset(self, **kwargs):
        qs = super().get_queryset()
        state = self.request.query_params.get("state")
        city = self.request.query_params.get("city")
        if state:
            qs= qs.filter(state = state)
        if city:
            qs =qs.filter(city=city)
        return city
'''

@method_decorator(name="get", decorator=cache_page(timeout=5))
class LocationApiView(
    generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



@method_decorator(name="get", decorator=cache_page(timeout=60*5))
class ReviewApiView(APIView):
    authentication_classes = [JWTAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer

    @swagger_auto_schema(request_body=ReviewSerializer, operation_description="Create a new Review for the company with id of ID")
    def post(self,request,*args, **kwargs):
        """Creates a new Review per Company"""
        print(request.user)
        company_id = kwargs.get("company_id")
        try:
            company = TransportCompany.objects.get(id=company_id)
        except:
            return Response({"error":f"No Company with the ID {company_id}"}, status=status.HTTP_404_NOT_FOUND)
        print(request.data)
        serializer = ReviewSerializer(data=request.data, context={"company":company})
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data)
    
    def get(self, request, *args, **kwargs):
        """Get the list of the reviews for a Travel Company"""
        queryset = Review.objects.all()
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(name="get", decorator=cache_page(timeout=5))
class ReviewIndividualApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ReviewSerializer
    

    @swagger_auto_schema(responses={200:ReviewSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        review_id = kwargs.get("review_id")
        try:
            review = Review.objects.get(id = review_id)
        except:
            return Response(status= status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(instance=review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema( 
        request_body=ReviewSerializer, responses={200:ReviewSerializer(many=True)})
    def put(self, request, *args, **kwargs):
        review_id = kwargs.get("review_id")
        try:
            review = Review.objects.get(id = review_id)
        except:
            return Response(status= status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(instance=review, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ReviewSerializer)
    def delete(self, request, **kwargs):
        review_id = kwargs.get("review_id")
        try:
            review = Review.objects.get(id = review_id)
        except:
            return Response(status= status.HTTP_404_NOT_FOUND)
        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(     
        request_body=ReviewSerializer,responses={200:ReviewSerializer(many=True)})
    def patch(self, request, **kwargs):
        review_id = kwargs.get("review_id")
        try:
            review = Review.objects.get(id = review_id)
        except:
            return Response(status= status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(instance=review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)



"/transports/ -- all"
"/transports/id -- crud"

@method_decorator(name="get", decorator=cache_page(timeout=5))
class TransportPriceListCreateApiView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication, authentication.SessionAuthentication]
    serializer_class = TransportPriceCreateSerializer
    lookup_field = "company_id"
    queryset = TransportPrice.objects.all()
    

    
    @swagger_auto_schema(responses={200:TransportPriceCreateSerializer})
    def get(self, request, *args, **kwargs):
        "Get the list of transport price for the company with the given ID"
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(request_body=TransportPriceCreateSerializer, responses={200:TransportPriceCreateSerializer})
    def post(self, request, *args, **kwargs):
        "Creates a new transport price for the company with the given ID"

        return super().post(request, *args, **kwargs)

    
    def get_queryset(self, **kwargs):
        qs = super().get_queryset()
        company_id = self.kwargs.get(self.lookup_field)
        queryset = qs.filter(company_id  = company_id)        
        return queryset

    def get_serializer_context(self):
        company_id = self.kwargs.get(self.lookup_field)
        context =  super().get_serializer_context()
        company = TransportCompany.objects.get(id = company_id)
        context["company"] = company
        return context

    
@method_decorator(name="get", decorator=cache_page(timeout=5))
@method_decorator(name="get", decorator=swagger_auto_schema( responses={200:TransportPriceReadSerializer(many=True)}))
@method_decorator(name="put", decorator=swagger_auto_schema(request_body=TransportPriceReadSerializer))
@method_decorator(name="patch", decorator=swagger_auto_schema(request_body=TransportPriceReadSerializer))
@method_decorator(name="delete", decorator=swagger_auto_schema())
class TransportPriceApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication, authentication.SessionAuthentication]
    serializer_class = TransportPriceReadSerializer
    queryset = TransportPrice.objects.all()
    lookup_field = "price_id"
    
    def get_object(self):
        price_id = self.kwargs["price_id"]
        print(self.kwargs, "\n\n\n")
        try:
            obj = self.get_queryset().get(id =price_id)
        except:
        
            return Response(status=status.HTTP_404_NOT_FOUND)
        return obj



    def get_serializer_context(self, **kwargs):
        company_id = self.kwargs.get("company_id")
        print(self.kwargs, self.lookup_url_kwarg)
        context =  super().get_serializer_context()
        company = TransportCompany.objects.get(id = company_id)
        context["company"] = company
        return context

@method_decorator(name="get", decorator=cache_page(timeout=60*5))
class TicketApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketSerializer
    query_set = Ticket.objects.all()
    lookup_field = "pk" 

    @swagger_auto_schema( responses={200:TicketSerializer})
    def get(self, *args, **kwargs):

        pk = kwargs.get("pk")
        try:
            qs = Ticket.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        serializer = TicketListSerializer(instance=qs, context ={"request":self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=TicketSerializer, responses={202:TicketSerializer})
    def put(self, *args, **kwargs):
        

        pk = kwargs.get("pk")
        try:
            qs = Ticket.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TicketSerializer(instance=qs, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        try:
            qs = Ticket.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
@method_decorator(name="get", decorator=cache_page(timeout=60*5))
class TicketCreateView(generics.CreateAPIView, generics.ListAPIView):
    authentication_classes = [JWTAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    
    def get_serializer_class(self):
        
        if self.request.method == "GET":
            return TicketListSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        if serializer.is_valid(raise_exception = True):
            if self.request.user.is_authenticated:
                print(self.request.user)
                serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def dispatch(self, request, *args, **kwargs):
        print(args, kwargs)
        response = super().dispatch(request, *args, **kwargs)
        if request.method == "POST":
            url = request.build_absolute_uri(reverse("ticket", kwargs = {"pk":response.data.get("id")}))
            payment_url = request.build_absolute_uri(reverse("ticket-payment", kwargs = {"pk":response.data.get("id")}))
            response.data["Payment Link"] = payment_url
            response.headers["Location"] = url

        return response

@api_view(http_method_names=["GET"])
@swagger_auto_schema(responses={200:{
  "status": "success",
  "message": "Hosted Link",
  "data": {
    "link": "https://api.flutterwave.com/v3/hosted/pay/f524c1196ffda5556341"
  }
}})
@permission_classes([IsOwnerOnly])
def pay_for_ticket(request, pk=None, *args, **kwargs):
    "API Endpoint to get flutterwave payment page for ticket"
    ticket = Ticket.objects.get(id =pk)
    if ticket.paid:
        return Response({"message":"You have paid for this ticket"})
    pay = TicketPayment(ticket=ticket, request=request)
    #return redirect(pay.link)
    #data = json.dumps(pay.response.data)
    print()
    return Response(status=status.HTTP_200_OK, data=pay.response)
    #return Response( status=status.HTTP_200_OK)


@api_view(["GET"])
@swagger_auto_schema(auto_schema=None)
def payment_verify(request, pk, *args, **kwargs):
    with transaction.atomic():
        ticket = Ticket.objects.get(id =pk)
        if verify_transaction(request, ticket):
            
            ticket.paid = True
            ticket.save()
            serializer = TicketSerializer(instance=ticket)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
