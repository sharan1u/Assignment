from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from requests.exceptions import RetryError
from rest_framework import status
from rest_framework.views import APIView

from server.services import CustomRetry, make_request


class InitiateRequestView(APIView):
    """
    class to initiate the request to trigger an external api call 
    """
    EXCEPTION_STATUS_CODES = [500, 502, 503]
    BACKOFF_FACTOR = 0.1
    TOTAL_RETRY_ATTEMPTS = 5
    
    def __init__(self, *args, **kwargs):
        super(InitiateRequestView, self).__init__(*args, **kwargs)
        self.external_endpoint = settings.EXTERNAL_API_MAP.get('500')
    
    def get(self, request):
        """
        post method to capture the client request
        """
        json_response = {'message': 'success'}
        try:
            retries = CustomRetry(total=self.TOTAL_RETRY_ATTEMPTS,
                                  backoff_factor=self.BACKOFF_FACTOR,
                                  status_forcelist=self.EXCEPTION_STATUS_CODES)
            make_request(url=self.external_endpoint, retries=retries)
            return JsonResponse(json_response, status=status.HTTP_200_OK)
        except RetryError:
            print(f'Maximum attempts for retries exceeded ')
            json_response['message'] = 'retry limit exceeded'
            return JsonResponse(json_response, status=status.HTTP_408_REQUEST_TIMEOUT)
        except Exception as e:
            print(f'Something went wrong {e}')
            json_response['message'] = 'Something went wrong'
            return JsonResponse(json_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


