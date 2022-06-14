
from django.urls import reverse
from rest_framework import serializers, status
from .models import *
from rest_framework.exceptions import APIException
        
class ClientException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

class TransportCompanySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='transport-crud', lookup_field = "pk")
    review = serializers.SerializerMethodField()
    class Meta:
        model = TransportCompany
        fields = ["url",

                "name",
                "park",
                "lugage_policy",
                "review"
        ]
                        
        extra_kwargs = {
            "review":{"read_only":True},
            "url":{"read_only":True}
        }

    def get_park(self, obj):
        qs = obj.location.all()
        return LocationSerializer(qs, many=True).data


    def get_review(self, obj):
        qs = obj.review_set.all()
        print( ReviewSerializer(qs, many=True).data)
        return ReviewSerializer(qs, many=True).data
    

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
        return reverse("price-crud", kwargs={"id":obj.id, "pk":obj.company.pk})
    def get_company(self, obj):
        return obj.company.name
    
    def create(self, validated_data):
        company = self.context.get("company")
        
        validated_from_location = validated_data.pop("from_location")
        validated_to_location = validated_data.pop("to_location")

        #from_loc = LocationSerializer(data = validated_from_location, context={"no-create":True})
        #to_loc = LocationSerializer(data=validated_to_location)
        print(validated_from_location)
        from_loc = Location.objects.get_or_create(**validated_from_location)
        to_loc = Location.objects.get_or_create(**validated_to_location)
        #company = TransportCompany.objects.get()
        print(from_loc, to_loc)
        price = TransportPrice.objects.get_or_create(
            **validated_data,
            from_location_id=from_loc[0].id,
            to_location_id=to_loc[0].id,
            company_id=company.id
        )
        if price[1]:
            return price[0]
        return price[0]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionTx
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only = True)
    company = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model= Review
        fields = [
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








class TicketListSerializer(serializers.ModelSerializer):
    #car_type = serializers.SerializerMethodField()
    transport_company = serializers.StringRelatedField()
    from_location = LocationSerializer()
    to_location = LocationSerializer()
    paid = serializers.BooleanField(read_only=True)
    
    
    class Meta:
        model = Ticket
        fields= [
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