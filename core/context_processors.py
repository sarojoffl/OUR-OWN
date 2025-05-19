from .models import OrganizationInfo


def organization_info(request):
    org = OrganizationInfo.objects.first()
    return {
        'org': org
    }
