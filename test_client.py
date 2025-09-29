#!/usr/bin/env python3
"""
Script de pruebas para el cliente de MercadoLibre API
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch
from rich.console import Console

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from public_client import PublicMercadoLibreClient, SimpleProduct
from config import Config

console = Console()

class TestPublicClient(unittest.TestCase):
    """Pruebas para el cliente público"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.client = PublicMercadoLibreClient()
    
    def tearDown(self):
        """Limpieza después de cada prueba"""
        self.client.close()
    
    def test_client_initialization(self):
        """Prueba la inicialización del cliente"""
        self.assertEqual(self.client.site_id, "MLM")
        self.assertIsNotNone(self.client.session)
        self.assertIsNotNone(self.client.logger)
    
    def test_generate_sample_products(self):
        """Prueba la generación de productos de ejemplo"""
        products = self.client._generate_sample_products("iPhone", 3)
        
        self.assertEqual(len(products), 3)
        self.assertIsInstance(products[0], SimpleProduct)
        self.assertIn("iPhone", products[0].title)
        self.assertGreater(products[0].price, 0)
    
    def test_search_products_public(self):
        """Prueba la búsqueda pública de productos"""
        products = self.client.search_products_public("test", 5)
        
        self.assertIsInstance(products, list)
        self.assertLessEqual(len(products), 5)
        
        if products:
            self.assertIsInstance(products[0], SimpleProduct)
    
    def test_get_categories_public(self):
        """Prueba la obtención de categorías públicas"""
        categories = self.client.get_categories_public()
        
        self.assertIsInstance(categories, list)
        if categories:
            self.assertIsInstance(categories[0], dict)
            self.assertIn('id', categories[0])
            self.assertIn('name', categories[0])

class TestConfig(unittest.TestCase):
    """Pruebas para la configuración"""
    
    def test_config_values(self):
        """Prueba los valores de configuración"""
        self.assertIn(Config.DEFAULT_SITE, Config.AVAILABLE_SITES)
        self.assertGreater(Config.DEFAULT_LIMIT, 0)
        self.assertLessEqual(Config.DEFAULT_LIMIT, 50)
    
    def test_site_name_resolution(self):
        """Prueba la resolución de nombres de sitio"""
        self.assertEqual(Config.get_site_name('MLM'), 'México')
        self.assertEqual(Config.get_site_name('MLA'), 'Argentina')
        self.assertEqual(Config.get_site_name('INVALID'), 'INVALID')
    
    def test_config_validation(self):
        """Prueba la validación de configuración"""
        validations = Config.validate_config()
        
        self.assertIsInstance(validations, dict)
        self.assertIn('site_valid', validations)
        self.assertIn('limit_valid', validations)

class TestSimpleProduct(unittest.TestCase):
    """Pruebas para la clase SimpleProduct"""
    
    def test_product_creation(self):
        """Prueba la creación de productos"""
        product = SimpleProduct(
            id="MLM123",
            title="Test Product",
            price=100.0,
            currency="MXN",
            permalink="https://test.com",
            thumbnail="https://test.com/img.jpg",
            condition="new"
        )
        
        self.assertEqual(product.id, "MLM123")
        self.assertEqual(product.title, "Test Product")
        self.assertEqual(product.price, 100.0)
        self.assertEqual(product.currency, "MXN")
        self.assertEqual(product.condition, "new")

def run_integration_tests():
    """Ejecuta pruebas de integración"""
    console.print("\n🧪 [bold blue]Ejecutando pruebas de integración[/bold blue]")
    
    tests = [
        ("Conexión a internet", test_internet_connection),
        ("Cliente público", test_public_client_integration),
        ("Exportación de datos", test_data_export),
        ("Configuración", test_config_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            console.print(f"🔍 Probando: {test_name}")
            result = test_func()
            results.append((test_name, result, None))
            console.print(f"✅ {test_name}: {'PASS' if result else 'FAIL'}")
        except Exception as e:
            results.append((test_name, False, str(e)))
            console.print(f"❌ {test_name}: ERROR - {str(e)}")
    
    # Resumen
    passed = sum(1 for _, result, _ in results if result)
    total = len(results)
    
    console.print(f"\n📊 [bold]Resumen: {passed}/{total} pruebas pasaron[/bold]")
    
    return passed == total

def test_internet_connection():
    """Prueba la conexión a internet"""
    import requests
    try:
        response = requests.get("https://httpbin.org/status/200", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_public_client_integration():
    """Prueba de integración del cliente público"""
    try:
        with PublicMercadoLibreClient() as client:
            products = client.search_products_public("test", 2)
            return len(products) > 0
    except:
        return False

def test_data_export():
    """Prueba la exportación de datos"""
    try:
        with PublicMercadoLibreClient() as client:
            products = client._generate_sample_products("test", 2)
            client.export_to_json(products, "test_export.json")
            
            # Verificar que el archivo se creó
            return os.path.exists("exports/test_export.json")
    except:
        return False

def test_config_integration():
    """Prueba la integración de configuración"""
    try:
        config_summary = Config.get_config_summary()
        validations = Config.validate_config()
        
        return (
            isinstance(config_summary, dict) and
            isinstance(validations, dict) and
            all(validations.values())
        )
    except:
        return False

def main():
    """Función principal de pruebas"""
    console.print("🧪 [bold blue]Suite de Pruebas - Cliente MercadoLibre API[/bold blue]")
    console.print("=" * 60)
    
    # Pruebas unitarias
    console.print("\n📋 [bold]Ejecutando pruebas unitarias[/bold]")
    
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar clases de prueba
    suite.addTests(loader.loadTestsFromTestCase(TestPublicClient))
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestSimpleProduct))
    
    # Ejecutar pruebas unitarias
    runner = unittest.TextTestRunner(verbosity=2)
    unit_result = runner.run(suite)
    
    # Pruebas de integración
    integration_result = run_integration_tests()
    
    # Resumen final
    console.print("\n" + "=" * 60)
    
    if unit_result.wasSuccessful() and integration_result:
        console.print("🎉 [bold green]¡Todas las pruebas pasaron![/bold green]")
        console.print("✅ El cliente está listo para usar")
        return 0
    else:
        console.print("❌ [bold red]Algunas pruebas fallaron[/bold red]")
        
        if not unit_result.wasSuccessful():
            console.print(f"   Pruebas unitarias: {len(unit_result.failures)} fallos, {len(unit_result.errors)} errores")
        
        if not integration_result:
            console.print("   Pruebas de integración: FALLARON")
        
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        console.print("\n\n⚠️  Pruebas interrumpidas por el usuario")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
