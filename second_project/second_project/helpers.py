from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.crypto import get_random_string
import hashlib

def pg_records(request, allRecords, recordsPerPage):
	paginator = Paginator(allRecords, recordsPerPage)
	pageRequested = request.GET.get('page')

	try:
		# create Page object for the given page
		records = paginator.page(pageRequested)
	except PageNotAnInteger:
		# if page parameter in the query string is not available, return the first page
		records = paginator.page(1)
	except EmptyPage:
		# if the value of the page parameter exceeds num_pages then return the last page
		records = paginator.page(paginator.num_pages)

	return records


def generate_activation_key(username):
	chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-='
	secret_key = get_random_string(20, chars)
	return hashlib.sha256((secret_key + username).encode('utf-8')).hexdigest()