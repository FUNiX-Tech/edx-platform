def chatbot_query_serializer(query):
    return {
        'id': query.id,
        'session_id': query.session.id,
        'student_id': query.session.student.id,
        'query_msg': query.query_msg,
        'response_msg': query.response_msg,
        'status': query.status,
        'vote': query.vote,
        'created': query.created,
        'feedback': query.feedback,
    }

def chatbot_query_list_serializer(query_list):
    result = []
    for query in query_list: 
        result.append(chatbot_query_serializer(query))
    return result


def chatbot_session_list_serializer(session_list):
    result = []

    for session in session_list: 
        latest_query = session.chatbot_queries.all().order_by('-created').first()
        if not latest_query: 
            session.delete()
        if latest_query:
            result.append(chatbot_query_serializer(latest_query))
    
    return result