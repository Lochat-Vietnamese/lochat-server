from rest_framework.response import Response
from rest_framework import status


class BaseResponse:
    @staticmethod
    def success(status_code=status.HTTP_200_OK, message="success", data=None):
        return Response({
            "message": message,
            "data": data
        }, status=status_code, content_type="application/json; charset=utf-8")

    @staticmethod
    def error(status_code=status.HTTP_400_BAD_REQUEST, message="something_went_wrong", data=None):
        return Response({
            "message": message,
            "data": data
        }, status=status_code, content_type="application/json; charset=utf-8")
    
    @staticmethod
    def not_found(status_code=status.HTTP_404_NOT_FOUND, message="not_found", data=None):
        return Response({
            "message": message,
            "data": data
        }, status=status_code, content_type="application/json; charset=utf-8")
    
    @staticmethod
    def internal(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="internal_error", data=None):
        return Response({
            "message": message,
            "data": data
        }, status=status_code, content_type="application/json; charset=utf-8")
    
    @staticmethod
    def custom(status_code: status, message: str, data=None):
        return Response({
            "message": message,
            "data": data
        }, status=status_code, content_type="application/json; charset=utf-8")
