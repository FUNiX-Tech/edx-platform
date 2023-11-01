
from .models import ToggleFeatureCourse


def featureCourse(course_id):
    feature_course = ToggleFeatureCourse.findCourseToggeFeature(course_id=course_id)
    results = []

    if feature_course:
        if feature_course[0].is_discussion:
            results.append('discussion')
        if feature_course[0].is_chatGPT:
            results.append('chatGPT')
        if feature_course[0].is_feedback:
            results.append('feedback')
        if feature_course[0].is_search:
            results.append('search')
        if feature_course[0].is_date_and_progress:
            results.append('dates')
    else:
        results = ['discussion', 'chatGPT', 'feedback', 'search', 'dates']

    return results