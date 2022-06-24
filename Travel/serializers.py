from multiprocessing import context
from django.db import transaction
from django.urls import reverse
from rest_framework import serializers, status
from .models import *
from rest_framework.exceptions import APIException

class ClientException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST



class LocationSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="location-crud", lookup_field="pk")
    class Meta:
        model = Location
        fields = [
            "url",
            "id",
            "state",
            "address",
            "city",  
        ]
        extra_kwargs = {"id":{
                "read_only":True
                }
            }

    def validate(self, attrs):
        ''
        for value in attrs:
            attrs[value] = attrs[value].title()
            
        
        print(attrs)
        return super().validate(attrs)

    def create(self, validated_data):
        print("In Locat")
        if self.context.get("no-create"):
            return validated_data

        try:
            return super().create(validated_data)
        except Exception as e:
            raise ClientException(e)

        
    

class TransportPriceReadSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    from_location = LocationSerializer()
    to_location = LocationSerializer()
    
    class Meta:
        model = TransportPrice
        fields = "__all__"

        extra_kwargs = {
            "company":{
                "read_only":True
            }
        }
    def get_company(self, obj):
        return obj.company.name



    def update(self, instance, validated_data):
        
        company = self.context.get("company")
        
   
        if "from_location" in validated_data:
            from_location = validated_data.get("from_location", None)
            from_loc = Location.objects.get_or_create(
            state=from_location["state"], city=from_location["city"], address=from_location["address"])
            print(from_loc)
            instance.from_location_id=from_loc[0].id
        if "to_location" in validated_data:
            to_location = validated_data.get("to_location", None)

            to_loc = Location.objects.get_or_create( 
            state=to_location["state"], city=to_location["city"], address=to_location["address"]) 
            instance.to_location_id = to_loc[0].id
        if "car_type" in validated_data:
            instance.car_type = validated_data.get("car_type",None)
        if "price" in validated_data:
            instance.price = validated_data.get("price",None)
        print(validated_data.keys())
        
        
        return instance


class TransportPriceCreateSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    from_location = LocationSerializer()
    to_location = LocationSerializer()
    
    class Meta:
        model = TransportPrice
        fields = ["url",
                    "id",
                "company",
                "from_location",
                "to_location",
                "car_type",
                "price"
                ]
        
        '''extra_kwargs = {
            "car_type":{
                "read_only":True
            },
            "to_location":{
                "read_only":True
            },
            "from_location":{
                "read_only":True
            },
            "company":{
                "read_only":True
            }
        }'''
    def get_url(self, obj):
        request = self.context.get("request")
        scheme = request.is_secure() and "https" or "http"
        return f'{scheme}://{request.get_host()}'+reverse("price-crud", kwargs={"company_id":obj.company.id, "price_id":obj.id})

    
    def get_company(self, obj):
        return obj.company.name
    
    def create(self, validated_data):
        company = self.context.get("company")
        
        validated_from_location = validated_data.pop("from_location")
        validated_to_location = validated_data.pop("to_location")

        #from_loc = LocationSerializer(data = validated_from_location, context={"no-create":True})
        #to_loc = LocationSerializer(data=validated_to_location)
        with transaction.atomic():
            from_loc = Location.objects.get_or_create(**validated_from_location)
            to_loc = Location.objects.get_or_create(**validated_to_location)
            if from_loc[0] not in company.park.all():
                company.park.add(from_loc[0])
            if to_loc not in company.park.all():
                company.park.add(to_loc[0])
            company.save()
            #company = TransportCompany.objects.get()

            price = TransportPrice.objects.get_or_create(
                **validated_data,
                from_location_id=from_loc[0].id,
                to_location_id=to_loc[0].id,
                company_id=company.id
            )
        if price[1]:
            return price[0]
        return price[0]



class TransportCompanyWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransportCompany
        fields = [
                "name",
                "park",
                "lugage_policy",
        ]

class TransportCompanyReadSerializer(serializers.ModelSerializer):
    url= serializers.SerializerMethodField()
    park = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = TransportCompany
        fields = ["url",
                "name",
                "park",
                "lugage_policy",
                "review",
                "price",
                "average_rating"
        ]
                        
        extra_kwargs = {
            "review":{"read_only":True},
            "url":{"read_only":True},
            "price":{"read_only":True}
        }

    def get_average_rating(self, obj):
        return obj.average_rating["avg_rating"]


    def get_park(self, obj):
        qs = obj.park.all()
        request = self.context.get("request")
        serializer = LocationSerializer(qs, many=True, context={"request":request}).data
        return serializer

    def get_url(self, obj):
        request = self.context.get("request")
        scheme = request.is_secure() and "https" or "http"
        return f'{scheme}://{request.get_host()}'+reverse("transport-crud", kwargs={"company_id":obj.id})


    def get_review(self, obj):
        request = self.context.get("request")
        qs = obj.review_set.all()
        return ReviewSerializer(qs, many=True, context={"request":request}).data
    
    def get_price(self, obj):
        context = self.context
        qs = obj.transportprice_set.all()
        return TransportPriceReadSerializer(qs, many=True, context=context).data


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionTx
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    author = serializers.PrimaryKeyRelatedField(read_only = True)
    company = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model= Review
        fields = [
            "url",
            "id",
            "author",
            "content",
            "ratings",
            "company",
            "date"
        ]
    def create(self, validated_data):
        validated_data["company"] = self.context["company"]
        return super().create(validated_data)

    def get_url(self, obj):
        request = self.context.get("request")
        scheme = request.is_secure() and "https" or "http"
        return f'{scheme}://{request.get_host()}'+reverse("review-crud", kwargs={"company_id":obj.company.id, "review_id":obj.id})










class TicketListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="ticket")
    #car_type = serializers.SerializerMethodField()
    transport_company = serializers.StringRelatedField()
    from_location = LocationSerializer()
    to_location = LocationSerializer()
    paid = serializers.BooleanField(read_only=True)
    
    
    class Meta:
        model = Ticket
        fields= [
            "url",
            'user',
            "id",
            "date",
            "time",
            "reserved_seats",
            "from_location",
            "to_location",
            "transport_company",
            "car_type",
            "price",
            "paid",
        ]

    def validate(self, attrs):
        company = self.transport_company
        if self.from_location not in company.park.all():
            raise serializers.ValidationError(f"{self.from_location} not in list of {self.transport_company} parks")
        if self.to_location not in company.park.all():
            raise serializers.ValidationError(f"{self.to_location} not in list of {self.transport_company} parks")

        
        return super().validate(attrs)

 



class TicketSerializer(serializers.ModelSerializer):
   
    #transport_company = serializers.StringRelatedField()
    paid = serializers.BooleanField(read_only=True)
    class Meta:
        model = Ticket
        fields= [
            
            "id",
            "date",
            "time",
            "reserved_seats",
            "from_location",
            "to_location",
            "transport_company",
            "car_type",
            "price",
            "paid",
        ]
        

    def create(self, validated_data):
        start = validated_data.get("from_location")
        dest = validated_data.get("to_location")
        car_type = validated_data.get("car_type")
        company = validated_data.get("transport_company")
        per_price = TransportPrice.objects.filter(from_location=start,
        to_location=dest, company=company,car_type=car_type).first().price
        print(per_price)
        validated_data["price"] = validated_data["reserved_seats"] * per_price
        return super().create(validated_data)

    def update(self,instance, validated_data,*args, **kwargs):
        start = validated_data.get("from_location")
        dest = validated_data.get("to_location")
        car_type = validated_data.get("car_type")
        company = validated_data.get("transport_company")
        per_price = TransportPrice.objects.filter(from_location=start,
        to_location=dest, company=company,car_type=car_type).first().price
        
        validated_data["price"] = validated_data["reserved_seats"] * per_price
      
        #per_price = validated_data.get("car_type").price
        instance.price = validated_data["price"]
        return super().update(instance, validated_data)

    def validate(self, attrs):
        transport_company = attrs["transport_company"]
        from_location = attrs["from_location"]
        to_location = attrs["to_location"]
        car_type = attrs["car_type"]

        if from_location not in transport_company.park.all():
            raise serializers.ValidationError(f"{from_location} not in list of {transport_company} parks")
        if to_location not in transport_company.park.all():
            raise serializers.ValidationError(f"{to_location} not in list of {transport_company} parks")
        try:
            transport_company.transportprice_set.get(from_location=from_location,
                                                       to_location=to_location,car_type=car_type)
        except Exception as e:
            print(e)
            raise serializers.ValidationError(f"The {transport_company} price information is not available for trip from {from_location} to {to_location} and car type of {car_type}")
        return super().validate(attrs)


      
'''

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            
            "id",
            "date",
            "time",
            "reserved_seats",
            "from_location",
            "to_location",
            "transport_company",
            "car_type",
            "price",
            "paid",
        ]
    def create(self, validated_data):
        #from_loc_id = validated_data.get("from_location")
        #to_loc_id = validated_data.get("to_location")
         
        return super().create(validated_data)

'''