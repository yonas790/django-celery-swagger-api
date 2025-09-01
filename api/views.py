from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .tasks import send_email_notification, process_data_task
import logging

logger = logging.getLogger(__name__)

@swagger_auto_schema(
    method='post',
    operation_description="Send email notification via background task",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['subject', 'message', 'recipients'],
        properties={
            'subject': openapi.Schema(type=openapi.TYPE_STRING, description='Email subject'),
            'message': openapi.Schema(type=openapi.TYPE_STRING, description='Email message'),
            'recipients': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING),
                description='List of recipient emails'
            ),
        },
    ),
    responses={
        200: openapi.Response(
            description="Email task queued successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'task_id': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
        400: openapi.Response(description="Bad request"),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def send_email(request):
    """
    Send email notification using Celery background task
    """
    try:
        subject = request.data.get('subject')
        message = request.data.get('message')
        recipients = request.data.get('recipients', [])
        
        if not all([subject, message, recipients]):
            return Response(
                {'error': 'Subject, message, and recipients are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Queue the email task
        task = send_email_notification.delay(subject, message, recipients)
        
        return Response({
            'message': 'Email task queued successfully',
            'task_id': task.id
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error queuing email task: {e}")
        return Response(
            {'error': 'Failed to queue email task'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@swagger_auto_schema(
    method='post',
    operation_description="Process data via background task",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['data'],
        properties={
            'data': openapi.Schema(type=openapi.TYPE_STRING, description='Data to process'),
        },
    ),
    responses={
        200: openapi.Response(
            description="Data processing task queued successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'task_id': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def process_data(request):
    """
    Process data using Celery background task
    """
    try:
        data = request.data.get('data')
        
        if not data:
            return Response(
                {'error': 'Data is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Queue the processing task
        task = process_data_task.delay(data)
        
        return Response({
            'message': 'Data processing task queued successfully',
            'task_id': task.id
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error queuing processing task: {e}")
        return Response(
            {'error': 'Failed to queue processing task'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@swagger_auto_schema(
    method='get',
    operation_description="Check API health status",
    responses={
        200: openapi.Response(
            description="API is healthy",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint
    """
    return Response({
        'status': 'healthy',
        'message': 'Django Celery API is running'
    }, status=status.HTTP_200_OK)
