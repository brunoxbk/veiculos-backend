from django.urls import path
from .views import (
    VeiculoListCreateView,
    VeiculoRetrieveUpdateDestroyView,
    VeiculosStatusView
)

urlpatterns = [
    path('', VeiculoListCreateView.as_view(), name='veiculo-list-create'),
    path('<int:pk>/', VeiculoRetrieveUpdateDestroyView.as_view(), name='veiculo-detail'),
    path('status/', VeiculosStatusView.as_view(), name='veiculo-status'),
]
