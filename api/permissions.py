from rest_framework.permissions import BasePermission

class IsOrganizer(BasePermission):
	message = "You must be an organizer to update"
	def has_object_permission(self, request, view, obj):
		if  (obj.organizer == request.user):
			return True
		else:
			return False
