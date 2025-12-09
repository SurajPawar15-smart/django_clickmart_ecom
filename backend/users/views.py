from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = UserRegisterSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()

                return Response({
                    "message": "User registered successfully!",
                    "data": UserSerializer(user).data
                }, status=status.HTTP_201_CREATED)

            return Response({
                "status": "error",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated] # checks if the user is authenticated
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# class ProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         serializer = UserSerializer(user)
#         return Response({
#             "message": "User profile fetched successfully",
#             "data": serializer.data
#         }, status=status.HTTP_200_OK)

#     def patch(self, request):
#         user = request.user
#         serializer = UserSerializer(user, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "message": "Profile updated successfully!",
#                 "data": serializer.data
#             }, status=status.HTTP_200_OK)

#         return Response({
#             "status": "error",
#             "errors": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)

