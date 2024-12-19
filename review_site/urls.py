from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path

from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="ScoreXpert API",
        default_version='v1',
        description="Detailed documentation of the ScoreXpert API",
        contact=openapi.Contact(email="vladislavmojseev@gmail.com"),
    ),
    public=True,
)

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('feedback/', views.feedback, name='feedback'),
    path('categories/', views.categories, name='categories'),
    path('login/', views.login_user, name='login'),
    path('category/<str:category_name>/', views.category, name='category'),
    path('add-company/', views.add_company, name='add_company'),
    path('company/<str:company_name>/', views.company, name='company'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('all-companies/', views.all_companies, name='all_companies'),
    path('my-companies/', views.my_companies, name='my_companies'),
    path('update-company/<str:company_name>/', views.update_company, name='update_company'),
    path('delete-company/<str:company_name>/', views.delete_company, name='delete_company'),
    path('api/docs/', views.api_docs, name='api_docs'),
    path('api/reviews/', views.ReviewApiList.as_view()),
    path('api/company/<str:company_name>/', views.CompanyApiRetrieve.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),

]
