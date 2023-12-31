from UserAccountHub.api.serializers import UserSerializer ,AccountSerializer,Registerationerializer
from UserAccountHub.models import User ,Account, UserStatus ,AccountStatus
from rest_framework.authtoken.models import Token


# Create your views here.
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from rest_framework import status
from django.db import transaction

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

          data ={}
          data["failed"]="no user found"
          return Response (data =data ,status=status.HTTP_200_OK)
        
        serializer = UserSerializer(user)
        print (serializer.data)
        return Response(serializer.data)

        
        
@api_view (["DELETE"])

def delete_users (request):
    users_id =request.data.get('users_id' ,[])
    data={}
    if not users_id:
        return Response ({'error' :'user_id is required'} ,
                         status=status.HTTP_400_BAD_REQUEST)
    
   
    else:
            with transaction.atomic():
                users = User.objects.filter(id__in=users_id)
                # Update status to 'DELETED'
                users.update(status=UserStatus.DELETED)
                data["success"] = "deleted successfully"
                return Response(data=data, status=status.HTTP_204_NO_CONTENT)
    


@api_view(["POST"])

def add_user(request):
    if request.method=="POST":
        serializer = UserSerializer(data =request.data)
        if serializer.is_valid():
            serializer.save()
           
            return Response (serializer.data ,status=status.HTTP_200_OK)
        else :
            return Response (serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
        

@api_view(["PATCH"])

def update_user (request , id):
    try :
        user = User.objects.get(id =id)
        print(user,"User")
        if request.method =="PATCH":
            serializer = UserSerializer (user, data=request.data , partial =True)
        
        if serializer.is_valid():
           
            serializer.save()
           
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else :
            print(serializer.errors)
            return Response(serializer.errors,"errrrror")

    except User.DoesNotExist:
        return Response(status =status.HTTP_404_NOT_FOUND)
    
    






# /////////////////////////////////////////////////////////

@api_view(["GET"])
def accounts_list (request):
    if request.method == "GET":
        account = Account.objects.all()
        serializer = AccountSerializer(account ,many=True)
        return Response (serializer.data ,status = status.HTTP_200_OK)


@api_view (["GET"])

def account_by_id (request,search_query):
    if request.method == "GET":
        
            
                try:
                    
                        
                    
                        account =Account.objects.get(accountNumber=search_query)
                    
                       
                except:
                    try:
                        account = Account.objects.get(id=search_query)
                    except:
                        try:
                            account = Account.objects.get(user_id =search_query)
                        except Account.DoesNotExist:
                                data ={}
                                data["failed"]="no user found"
                                return Response (data =data ,status=status.HTTP_200_OK)
                        
                serializer =AccountSerializer(account)
                return Response(serializer.data)

# /////////////////////////////////////////
# Delete one or more accounts

@api_view(["DELETE"])
def delete_accounts(request ):
    accounts_id=request.data.get("accounts_id" ,[])
    data={}
    if not accounts_id :
        return Response ({"error" : "account_id is required"} ,status=status.HTTP_400_BAD_REQUEST)

    else :
        with transaction.atomic():
            data ={}
            accounts =Account.objects.filter(id__in = accounts_id)
            accounts.update(status=AccountStatus.DELETED)
            data["success"]="Deleted Successfully"
            return Response(data=data, status=status.HTTP_204_NO_CONTENT)


   

# //////////////////////////////////////////////////////
# Add new account 

@api_view(["POST"])

def add_account(request):
    if request.method =="POST":
        serializer = AccountSerializer (data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data ,status=status.HTTP_201_CREATED)
        else :
            return Response (serializer.errors ,status =status.HTTP_400_BAD_REQUEST)
        

# ///////////////////////////////////////////////////////
# Update account 

@api_view (["PATCH"])
def update_account (request ,id):
    
        try:

            print(request.data ,"Data")
            account = Account.objects.get (id=id)
        except Account.DoesNotExist:
            return Response (status=status.HTTP_404_NOT_FOUND)
        if request.method =="PATCH":
            serializer = AccountSerializer(account , request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=status.HTTP_201_CREATED)
            else :
                return Response(serializer.errors)
        
        
@api_view(["POST"])
def registeration_view (request):
     if request.method =="POST":
            print(request.data ,"Data")
            
            serializer = Registerationerializer(data =request.data)
 
            data={}
            if serializer.is_valid():
                print("Serializer is valid")
                print(f"Trying to register with email: {serializer.validated_data['email']}")
                if User.objects.filter(email=serializer.validated_data['email']).exists():
                    data['response'] = 'Email is already in use.'
                    print("Email is already in use")

                else:
                    print(request.data)
                    user = serializer.save()
                    data={}
                    data["response"] = "successfully registerd"
                    data["email"] = user.email
                    data["firstName"] = user.firstName
                    data["status"] = user.status
                    data["lastName"] = user.lastName
                    data["gender"] = user.gender
                    data["date_of_Birth"] = user.date_of_Birth
                    data["username"] = user.username
                    token = Token.objects.get(user=user) if Token.objects.filter(user=user).exists() else None
                    data["token"] = token.key if token else None
                    data["token"] =token
                    
               
            else :
                    print("Serializer is not valid")                 
                    data=serializer.errors
                    print (data)
                    return Response (data)