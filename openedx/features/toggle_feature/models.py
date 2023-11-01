from django.db import models
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview


class ToggleFeatureCourse (models.Model) :
    course = models.ForeignKey(
        CourseOverview,
        db_constraint=False,
        db_index=True,
        on_delete=models.DO_NOTHING,
        unique=True
    )
    is_feedback =  models.BooleanField(default=True, verbose_name='feedback' )
    is_discussion = models.BooleanField(default=True , verbose_name='discussion')
    is_date_and_progress =  models.BooleanField(default=True, verbose_name='date and progress')
    is_search = models.BooleanField(default=True,verbose_name='search')
    is_chatGPT = models.BooleanField(default=True, verbose_name='chatGPT')

    def __str__ (self):

        return f'{self.course_id}'
    
    @classmethod
    def findCourseToggeFeature (self , course_id) :
        try:
            return self.objects.filter(course_id = course_id)
        except:
            return None