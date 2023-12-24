from vendor.models import Vendor
from django.conf import settings


# context_processors are a module where you can define functions that provide additional context to all templates rendered within your project
def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)


def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}
