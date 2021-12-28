from datetime import timedelta

from lms.djangoapps.courseware.courses import funix_get_assginment_date_blocks, get_course_with_access
from common.djangoapps.student.models import get_user_by_username_or_email
from openedx.features.funix_relative_date.models import FunixRelativeDate, FunixRelativeDateDAO
from opaque_keys.edx.keys import CourseKey

class FunixRelativeDateLibary():
	@classmethod
	def _get_last_complete_assignment(self, assignment_blocks):
		return next((asm for asm in assignment_blocks[::-1] if asm.complete), None)

	@classmethod
	def get_schedule(self, user_name, course_id):
		user = get_user_by_username_or_email(user_name)
		course_key = CourseKey.from_string(course_id)
		course = get_course_with_access(user, 'load', course_key=course_key, check_if_enrolled=False)
		assignment_blocks = funix_get_assginment_date_blocks(course=course, user=user, request=None, include_past_dates=True)

		last_complete_date = FunixRelativeDateDAO.get_enroll_by_id(user_id=user.id, course_id=course_id).date

		# Delete all old date
		FunixRelativeDateDAO.delete_all_date(user_id=user.id, course_id=course_id)

		index = 0
		completed_assignments = [asm for asm in assignment_blocks if asm.complete]
		uncompleted_assignments = [asm for asm in assignment_blocks if not asm.complete]

		completed_assignments.sort(key=lambda x: x.complete_date)
		for asm in completed_assignments:
			index += 1
			last_complete_date = asm.complete_date
			FunixRelativeDate(user_id=user.id, course_id=str(course_id), block_id=asm.block_key, type='block', index=index, date=last_complete_date).save()

		for asm in uncompleted_assignments:
			index += 1
			last_complete_date += timedelta(days=1)

			FunixRelativeDate(user_id=user.id, course_id=str(course_id), block_id=asm.block_key, type='block', index=index, date=last_complete_date).save()
