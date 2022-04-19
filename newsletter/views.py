import json 

from .forms import ContactForm
from birdsong.models import Contact
from django.http import request, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        form = ContactForm(data)
        if form.is_valid():
            Contact.objects.get_or_create(email=form.cleaned_data["email"])
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})