from django.shortcuts import render
from django.contrib.auth.models import User 
from .serializers import RegisterSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

# Create your views here.

class RegisterApi(CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    
    def post(self, request, *args, **kwargs): # normalde register post edildiğinde user bilgisini tekrar döner, burada biz bunu yerine mesage dönmesini istiyoruz . .o yüzde npost methodunu override ettik
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) #valid değilse hata versin
        ## burada barry hoca ile yaptığımız gibi token üretmemiz lazım
        ## aslında kullandığımız 3rd part auth methodu token üretip siliyor zaten..
        serializer.save()
        return Response({
            "message": "User created successfully..."
        })