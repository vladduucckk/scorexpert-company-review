from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.db.models import Avg, IntegerField
from django.db.models.functions import Cast
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from company_reviews import settings
from .filters import ReviewFilter
from .models import Company, Category, Review
from .forms import CompanyForm, FeedbackForm, ReviewForm, CompanyFormUpdate
from .serializers import ReviewSerializer


def home(request):
    """Обробник домашньої сторінки"""
    electronics_data = Company.objects.filter(cat__name="Electronics & Technology").count()
    business_data = Company.objects.filter(cat__name="Business Services").count()
    vehicles_data = Company.objects.filter(cat__name="Vehicles & Transportation").count()
    edu_data = Company.objects.filter(cat__name="Education & Training").count()
    fashion_data = Company.objects.filter(cat__name="Shopping & Fashion").count()
    return render(request, 'home.html', context={'electronics_data': electronics_data, 'business_data': business_data,
                                                 'vehicles_data': vehicles_data, 'edu_data': edu_data,
                                                 'fashion_data': fashion_data})


def about(request):
    """Обробник інформаційної сторінки"""
    return render(request, 'about.html')


@login_required(login_url='login')
def my_companies(request):
    """Обробник власних компаній користувача"""
    data = Company.objects.filter(user=request.user)
    if data.count() > 0:
        return render(request, 'my_companies.html', {'data': data})
    else:
        text = "You don’t have any created companies"
        return render(request, 'my_companies.html', {'text': text})


def all_companies(request):
    """Обробник всих компаній"""
    search = request.GET.get('search')
    if search is None:
        data = Company.objects.all()
        return render(request, 'all_companies.html', context={'data': data})
    else:
        data = Company.objects.filter(name__icontains=search)
        if data.count() > 0:
            return render(request, 'all_companies.html', context={'data': data})
        else:
            text = "Nothing found"
            return render(request, 'all_companies.html', context={'text': text})


def feedback(request):
    """Обробник форми для відгука"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = "Thank you for your feedback!"
            message = "We have received your message and will respond shortly."
            from_email = settings.EMAIL_HOST_USER
            recipient_list = email
            send_mail(subject=subject, message=message, from_email=from_email, recipient_list=[recipient_list])
            form.save()
            return redirect('home')
        else:
            errors = form.errors
            return render(request, 'feedback.html', context={'form': form, 'errors': errors})
    else:
        form = FeedbackForm()
        return render(request, 'feedback.html', context={'form': form})


@login_required(login_url='login')
def add_company(request):
    """Обробник форми для створення запису в БД(нова компанія)"""
    form = CompanyForm()
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            errors = form.errors
            return render(request, 'add_company.html', {'form': form, 'errors': errors})
    else:
        return render(request, 'add_company.html', {'form': form})


def categories(request):
    """Обробник категорій"""
    return render(request, 'category.html')


def category(request, category_name):
    """Обробник для категорії"""
    if category_name == "tech":
        data = Company.objects.filter(cat__name="Electronics & Technology")
        return render(request, 'data_category.html',
                      context={"cat": "Electronics & Technology", "data": data})
    elif category_name == "business":
        data = Company.objects.filter(cat__name="Business Services")
        return render(request, 'data_category.html', context={"cat": "Business Services", "data": data})
    elif category_name == "science":
        data = Company.objects.filter(cat__name="Education & Training")
        return render(request, 'data_category.html', context={"cat": "Education & Training", "data": data})
    elif category_name == "transportation":
        data = Company.objects.filter(cat__name="Vehicles & Transportation")
        return render(request, 'data_category.html', context={"cat": "Vehicles & Transportation", "data": data})
    elif category_name == "fashion":
        data = Company.objects.filter(cat__name="Shopping & Fashion")
        return render(request, 'data_category.html', context={"cat": "Shopping & Fashion", "data": data})
    else:
        raise Http404("Page not found")


@login_required(login_url='login')
def company(request, company_name):
    """Обробник для компанії(відгуки та повна інформація)"""
    company_get = get_object_or_404(Company, name=company_name)
    details_review = Review.objects.filter(company__name=company_name)
    total_review = Review.objects.filter(company__name=company_name).count()
    avg_mark = Review.objects.filter(company__name=company_name).aggregate(avg=Avg(Cast("mark", IntegerField())))
    review1 = Review.objects.filter(company__name=company_name, mark="1").count()
    review2 = Review.objects.filter(company__name=company_name, mark="2").count()
    review3 = Review.objects.filter(company__name=company_name, mark="3").count()
    review4 = Review.objects.filter(company__name=company_name, mark="4").count()
    review5 = Review.objects.filter(company__name=company_name, mark="5").count()

    if request.method == 'POST':
        form = ReviewForm(request.POST, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.company = company_get
            instance.save()
            return redirect('company', company_name=company_get.name)

    else:
        details_company = Company.objects.filter(name=company_name)
        form = ReviewForm()
        return render(request, 'company.html',
                      context={"company_name": company_name, "details_company": details_company, "form": form,
                               "details_review": details_review, 'total_review': total_review, "review1": review1,
                               "review2": review2,
                               "review3": review3, "review4": review4, "review5": review5, "avg_mark": avg_mark})


@login_required(login_url='login')
def update_company(request, company_name):
    """Обробник для оновлення запису в БД(Оновлення інформації про компанію)"""
    get_company = get_object_or_404(Company, name=company_name)
    if get_company.user == request.user:
        if request.method == 'POST':
            form = CompanyFormUpdate(request.POST, instance=get_company)
            if form.is_valid():
                form.save()
                messages.success(request, 'Company updated successfully!')
                return redirect('my_companies')
        else:
            form = CompanyFormUpdate(instance=get_company)
            return render(request, "update_company.html", context={"form": form, "company_name": company_name})
    else:
        messages.error(request, "You can’t edit a company created by someone else")
        return redirect('my_companies')


@login_required(login_url='login')
def delete_company(request, company_name):
    """Обробник для видалення компанії"""
    company_get = get_object_or_404(Company, name=company_name)
    if company_get.user == request.user:
        if request.method == 'POST':
            company_get.delete()
            messages.success(request, 'Company deleted successfully!')
            return redirect('my_companies')
        return render(request, 'delete_company.html', context={"company_name": company_name})
    else:
        messages.error(request, "You can’t delete a company created by someone else")
        return redirect('my_companies')


def register(request):
    """Обробник для реєстрації користувача"""
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!')
            return redirect("login")
        else:
            errors = form.errors
            return render(request, 'register.html', context={'form': form, 'errors': errors})
    else:
        form = UserCreationForm()
        return render(request, "register.html", context={"form": form})


def login_user(request):
    """Обробник для авторизації"""
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            error = form.errors
            return render(request, 'login.html', context={'form': form, 'errors': error})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', context={'form': form})


def logout_user(request):
    """Обробник для завершення сессії"""
    logout(request)
    return redirect('login')


def api_docs(request):
    """Обробник для технічної документації по API"""
    return render(request, 'api_docs.html')


class ReviewApiList(ListAPIView):
    """Ендпоїнт для отримання всіх записів з відгуками"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ReviewFilter
    ordering_fields = ('mark',)
    permission_classes = (AllowAny,)


class CompanyApiRetrieve(RetrieveAPIView):
    """Ендпоїнт для отримання одного запису з данними про компанію"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        company_name = self.kwargs.get('company_name')
        instance = Review.objects.filter(company__name=company_name)
        if instance.count() == 0:
            raise NotFound("The company does not exist or has no reviews")
        else:
            instance_avg = instance.aggregate(avg=Avg(Cast("mark", IntegerField())))
            instance_count = instance.count()

            data = {"company_name": company_name, "average_mark": round(instance_avg["avg"], 2),
                    'total_reviews': instance_count}
            return Response(data)
