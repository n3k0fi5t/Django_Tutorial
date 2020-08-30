from django.shortcuts import render
from django.views.decorators.http import require_GET

from django.conf import settings

ID = settings.VISITOR_SESSION_ID

# Create your views here.
@require_GET
def visit(request):
    rs = request.session

    data = rs.get(ID)
    if not data:
        data = rs[ID] = {'visit_count' : 0}
    data['visit_count'] += 1

    # save data to db
    rs.modified = True

    return render(request, 'base.html', {
        'visit_count' : data['visit_count'],
    })