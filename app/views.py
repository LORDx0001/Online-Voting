from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Voter, Election, Candidate, Vote
from .serializers import VoterCreateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import VoterCreateSerializer, VoterUpdateSerializer, VoterLoginSerializer
from .models import Voter
from rest_framework_simplejwt.tokens import RefreshToken


# @swagger_auto_schema(method='post', responses={200: VoterCreateSerializer(many=True)}, request_body=VoterCreateSerializer)
# @api_view(['POST'])
# def voter_create(request):
#     data = request.data
#     serializer = VoterCreateSerializer(data=data)
#     if serializer.is_valid():
#         voter = serializer.save()
#         voter.password = make_password(data['password'])
#         voter.save()
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)

@swagger_auto_schema(
    method='POST',
    request_body=VoterCreateSerializer,
    responses={201: VoterCreateSerializer}
)
@api_view(['POST'])
def create_voter(request):
    data = request.data
    serializer = VoterCreateSerializer(data=data)
    if serializer.is_valid():
        voter = serializer.save()
        voter.password = make_password(data['password'])
        voter.save()
        return Response({"message": "Voter create"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='PUT',
    request_body=VoterUpdateSerializer,
    responses={200: VoterUpdateSerializer}
)
@api_view(['PUT'])
def update_voter(request, pk):
    voter_instance = get_object_or_404(Voter, pk=pk)
    serializer = VoterUpdateSerializer(instance=voter_instance, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'message': "Changed "}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='POST',
    request_body=VoterLoginSerializer,
    responses={200: "Token created successfully", 401: "Unauthorized"}
)
@api_view(['POST'])
def voter_login(request):
    serializer = VoterLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        voter = Voter.objects.filter(username=username).first()
        if not voter or not voter.check_password(serializer.validated_data['password']):
            return Response({'error': 'Voter not found or incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(voter)
        access = refresh.access_token
        access['full_name'] = getattr(voter, 'full_name', None)
        return Response({
            'access_token': str(access),
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)