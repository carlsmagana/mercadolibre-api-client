#!/usr/bin/env python3
"""
Prueba de APIs públicas de MercadoLibre sin autenticación
"""

import requests
import json

def test_public_api():
    """Prueba diferentes endpoints públicos"""
    
    print("🔍 Probando APIs públicas de MercadoLibre...")
    
    # URLs a probar
    test_urls = [
        "https://api.mercadolibre.com/sites/MLM/search?q=iPhone&limit=5",
        "https://api.mercadolibre.com/sites/MLM/categories",
        "https://api.mercadolibre.com/currencies",
        "https://api.mercadolibre.com/sites",
    ]
    
    for url in test_urls:
        try:
            print(f"\n📡 Probando: {url}")
            response = requests.get(url, timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data:
                    print(f"   ✅ Productos encontrados: {len(data['results'])}")
                    if data['results']:
                        product = data['results'][0]
                        print(f"   📱 Ejemplo: {product.get('title', 'N/A')[:50]}...")
                        print(f"   💰 Precio: ${product.get('price', 0):,.2f}")
                elif isinstance(data, list):
                    print(f"   ✅ Items encontrados: {len(data)}")
                else:
                    print(f"   ✅ Datos obtenidos: {list(data.keys())[:3]}")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    test_public_api()
