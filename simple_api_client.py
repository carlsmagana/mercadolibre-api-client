#!/usr/bin/env python3
"""
Cliente simple para MercadoLibre API
Usa búsquedas públicas con tu App ID
"""

import os
import requests
import json
from dotenv import load_dotenv

class SimpleAPIClient:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('MELI_CLIENT_ID')
        
        if not self.client_id:
            raise Exception("MELI_CLIENT_ID debe estar configurado en .env")
    
    def search_products(self, query, limit=10):
        """Busca productos usando API pública con tu App ID"""
        print(f"🔍 Buscando: '{query}' (límite: {limit})")
        print(f"🔑 Usando App ID: {self.client_id}")
        
        # Usar API pública con tu App ID
        url = "https://api.mercadolibre.com/sites/MLM/search"
        params = {
            'q': query,
            'limit': min(limit, 50),
            'caller.id': self.client_id  # Identificar tu app
        }
        
        try:
            response = requests.get(url, params=params)
            
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                print(f"✅ Encontrados {len(results)} productos REALES")
                print(f"📊 Total disponible: {data.get('paging', {}).get('total', 'N/A'):,}")
                
                products = []
                for product in results:
                    products.append({
                        'id': product.get('id'),
                        'title': product.get('title'),
                        'price': product.get('price'),
                        'currency': product.get('currency_id'),
                        'sold_quantity': product.get('sold_quantity'),
                        'available_quantity': product.get('available_quantity'),
                        'condition': product.get('condition'),
                        'seller_id': product.get('seller', {}).get('id'),
                        'seller_nickname': product.get('seller', {}).get('nickname'),
                        'category_id': product.get('category_id'),
                        'free_shipping': product.get('shipping', {}).get('free_shipping', False),
                        'permalink': product.get('permalink'),
                        'thumbnail': product.get('thumbnail')
                    })
                
                return products
            else:
                print(f"❌ Error en búsqueda: {response.status_code}")
                print(f"Respuesta: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return []
    
    def get_product_details(self, product_id):
        """Obtiene detalles de un producto específico"""
        print(f"📱 Obteniendo detalles de: {product_id}")
        
        url = f"https://api.mercadolibre.com/items/{product_id}"
        params = {'caller.id': self.client_id}
        
        try:
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Detalles obtenidos")
                return data
            else:
                print(f"❌ Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def export_to_json(self, products, filename):
        """Exporta productos a JSON"""
        if not products:
            print("❌ No hay productos para exportar")
            return
        
        os.makedirs('exports', exist_ok=True)
        filepath = f"exports/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Exportado a: {filepath}")

def main():
    import sys
    from datetime import datetime
    
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python3 simple_api_client.py search QUERY [LIMIT]")
        print("  python3 simple_api_client.py product PRODUCT_ID")
        print("  python3 simple_api_client.py demo")
        return
    
    command = sys.argv[1]
    
    try:
        client = SimpleAPIClient()
        
        if command == "search":
            if len(sys.argv) < 3:
                print("❌ Especifica qué buscar")
                return
            
            query = " ".join(sys.argv[2:])
            if query.isdigit():
                # Si el último argumento es un número, es el límite
                parts = sys.argv[2:]
                limit = int(parts[-1])
                query = " ".join(parts[:-1])
            else:
                limit = 10
            
            products = client.search_products(query, limit)
            
            if products:
                print(f"\n📋 Resultados REALES para '{query}':")
                print("=" * 60)
                
                for i, product in enumerate(products, 1):
                    print(f"\n{i}. {product['title']}")
                    print(f"   🆔 ID: {product['id']}")
                    print(f"   💰 Precio: ${product['price']:,.2f} {product['currency']}")
                    print(f"   🔥 Vendidos: {product['sold_quantity']:,}")
                    print(f"   📦 Stock: {product['available_quantity']:,}")
                    print(f"   🏷️ Condición: {product['condition']}")
                    print(f"   👤 Vendedor: {product['seller_nickname']} ({product['seller_id']})")
                    print(f"   🚚 Envío: {'✅ Gratis' if product['free_shipping'] else '💰 Pago'}")
                    print(f"   🔗 URL: {product['permalink']}")
                
                # Exportar automáticamente
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"real_search_{query.replace(' ', '_')}_{timestamp}.json"
                client.export_to_json(products, filename)
        
        elif command == "product":
            if len(sys.argv) < 3:
                print("❌ Especifica el ID del producto")
                return
            
            product_id = sys.argv[2]
            details = client.get_product_details(product_id)
            
            if details:
                print(f"\n📱 Detalles REALES de {product_id}:")
                print("=" * 50)
                print(f"Título: {details.get('title')}")
                print(f"Precio: ${details.get('price'):,.2f} {details.get('currency_id')}")
                print(f"Vendidos: {details.get('sold_quantity'):,}")
                print(f"Stock: {details.get('available_quantity'):,}")
                print(f"Condición: {details.get('condition')}")
                print(f"Categoría: {details.get('category_id')}")
        
        elif command == "demo":
            print("🎬 Demo con datos REALES de MercadoLibre")
            print("=" * 50)
            
            queries = ["iPhone 15", "MacBook Pro", "Samsung Galaxy S24"]
            
            for query in queries:
                print(f"\n🔍 Buscando: {query}")
                products = client.search_products(query, 2)
                
                if products:
                    for product in products:
                        print(f"  📱 {product['title'][:50]}...")
                        print(f"     💰 ${product['price']:,.2f}")
                        print(f"     🔥 {product['sold_quantity']:,} vendidos")
                        print(f"     👤 {product['seller_nickname']}")
                else:
                    print("  ❌ Sin resultados")
        
        else:
            print(f"❌ Comando desconocido: {command}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
