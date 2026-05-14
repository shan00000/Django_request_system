from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.views import generic
# Create your views here.


# @login_required
# def dashboard(request):
#     return HttpResponse("Welcome to the dashboard! This is where you can view and manage your requests.")



from .models import SoftwareRequest


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "requests/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_year = self.request.GET.get("year")

        software_requests = SoftwareRequest.objects.filter(
            requested_by=self.request.user
        )

        if selected_year:
            software_requests = software_requests.filter(
                start_date__year=selected_year
            )

        context["software_requests"] = software_requests
        context["selected_year"] = selected_year

        return context

class RequestDetailView(LoginRequiredMixin, generic.DetailView):
    model = SoftwareRequest
    template_name = "requests/request_detail.html"
    context_object_name = "software_request"

    def get_queryset(self):
        return SoftwareRequest.objects.filter(requested_by=self.request.user)
    
def logout_view(request):
    logout(request)
    return redirect("accounts:login")