from django.contrib.auth import authenticate, login, logout
from users.models import CustomUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
  
@api_view(['POST'])
def signUpUser(request):
    # Extract data from the request body (no need to manually check POST)
    name = request.data.get("name")
    phone = request.data.get("phone")
    email = request.data.get("email", None)  # Default to None if not provided
    password = request.data.get("password")

    # Validate required fields
    if not name or not phone or not password:
        return Response({"error": "Name, phone number, and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the phone number already exists
    number_exist = CustomUser.objects.filter(phone_number=phone).first()
    if number_exist:
        return Response({"error": "User with the same phone number already exists."}, status=status.HTTP_409_CONFLICT)
    
    # Create the user
    user = CustomUser.objects.create_user(
        name=name,
        phone_number=phone,
        email=email,
        password=password
    )
    user.save()

    # Return success message
    return Response({"message": "User successfully created. Please sign in."}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def loginUser(request):
    phone_number = request.data.get("phone_number")
    password = request.data.get("password")

    # Check if phone_number and password are provided
    if not phone_number or not password:
        return Response({"error": "Phone number and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate the user
    user = authenticate(phone_number=phone_number, password=password)

    if user is not None:
        # Generate JWT tokens (access and refresh)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Return the token in the response
        return Response({
            'message': "Login successful",
            'access_token': access_token,
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
def logoutUser(request):
    # Log out the user (this clears the session data)
    logout(request)
    return Response({"message": "You have been logged out successfully."}, status=200)