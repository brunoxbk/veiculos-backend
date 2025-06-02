from rest_framework import generics
from .models import Veiculo
from .serializers import VeiculoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django_filters import rest_framework as filters


class VeiculoListCreateView(generics.ListCreateAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('marca', 'ano', 'vendido')


class VeiculoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer


class VeiculosStatusView(APIView):
    def get(self, request):
        fabricantes = Veiculo.objects.values('marca').annotate(total=models.Count('id'))
        result_fabricantes = {f['marca']: f['total'] for f in fabricantes}

        uma_semana_atras = timezone.now() - timedelta(days=7)
        ultimos_cadastrados = Veiculo.objects.filter(created__gte=uma_semana_atras)

        class FloorDiv(models.Func):
            function = 'FLOOR'
            arity = 1

        veiculos_por_decada = (
            Veiculo.objects
            .annotate(decada=models.ExpressionWrapper(FloorDiv(models.F('ano') / 10) * 10, output_field=models.IntegerField()))
            .values('decada')
            .annotate(qtd=models.Count('id'))
            .order_by('decada')
        )
    
        return Response({
            "total_veiculos": Veiculo.objects.count(),
            "total_fabricantes": result_fabricantes,
            "total_por_decada": veiculos_por_decada,
            "nao_vendidos": Veiculo.objects.filter(vendido=False).count(),
            "fabricantes": result_fabricantes,
            "ultimos_cadastrados": VeiculoSerializer(ultimos_cadastrados, many=True).data
        })

