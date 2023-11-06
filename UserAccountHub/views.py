from UserAccountHub.api.serializers import UserSerializer
from UserAccountHub.models import User ,Account


# Create your views here.
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from rest_framework import status

@api_view(["GET"])
def user_list (request):
    if request.method == "GET":
        user =User.objects.all()
        serializer =UserSerializer (user , many=True)

        return Response (serializer.data)

@api_view (["GET"])
def user_detail_view_by_username_or_email(request ,username_or_email):
    if request.method =="GET":
        try:
            try:
                if username_or_email.isdigit():
                    user = User.objects.get(id= username_or_email)
                else :
                    user = User.objects.get(username = username_or_email)
            except :
                user=User.objects.get(email= username_or_email)

        except User.DoesNotExist :
            return Response (status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        return Response(serializer.data)

        
        
