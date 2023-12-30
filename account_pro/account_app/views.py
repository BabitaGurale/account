from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Account
from .serializers import AccountSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings

import logging
from django.core.mail import send_mail

error_logger = logging.getLogger('error_logger')
success_logger = logging.getLogger('success_logger')


class AccountApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]    

    def get(self, request):
        try:
            account = Account.objects.all()
            serializer = AccountSerializer(account, many=True)
            success_logger.info('Account fetch successfully')
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error("There is error fetching the account")
            return Response(data={'details':"There is an error fetching the posts"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = AccountSerializer(data=request.data, context={'request':request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            success_logger.info(f'Account with id{serializer.data.get("id")} created successfully')
            send_mail(
                from_email=settings.EMAIL_HOST_USER,
                subject="Account Creation",
                message=f"account created successfully with person id {serializer.data.get('id')}.",
                recipient_list=[request.user.email,],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            error_logger.info(f'Error saving data {serializer.errors}')
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountDetail(APIView):

    def get(self, request, pk):
        try:
            person = Account.objects.get(pk=pk)
            serializer = AccountSerializer(person)
            success_logger.info('account fetch successfully')
            return Response(serializer.data)
        except Exception as e:
            error_logger.error("There is error fetching the person")
            return Response(data={'detail':'Error retriving data'}, status=status.HTTP_400_BAD_REQUEST)



    def put(self, request, pk):
        try:
            person = self.get_object(pk)
            serializer = AccountSerializer(person, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            success_logger.info('Posts fetch successfully')
            return Response(serializer.data)
        except Exception as e:
            error_logger.error("There is error fetching the person")
            return Response(data={'detail':'Error retriving data'}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        account = self.get_object(pk)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    