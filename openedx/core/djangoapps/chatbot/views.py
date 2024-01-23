import json
import math
import logging
from django.http import JsonResponse, HttpResponseForbidden
from .models import ChatbotSession, ChatbotQuery, ChatbotError
from .serializer import chatbot_query_list_serializer, chatbot_query_serializer, chatbot_session_list_serializer
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext_lazy as _
import requests
from .api import get_chatbot_bearer_token, get_chatbot_api_url

@require_http_methods('GET')
@login_required
def chatbot_fetch_query_list_view(request, session_id, skip, limit):
    # all = ChatbotQuery.objects.all()
    # for q in all:
    #     if q.status == 'idle' or q.status == 'pending':
    #         q.status = 'failed'
    #         q.save()

    #     if not q.query_msg:
    #         q.delete()


    user = request.user
    
    if session_id == '0':
        last_query = ChatbotQuery.objects.filter(session__student=request.user).last()
        query_list = [] if last_query is None else last_query.session.chatbot_queries.order_by('-id').all()[skip:skip + limit]
        total = 0 if last_query is None else last_query.session.chatbot_queries.count()
        total_page = math.ceil(total/limit)
    else:
        query_list = ChatbotQuery.objects.filter(session__student=user, session__id=session_id).order_by('-id')[skip:skip + limit]
        total = ChatbotQuery.objects.filter(session__student=user, session__id=session_id).count()
        total_page = math.ceil(total / limit)

    remain_page = math.ceil((total - skip - limit)/limit)

    return JsonResponse(
        {
            'message': _('success'),
            'data': {
                'query_list': chatbot_query_list_serializer(query_list),
                'total_page': total_page,
                'remain_page': remain_page,
            }
        }, 
        status=200
    )

@require_http_methods('GET')
@login_required
def chatbot_fetch_session_list_view(request, skip, limit):
    user = request.user

    session_list = ChatbotSession.objects.filter(student=user).order_by('-id').all()[skip:skip + limit]
    total = ChatbotSession.objects.filter(student=user).count()
    total_page = math.ceil(total/limit)
    remain_page = math.ceil((total - skip - limit)/limit)

    return JsonResponse(
        {
            'message': _('success'),
            'data': {
                'session_list': chatbot_session_list_serializer(session_list),
                'total_page': total_page,
                'remain_page': remain_page,
            }
        }, 
        status=200
    )

@require_http_methods(['POST', 'PUT'])
@login_required
def chatbot_query_view(request):
    """
    Create/update query item
    """
    request_data = json.loads(request.body.decode('utf8'))

    query_msg = request_data.get('query_msg')
    session_id = request_data.get('session_id')
    response_msg = request_data.get('response_msg') or ''
    status = request_data.get('status')
    id = request_data.get('id')
    hash = request_data.get('hash')
    error = request_data.get('error')

    if error:
        _save_error(error)

    session = ChatbotSession.objects.filter(id=session_id).last()



    try:
        if request.method == 'POST':
            if not query_msg:
                return JsonResponse(
                    {
                        'message': _('Missing query message.'),
                        'hash': hash
                    }, 
                    status=400
                )
            if session is None: 
                session = ChatbotSession.objects.create(student=request.user)

            query_item = ChatbotQuery.objects.create(session=session, query_msg=query_msg, response_msg=response_msg, status=status)

        if request.method == 'PUT':
            query_item = ChatbotQuery.objects.filter(id=id).first()
            query_item.status = status
            query_item.response_msg = response_msg
            query_item.save()

    except Exception as e:
        logging.error(str(e))
        _save_error(str(e))
        return JsonResponse(
            {
                'message': _('Internal Server Error'),
                'hash': hash
            }, 
            status=500
        )

    return JsonResponse(
        {
            'message': _('success'),
            'data': chatbot_query_serializer(query_item),
            'hash': hash
        }, 
        status=200
    )

@require_http_methods('PUT')
@login_required
def chatbot_vote_response_view(request):
    data = json.loads(request.body.decode('utf8'))

    if data.get('vote') not in ['up', 'down', 'remove']:
        return JsonResponse(
            {
                'message': _('Vote must be "up" or "down" or "remove"')
            },
            status=200
        )
        
    response = ChatbotQuery.objects.filter(id=data.get('query_id')).first()
    if response is None: 
        return JsonResponse(
            {
                'message': _('Not found query response')
            },
            status=400
        )
    if data.get('vote') == 'remove': 
        response.vote = None
        response.feedback = ''
    else:
        response.vote = data.get('vote')

    response.save()

    return JsonResponse(
        {
            'message': _('success'),  
            'data': {
                'vote': data.get('vote'),
                'id': data.get('query_id')
            }
        }
    )
    
@require_http_methods('PUT')
@login_required
def chatbot_give_feedback_view(request):
    data = json.loads(request.body.decode('utf8'))

    feedback = data.get('feedback')
    query_id = data.get('query_id')

    if not feedback or not query_id:
        return JsonResponse(
            {
                'message': _('Missing query_id or feedback.')
            },
            status=400
        )
    
    if len(feedback) > 500:
        return JsonResponse(
            {
                'message': _('Feedback cannot be exceed 500 characters.')
            },
            status=400
        )
        
    response = ChatbotQuery.objects.filter(id=query_id).first()
    if response is None: 
        return JsonResponse(
            {
                'message': _('Not found query response')
            },
            status=400
        )
    
    if response.vote != 'down': 
        return JsonResponse(
            {
                'message': _('The vote is not "down" so cannot give feedback.')
            },
            status=400
        )

    response.feedback = feedback 
    response.save()

    return JsonResponse(
        {
            'message': _('success'),  
            'data': {
                'feedback': feedback,
                'id': query_id
            }
        }
    )

@require_http_methods('POST')
@login_required
def chatbot_start_new_session_view(request):
    try:
        new_session = ChatbotSession.objects.create(student=request.user)
        return JsonResponse(
            {
                'message': _('success'), 
                'data': {
                    'session_id': new_session.session_id
                }
            },
            status=200
        )
    except Exception as e:
        logging.error(str(e))
        return JsonResponse(
            {
                'message': _('Internal Server Error')
            },
            status=500
        )

@require_http_methods('PUT')
@login_required
def chatbot_retry_query_view(request):
    data = json.loads(request.body.decode('utf8'))

    query = ChatbotQuery.objects.filter(id=data.get('query_id')).first()

    if query is None:
        return JsonResponse(
            {
                'message': _('Not found query')
            },
            status=400
        )
    
    if query.status != 'failed':
        return JsonResponse(
            {
                'message': _('You can only retry on failed query')
            },
            status=400
        )
    
    response_msg = _chatbot_get_response(query.query_msg, query.session.id)

    if response_msg is None: 
        return JsonResponse(
            {
                'message': _('Internal Server Error'),
                'data': chatbot_query_serializer(query)
            },
            status=200
        )

    query.status = 'succeeded'
    query.response_msg = response_msg
    query.save()
    return JsonResponse(
        {
            'message': _('success'),
            'data': chatbot_query_serializer(query)
        },
        status=200
    )

@require_http_methods('PUT')
@login_required
def chatbot_cancel_query_view(request):
    data = json.loads(request.body.decode('utf8'))

    query = ChatbotQuery.objects.filter(id=data.get('query_id')).first()

    if query is None:
        return JsonResponse(
            {
                'message': _('Not found query')
            },
            status=400
        )
    
    if query.status != 'pending':
        return JsonResponse(
            {
                'message': _('This query has already finished')
            },
            status=400
        )

    query.status = 'canceled'
    return JsonResponse(
        {
            'message': _('success')
        },
        status=200
    )

# helper function
def _chatbot_get_response(query_msg, session_id):
    url = get_chatbot_api_url()
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {get_chatbot_bearer_token()}'
    }
    data = {
        'query': query_msg,
        'chat_id': session_id
    }

    try:
        r = requests.post(url, headers=headers, data=json.dumps(data))
    except Exception as e: 
        _print_chatbot_error(str(e))
        return None

    if r.status_code == 200:
        return r.json().get('data').get('response')

    else: 
        _print_chatbot_error(f"Response status code: ", r.status_code)
        try:
            _print_chatbot_error("Response error: ", r.json())
        except Exception as e: 
            _print_chatbot_error(str(e))
    
    return None

def _print_chatbot_error(msg):
    error_msg = f"[ CHATBOT_ERROR ]: {msg}"
    print(error_msg)

def _save_error(msg):
    try:
        ChatbotError.objects.create(error_msg=msg)
    except Exception as e:
        _print_chatbot_error(f"Got error when saving ChatbotError: {str(e)}. The error need to be saved: {msg}")