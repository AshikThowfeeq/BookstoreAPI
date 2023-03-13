from django.shortcuts import render
from api.serializers import BookSerializer,UserSerializer
from api.models import Books
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions


# authentication and permissions


class BooksView(ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=BookSerializer
    model=Books
    queryset=Books.objects.all()

    # localhost:8000/api/v1/books/genres/

    @action(methods=["GET"],detail=False)
    def genres(self,request,*args,**kwargs):
        qs=Books.objects.all().values_list("genres",flat=True).distinct()
        return Response(data=qs)


    # localhost:8000/api/v1/books?genres=comedy/

    # def list(self, request, *args, **kwargs):
    #     qs=Books.objects.all()
    #     if "genres" in self.request.query_params:
    #         cat=self.request.query_params.get("genres")
    #         qs=qs.filter(genres=cat)
    #     serializer=BookSerializer(qs,many=True)
    #     return Response(data=serializer.data)


    def get_queryset(self):
        qs=Books.objects.all()

        if "genres" in self.request.query_params:
            cat=self.request.query_params.get("genres")
            qs=qs.filter(genres=cat)
            
        if "price_gt" in self.request.query_params:
            price=self.request.query_params.get("price_gt")
            qs=qs.filter(price__gt=price)
        return qs




class UsersView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()

    # def create(self, request, *args, **kwargs):
    #     serializer=UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         usr=User.objects.create_user(**serializer.validated_data)
    #         serializer=UserSerializer(usr,many=False)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)