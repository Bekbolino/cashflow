from django.urls import path 
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("control", views.control, name="control"),
    path("delete_item/", views.delete_item, name="delete_item"),
    path("edit/<slug:num>", views.edit, name="edit"),
    path("delete_cashflow", views.delete_cashflow, name="delete_cashflow"),

]
