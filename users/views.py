from django.contrib.auth import authenticate, login, logout
from users.models import CustomUser, PhoneNumber, SpamAction, UserContact
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.db.models import Q
  
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
        # Access token instance
        access_token = refresh.access_token
        access_token.set_exp(lifetime=settings.AUTH_TOKEN_VALIDITY)

        # Return the token in the response
        return Response({
            'message': "Login successful",
            'access_token': str(access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
def logoutUser(request):
    # Log out the user (this clears the session data)
    logout(request)
    return Response({"message": "You have been logged out successfully."}, status=200)


@api_view(['POST'])
def mark_as_spam(request, query):
    if request.user.is_authenticated:
        try:
            # Check if the user has already performed the action
            user = request.user
            # Create PhoneNumber instance if it does not exist
            phone_number_instance, created = PhoneNumber.objects.get_or_create(number=query)

            # Create or get the SpamAction instance for the user and phone number
            spam_action, created = SpamAction.objects.get_or_create(user=user, phone_number=phone_number_instance)
            
            if not spam_action.is_marked_as_spam:
                # Mark the action as performed by the user
                spam_action.is_marked_as_spam = True
                spam_action.save()

            # Get the PhoneNumber instance
            number_object = PhoneNumber.objects.get(number=query)

            # Update the spam likelihood
            number_object.spam_likelihood += 1
            number_object.save()

            return Response({"message": "Phone number is marked as spam!"}, status=status.HTTP_200_OK)
        
        # Handle case where multiple phone number entries are returned
        except PhoneNumber.MultipleObjectsReturned:
            most_spammed_number = PhoneNumber.objects.filter(number=query).order_by('-spam_likelihood').first()
            most_spammed_number.spam_likelihood += 1
            most_spammed_number.save()

            return Response({"message": "Found multiple phone number entries. Marked most-spammed one as spam."}, status=status.HTTP_200_OK)
        
    else:
        return Response({"error": "User not authenticated, please login."}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
def search_person_by_name(request, query):
    try:
        print("search_person_by_name query=",query)
        # Fetch results that start with the query
        starts_with_results = PhoneNumber.objects.filter(Q(name__startswith=query)).values()
        
        # Fetch results that contain the query but do not start with it
        contains_with_results = PhoneNumber.objects.filter(Q(name__icontains=query)).values().exclude(name__istartswith=query)
        
        print(starts_with_results)
        print(contains_with_results)

        # Combine both querysets
        results = list(starts_with_results) + list(contains_with_results)
        
        search_results = []
        for result in results:
            result_info = {
                'name': result['name'],
                'phone_number': result['number'],
                'spam_likelihood': result['spam_likelihood'],
            }
            search_results.append(result_info)

        return Response({'results': search_results}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
