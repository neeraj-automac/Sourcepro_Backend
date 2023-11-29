# custom_exception_handler.py

# from rest_framework.views import exception_handler
#
# def custom_exception_handler(exc, context):
#     response = exception_handler(exc, context)
#     print('response000000000',response)
#
#     if response is not None and response.status_code == 403:
#         # Replace the "detail" message with your custom message
#         response.data = {"status": "unauthorized_user"}
#
#     return response
