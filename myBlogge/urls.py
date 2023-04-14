from django.contrib import admin
from django.urls import path
from bloogger.views import *

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",HomeView.as_view(),name="home"),
    path("singup/",SingUp.as_view(),name="singup"),
    path("create/admin/",AdminView.as_view(),name="admin_singup"),
    path("create/private/",PrivateView.as_view(),name="private_singup"),
    path("create/public/",PublicView.as_view(),name="public_singup"),
    path("create/post/",postCreate,name="postCreate"),
    path("login/",LoginView.as_view(),name="login"),
    path("logout/",LinOut.as_view(),name="logout"),
    path("create/category/",categoryView,name="category"),
    path("/single/post/<int:id>/",singleView,name="singleView"),
    path("search/post/",search,name="search")
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
