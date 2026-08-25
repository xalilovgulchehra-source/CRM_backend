from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == 400:
            detail = response.data
            if isinstance(detail, dict):
                messages = []
                for field, errors in detail.items():
                    if isinstance(errors, list):
                        for error in errors:
                            messages.append(str(error))
                    else:
                        messages.append(str(errors))
                response.data = {
                    "xato": "Validatsiya xatosi",
                    "tafsilotlar": messages,
                }
            elif isinstance(detail, list):
                response.data = {
                    "xato": "Validatsiya xatosi",
                    "tafsilotlar": [str(e) for e in detail],
                }
        elif response.status_code == 401:
            response.data = {"xato": "Avtorizatsiya talab qilinadi"}
        elif response.status_code == 403:
            response.data = {"xato": "Ruxsat etilmagan"}
        elif response.status_code == 404:
            response.data = {"xato": "Topilmadi"}
        elif response.status_code == 405:
            response.data = {"xato": "Ushbu usul ruxsat etilmagan"}
        elif response.status_code >= 500:
            response.data = {"xato": "Ichki server xatosi"}

    return response
