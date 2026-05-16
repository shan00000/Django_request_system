from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.views import generic
from .models import SoftwareRequest, RequestCycle
from django.utils import timezone
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
                created_at__year=selected_year
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        active_cycle = RequestCycle.objects.filter(is_active=True).first()
        software_request = self.object
        current_year = timezone.now().year

        context["active_cycle"] = active_cycle
        context["can_edit"] = (
            active_cycle is not None
            and software_request.created_at.year == current_year
            and software_request.status == "submitted"
        )

        return context
    
class EditRequestView(LoginRequiredMixin, generic.TemplateView):
    template_name = "requests/edit_request.html"

    def get(self, request, pk):
        software_request = SoftwareRequest.objects.get(pk=pk, requested_by=request.user)
        active_cycle = RequestCycle.objects.filter(is_active=True).first()

        if not active_cycle or software_request.created_at.year != timezone.now().year or software_request.status != "submitted":
            return redirect("requests:request_detail", pk=pk)

        return render(request, self.template_name, {"software_request": software_request})

    def post(self, request, pk):
        software_request = SoftwareRequest.objects.get(pk=pk, requested_by=request.user)
        active_cycle = RequestCycle.objects.filter(is_active=True).first()

        if not active_cycle or software_request.created_at.year != timezone.now().year or software_request.status != "submitted":
            return redirect("requests:request_detail", pk=pk)

        software_request.application_name = request.POST.get("application_name")
        software_request.application_description = request.POST.get("application_description")
        software_request.application_website = request.POST.get("application_website")
        software_request.purchase_required = request.POST.get("purchase_required") == "on"
        software_request.need_virtual_desktop = request.POST.get("need_virtual_desktop") == "on"
        software_request.alternative_software_has_been_considered = request.POST.get("alternative_software_has_been_considered") == "on"
        software_request.license_agreement_detail = request.POST.get("license_agreement_detail")
        software_request.privacy_considered = request.POST.get("privacy_considered") == "on"
        software_request.primary_use = request.POST.get("primary_use")
        software_request.need_installing_on = request.POST.get("need_installing_on")
        software_request.need_staff_machine = request.POST.get("need_staff_machine") == "on"
        software_request.anything_else = request.POST.get("anything_else")
        software_request.start_date = request.POST.get("start_date")

        software_request.save()

        return redirect("requests:request_detail", pk=pk)


class NewRequestView(LoginRequiredMixin, generic.TemplateView):
    template_name = "requests/new_request.html"

    def get(self, request):
        active_cycle = RequestCycle.objects.filter(is_active=True).first()

        return render(request, self.template_name, {"active_cycle": active_cycle})

    def post(self, request):
        active_cycle = RequestCycle.objects.filter(is_active=True).first()

        if not active_cycle:
            return render(request, self.template_name, {
                "active_cycle": active_cycle,
                "error_message": "Request period is currently closed."
            })

        SoftwareRequest.objects.create(
            requested_by=request.user,
            application_name=request.POST.get("application_name"),
            application_description=request.POST.get("application_description"),
            application_website=request.POST.get("application_website"),
            purchase_required=request.POST.get("purchase_required") == "on",
            need_virtual_desktop=request.POST.get("need_virtual_desktop") == "on",
            alternative_software_has_been_considered=request.POST.get("alternative_software_has_been_considered") == "on",
            license_agreement_detail=request.POST.get("license_agreement_detail"),
            privacy_considered=request.POST.get("privacy_considered") == "on",
            primary_use=request.POST.get("primary_use"),
            need_installing_on=request.POST.get("need_installing_on"),
            need_staff_machine=request.POST.get("need_staff_machine") == "on",
            anything_else=request.POST.get("anything_else"),
            start_date=request.POST.get("start_date"),
        )

        return redirect("requests:dashboard")


def renew_request_view(request, pk):
    old_request = SoftwareRequest.objects.get(
        pk=pk,
        requested_by=request.user
    )

    active_cycle = RequestCycle.objects.filter(is_active=True).first()

    if not active_cycle:
        return redirect("requests:request_detail", pk=pk)

    already_renewed = SoftwareRequest.objects.filter(
        requested_by=request.user,
        application_name=old_request.application_name,
        created_at__year=timezone.now().year
    ).exists()

    if already_renewed:
        return redirect("requests:request_detail", pk=pk)

    new_request = SoftwareRequest.objects.create(
        requested_by=request.user,
        application_name=old_request.application_name,
        application_description=old_request.application_description,
        application_website=old_request.application_website,
        purchase_required=old_request.purchase_required,
        need_virtual_desktop=old_request.need_virtual_desktop,
        alternative_software_has_been_considered=old_request.alternative_software_has_been_considered,
        license_agreement_detail=old_request.license_agreement_detail,
        privacy_considered=old_request.privacy_considered,
        primary_use=old_request.primary_use,
        need_installing_on=old_request.need_installing_on,
        need_staff_machine=old_request.need_staff_machine,
        anything_else=old_request.anything_else,
        start_date=old_request.start_date,
    )

    return redirect("requests:dashboard")

    
def logout_view(request):
    logout(request)
    return redirect("accounts:login")