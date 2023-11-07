from UserAccountHub.api.serializers import UserSerializer ,AccountSerializer
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
        users=User.objects.filter(id__in= users_id)
        users.delete()
        data["success"]="deleted successful"
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)
    


@api_view(["POST"])

def add_user(request):
    if request.method=="POST":
        serializer = UserSerializer(data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data ,status=status.HTTP_201_CREATED)
        else :
            return Response (serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
        

@api_view(["PATCH"])

def update_user (request , id):
    try :
        user = User.objects.get(id =id)

    except User.DoesNotExist:
        return Response(status =status.HTTP_404_NOT_FOUND)
    
    if request.method =="PATCH":
        serializer = UserSerializer (user, request.data , partial =True)
        data ={}
        if serializer.is_valid():
            serializer.save()
            data["success"]="updated successfully"
            return Response (data =data)
        else :
            return Response(serializer.errors)






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
                                return Response({"error":"Account Does Not Exist"},status =status.HTTP_404_NOT_FOUND)
                         
                serializer =AccountSerializer(account)
                return Response(serializer.data)

# /////////////////////////////////////////
# Delete one or more accounts

@api_view(["DELETE"])
def delete_accounts(request ):
    accounts_id=request.data.get("accounts_id" ,[])
    if not accounts_id :
        return Response ({"error" : "account_id is required"} ,status=status.HTTP_400_BAD_REQUEST)

    else :
        data ={}
        accounts =Account.objects.filter(id__in = accounts_id)
        accounts.delete()
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
        
        
        




