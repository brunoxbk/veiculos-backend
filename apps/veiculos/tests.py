from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Veiculo
from .serializers import VeiculoSerializer


class VeiculoListCreateViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('veiculo-list-create')
        
        self.veiculo1 = Veiculo.objects.create(
            veiculo='Civic',
            marca=Veiculo.Marca.HONDA,
            ano=2020,
            descricao='Sedan Honda Civic',
            vendido=False
        )
        
        self.veiculo2 = Veiculo.objects.create(
            veiculo='Corolla',
            marca=Veiculo.Marca.TOYOTA,
            ano=2019,
            descricao='Sedan Toyota Corolla',
            vendido=True
        )
        
        self.veiculo3 = Veiculo.objects.create(
            veiculo='Onix',
            marca=Veiculo.Marca.CHEVROLET,
            ano=2020,
            descricao='Hatch Chevrolet Onix',
            vendido=False
        )

    def test_get_veiculo_list(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        
        veiculos = response.data
        self.assertEqual(veiculos[0]['veiculo'], 'Civic')
        self.assertEqual(veiculos[1]['veiculo'], 'Corolla')
        self.assertEqual(veiculos[2]['veiculo'], 'Onix')

    def test_get_veiculo_list_empty(self):
        Veiculo.objects.all().delete()
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_filter_by_marca(self):
        response = self.client.get(self.url, {'marca': 'HONDA'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['marca'], 'HONDA')

    def test_filter_by_ano(self):
        response = self.client.get(self.url, {'ano': 2020})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for veiculo in response.data:
            self.assertEqual(veiculo['ano'], 2020)

    def test_filter_by_vendido_true(self):
        response = self.client.get(self.url, {'vendido': 'true'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['vendido'], True)

    def test_filter_by_vendido_false(self):
        response = self.client.get(self.url, {'vendido': 'false'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for veiculo in response.data:
            self.assertEqual(veiculo['vendido'], False)

    def test_multiple_filters(self):
        response = self.client.get(self.url, {
            'marca': 'CHEVROLET',
            'ano': 2020,
            'vendido': 'false'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        veiculo = response.data[0]
        self.assertEqual(veiculo['marca'], 'CHEVROLET')
        self.assertEqual(veiculo['ano'], 2020)
        self.assertEqual(veiculo['vendido'], False)

    def test_create_veiculo_success(self):
        data = {
            'veiculo': 'Fiesta',
            'marca': 'FORD',
            'ano': 2021,
            'descricao': 'Hatch Ford Fiesta',
            'vendido': False
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Veiculo.objects.count(), 4)
        
        novo_veiculo = Veiculo.objects.get(veiculo='Fiesta')
        self.assertEqual(novo_veiculo.marca, 'FORD')
        self.assertEqual(novo_veiculo.ano, 2021)
        self.assertEqual(novo_veiculo.descricao, 'Hatch Ford Fiesta')
        self.assertFalse(novo_veiculo.vendido)

    def test_create_veiculo_invalid_data(self):
        data = {
            'veiculo': '',
            'marca': 'FORD',
            'ano': 2021,
            'descricao': 'Hatch Ford Fiesta',
            'vendido': False
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Veiculo.objects.count(), 3)
        self.assertIn('veiculo', response.data)

    def test_create_veiculo_invalid_marca(self):
        data = {
            'veiculo': 'Fiesta',
            'marca': 'MARCA_INVALIDA',
            'ano': 2021,
            'descricao': 'Hatch Ford Fiesta',
            'vendido': False
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Veiculo.objects.count(), 3)
        self.assertIn('marca', response.data)

    def test_create_veiculo_missing_required_fields(self):
        data = {
            'veiculo': 'Fiesta',
            'ano': 2021,
            'descricao': 'Hatch Ford Fiesta',
            'vendido': False
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Veiculo.objects.count(), 3)
        self.assertIn('marca', response.data)

    def test_create_veiculo_invalid_ano(self):
        data = {
            'veiculo': 'Fiesta',
            'marca': 'FORD',
            'ano': 'ano_invalido',
            'descricao': 'Hatch Ford Fiesta',
            'vendido': False
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Veiculo.objects.count(), 3)

    def test_create_veiculo_all_marca_choices(self):
        marcas_validas = [
            'CHEVROLET', 'FIAT', 'FORD', 'VOLKSWAGEN', 'RENAULT',
            'HONDA', 'TOYOTA', 'HYUNDAI', 'NISSAN', 'PEUGEOT',
            'CITROEN', 'JEEP', 'MITSUBISHI', 'KIA'
        ]
        
        for marca in marcas_validas:
            data = {
                'veiculo': f'Veiculo {marca}',
                'marca': marca,
                'ano': 2020,
                'descricao': f'Veículo da marca {marca}',
                'vendido': False
            }
            
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class VeiculoRetrieveUpdateDestroyViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.veiculo = Veiculo.objects.create(
            veiculo='Civic',
            marca=Veiculo.Marca.HONDA,
            ano=2020,
            descricao='Sedan Honda Civic',
            vendido=False
        )
        
        self.url = reverse('veiculo-detail', kwargs={'pk': self.veiculo.pk})

    def test_get_veiculo_detail(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.veiculo.id)
        self.assertEqual(response.data['veiculo'], 'Civic')
        self.assertEqual(response.data['marca'], 'HONDA')
        self.assertEqual(response.data['ano'], 2020)
        self.assertEqual(response.data['descricao'], 'Sedan Honda Civic')
        self.assertFalse(response.data['vendido'])

    def test_get_veiculo_not_found(self):
        url = reverse('veiculo-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_veiculo_put_success(self):
        data = {
            'veiculo': 'Civic Atualizado',
            'marca': 'HONDA',
            'ano': 2021,
            'descricao': 'Sedan Honda Civic Atualizado',
            'vendido': True
        }
        
        response = self.client.put(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.veiculo.refresh_from_db()
        self.assertEqual(self.veiculo.veiculo, 'Civic Atualizado')
        self.assertEqual(self.veiculo.ano, 2021)
        self.assertEqual(self.veiculo.descricao, 'Sedan Honda Civic Atualizado')
        self.assertTrue(self.veiculo.vendido)

    def test_update_veiculo_patch_success(self):
        data = {
            'vendido': True,
            'descricao': 'Descrição atualizada'
        }
        
        response = self.client.patch(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.veiculo.refresh_from_db()
        self.assertTrue(self.veiculo.vendido)
        self.assertEqual(self.veiculo.descricao, 'Descrição atualizada')
        self.assertEqual(self.veiculo.veiculo, 'Civic')
        self.assertEqual(self.veiculo.marca, 'HONDA')

    def test_update_veiculo_put_invalid_data(self):
        data = {
            'veiculo': '',
            'marca': 'HONDA',
            'ano': 2021,
            'descricao': 'Descrição',
            'vendido': True
        }
        
        response = self.client.put(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('veiculo', response.data)
        
        self.veiculo.refresh_from_db()
        self.assertEqual(self.veiculo.veiculo, 'Civic')

    def test_update_veiculo_patch_invalid_marca(self):
        data = {
            'marca': 'MARCA_INVALIDA'
        }
        
        response = self.client.patch(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('marca', response.data)
        
        self.veiculo.refresh_from_db()
        self.assertEqual(self.veiculo.marca, 'HONDA')

    def test_update_veiculo_put_missing_fields(self):
        data = {
            'veiculo': 'Civic Atualizado',
            'ano': 2021,
            'descricao': 'Descrição',
            'vendido': True
        }
        
        response = self.client.put(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('marca', response.data)

    def test_delete_veiculo_success(self):
        veiculo_id = self.veiculo.id
        
        response = self.client.delete(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Veiculo.objects.count(), 0)
        
        with self.assertRaises(Veiculo.DoesNotExist):
            Veiculo.objects.get(id=veiculo_id)

    def test_delete_veiculo_not_found(self):
        url = reverse('veiculo-detail', kwargs={'pk': 9999})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Veiculo.objects.count(), 1)

    def test_update_veiculo_change_marca(self):
        data = {
            'veiculo': 'Civic',
            'marca': 'TOYOTA',
            'ano': 2020,
            'descricao': 'Sedan Honda Civic',
            'vendido': False
        }
        
        response = self.client.put(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.veiculo.refresh_from_db()
        self.assertEqual(self.veiculo.marca, 'TOYOTA')

    def test_patch_only_vendido_status(self):
        self.assertFalse(self.veiculo.vendido)
        
        data = {'vendido': True}
        response = self.client.patch(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.veiculo.refresh_from_db()
        self.assertTrue(self.veiculo.vendido)
        self.assertEqual(self.veiculo.veiculo, 'Civic')
        self.assertEqual(self.veiculo.marca, 'HONDA')
        self.assertEqual(self.veiculo.ano, 2020)

    def test_patch_only_ano(self):
        data = {'ano': 2022}
        response = self.client.patch(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.veiculo.refresh_from_db()
        self.assertEqual(self.veiculo.ano, 2022)
        self.assertEqual(self.veiculo.veiculo, 'Civic')
        self.assertEqual(self.veiculo.marca, 'HONDA')
        self.assertFalse(self.veiculo.vendido)


class VeiculoModelTest(TestCase):
    def test_create_veiculo(self):
        veiculo = Veiculo.objects.create(
            veiculo='Civic',
            marca=Veiculo.Marca.HONDA,
            ano=2020,
            descricao='Sedan Honda Civic',
            vendido=False
        )
        
        self.assertEqual(veiculo.veiculo, 'Civic')
        self.assertEqual(veiculo.marca, 'HONDA')
        self.assertEqual(veiculo.ano, 2020)
        self.assertEqual(veiculo.descricao, 'Sedan Honda Civic')
        self.assertFalse(veiculo.vendido)
        self.assertIsNotNone(veiculo.created)
        self.assertIsNotNone(veiculo.updated)

    def test_veiculo_str_representation(self):
        veiculo = Veiculo.objects.create(
            veiculo='Civic',
            marca=Veiculo.Marca.HONDA,
            ano=2020,
            descricao='Sedan Honda Civic',
            vendido=False
        )
        
        expected_str = "HONDA Civic (2020)"
        self.assertEqual(str(veiculo), expected_str)

    def test_marca_choices_values(self):
        expected_choices = {
            'CHEVROLET': 'Chevrolet',
            'FIAT': 'Fiat',
            'FORD': 'Ford',
            'VOLKSWAGEN': 'Volkswagen',
            'RENAULT': 'Renault',
            'HONDA': 'Honda',
            'TOYOTA': 'Toyota',
            'HYUNDAI': 'Hyundai',
            'NISSAN': 'Nissan',
            'PEUGEOT': 'Peugeot',
            'CITROEN': 'Citroën',
            'JEEP': 'Jeep',
            'MITSUBISHI': 'Mitsubishi',
            'KIA': 'Kia'
        }
        
        for key_choice, label_choice in expected_choices.items():
            self.assertEqual(getattr(Veiculo.Marca, key_choice), key_choice)
            choice_found = False
            for choice_key, choice_label in Veiculo.Marca.choices:
                if choice_key == key_choice and choice_label == label_choice:
                    choice_found = True
                    break
            self.assertTrue(choice_found, f"Choice {key_choice}:{label_choice} não encontrada")

    def test_veiculo_auto_timestamps(self):
        veiculo = Veiculo.objects.create(
            veiculo='Civic',
            marca=Veiculo.Marca.HONDA,
            ano=2020,
            descricao='Sedan Honda Civic',
            vendido=False
        )
        
        self.assertIsNotNone(veiculo.created)
        self.assertIsNotNone(veiculo.updated)
        
        original_updated = veiculo.updated
        veiculo.descricao = 'Descrição atualizada'
        veiculo.save()
        
        veiculo.refresh_from_db()
        self.assertGreater(veiculo.updated, original_updated)

    def test_veiculo_fields_max_length(self):
        veiculo_name = 'a' * 100
        veiculo = Veiculo.objects.create(
            veiculo=veiculo_name,
            marca=Veiculo.Marca.HONDA,
            ano=2020,
            descricao='Descrição teste',
            vendido=False
        )
        self.assertEqual(len(veiculo.veiculo), 100)
        
        marca_longa = Veiculo.Marca.VOLKSWAGEN
        veiculo2 = Veiculo.objects.create(
            veiculo='Teste',
            marca=marca_longa,
            ano=2020,
            descricao='Descrição teste',
            vendido=False
        )
        self.assertEqual(veiculo2.marca, marca_longa)