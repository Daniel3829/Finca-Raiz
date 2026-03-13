from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register, CustomLoginView, dashboard, editar_inmueble, eliminar_inmueble, marcar_vendido, admin_dashboard, eliminar_inmueble_admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("register/", register, name="register"),

    path("login/", CustomLoginView.as_view(), name="login"),

    path(
        "logout/",
        LogoutView.as_view(next_page="/api/inmuebles/lista"),
        name="logout",
    ),

    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
        template_name="usuarios/password_reset.html"
        ),
        name="password_reset"
        ),

        path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
        template_name="usuarios/password_reset_done.html"
        ),
        name="password_reset_done"
        ),

        path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
        template_name="usuarios/password_reset_confirm.html"
        ),
        name="password_reset_confirm"
        ),

        path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
        template_name="usuarios/password_reset_complete.html"
        ),
        name="password_reset_complete"
        ),

    path("dashboard/", dashboard, name="dashboard"),
    path("editar/<int:id>/", editar_inmueble, name="editar_inmueble"),
    path("eliminar/<int:id>/", eliminar_inmueble, name="eliminar_inmueble"),
    path("vendido/<int:id>/", marcar_vendido, name="marcar_vendido"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin/eliminar-inmueble/<int:id>/", eliminar_inmueble_admin, name="eliminar_inmueble_admin"),
]