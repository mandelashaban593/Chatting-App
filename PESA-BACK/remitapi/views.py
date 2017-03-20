'''lead generation tool views'''
from django.template import RequestContext
from django.shortcuts import render_to_response
import remitapi.settings as settings
from remitapi.decorators import logged_out_required


@logged_out_required
def render_view(request, template, data):
	'''
	wrapper for rendering views , loads RequestContext
	@request  request object
	@template  string
	@data  tumple
	'''
	template = 'landing/%s' % template
	data['STATIC_URL'] = '%slanding/' % settings.STATIC_URL
	return render_to_response(
	template, data,
	context_instance=RequestContext(request)
	)


def landing_page(request):
	'''
	landing page
	'''
	return 	render_view(
		request,
		'index.html',
		{}
		)
