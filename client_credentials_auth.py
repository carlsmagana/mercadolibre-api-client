#!/usr/bin/env python3
"""
Autenticación con Client Credentials para MercadoLibre
Más simple para búsquedas de productos públicos
"""

import os
import requests
import json
from dotenv import load_dotenv

class ClientCredentialsAuth:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('MELI_CLIENT_ID')
        self.client_secret = os.getenv('MELI_CLIENT_SECRET')
        
        if not self.client_id or not self.client_secret:
            raise Exception("MELI_CLIENT_ID y MELI_CLIENT_SECRET deben estar configurados en .env")
    
    def get_access_token(self):
        """Obtiene token usando Client Credentials (más simple)"""
        token_url = "https://api.mercadolibre.com/oauth/token"
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        try:
            print("🔄 Obteniendo token con Client Credentials...")
            response = requests.post(token_url, json=data)
            
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                token_data = response.json()
                
                # Guardar token
                with open('.meli_token.json', 'w') as f:
                    json.dump(token_data, f, indent=2)
                
                print("✅ ¡Token obtenido exitosamente!")
                print(f"🔑 Access Token: {token_data['access_token'][:20]}...")
                print(f"⏰ Expira en: {token_data.get('expires_in', 'N/A')} segundos")
                print(f"🔍 Tipo: {token_data.get('token_type', 'N/A')}")
                
                return token_data['access_token']
            else:
                print(f"❌ Error obteniendo token: {response.status_code}")
                print(f"Respuesta: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def test_token(self, access_token=None):
        """Prueba el token con una búsqueda real"""
        if not access_token:
            # Cargar token guardado
            if not os.path.exists('.meli_token.json'):
                print("❌ No hay token guardado")
                return False
            
            try:
                with open('.meli_token.json', 'r') as f:
                    token_data = json.load(f)
                access_token = token_data.get('access_token')
            except:
                print("❌ Error cargando token")
                return False
        
        if not access_token:
            print("❌ Token inválido")
            return False
        
        print("🔄 Probando token con búsqueda real...")
        
        # Probar con una búsqueda de productos
        headers = {'Authorization': f'Bearer {access_token}'}
        
        try:
            response = requests.get(
                'https://api.mercadolibre.com/sites/MLM/search?q=iPhone&limit=3',
                headers=headers
            )
            
            print(f"📊 Status de prueba: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ ¡Token funcionando perfectamente!")
                print(f"📊 Total de productos disponibles: {data.get('paging', {}).get('total', 'N/A'):,}")
                
                # Mostrar productos de ejemplo
                results = data.get('results', [])
                if results:
                    print(f"\n📱 Productos encontrados ({len(results)}):")
                    for i, product in enumerate(results, 1):
                        print(f"  {i}. {product.get('title', 'N/A')}")
                        print(f"     💰 ${product.get('price', 0):,.2f}")
                        print(f"     🔥 {product.get('sold_quantity', 0):,} vendidos")
                        print(f"     👤 Vendedor: {product.get('seller', {}).get('nickname', 'N/A')}")
                        print()
                
                return True
            else:
                print(f"❌ Token no válido: {response.status_code}")
                print(f"Respuesta: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error probando token: {str(e)}")
            return False
    
    def search_products(self, query, limit=10):
        """Busca productos usando el token"""
        # Cargar token
        if not os.path.exists('.meli_token.json'):
            print("❌ No hay token. Ejecuta 'get_token' primero.")
            return []
        
        try:
            with open('.meli_token.json', 'r') as f:
                token_data = json.load(f)
            access_token = token_data.get('access_token')
        except:
            print("❌ Error cargando token")
            return []
        
        if not access_token:
            print("❌ Token inválido")
            return []
        
        print(f"🔍 Buscando: '{query}' (límite: {limit})")
        
        headers = {'Authorization': f'Bearer {access_token}'}
        params = {
            'q': query,
            'limit': min(limit, 50)
        }
        
        try:
            response = requests.get(
                'https://api.mercadolibre.com/sites/MLM/search',
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                print(f"✅ Encontrados {len(results)} productos REALES")
                
                products = []
                for product in results:
                    products.append({
                        'id': product.get('id'),
                        'title': product.get('title'),
                        'price': product.get('price'),
                        'currency': product.get('currency_id'),
                        'sold_quantity': product.get('sold_quantity'),
                        'condition': product.get('condition'),
                        'seller_nickname': product.get('seller', {}).get('nickname'),
                        'free_shipping': product.get('shipping', {}).get('free_shipping', False),
                        'permalink': product.get('permalink')
                    })
                
                return products
            else:
                print(f"❌ Error en búsqueda: {response.status_code}")
                print(f"Respuesta: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return []

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python3 client_credentials_auth.py get_token    # Obtener token")
        print("  python3 client_credentials_auth.py test         # Probar token")
        print("  python3 client_credentials_auth.py search QUERY # Buscar productos")
        return
    
    command = sys.argv[1]
    
    try:
        auth = ClientCredentialsAuth()
        
        if command == "get_token":
            token = auth.get_access_token()
            if token:
                print("\n🎉 ¡Listo! Ahora puedes buscar productos:")
                print("python3 client_credentials_auth.py test")
                print("python3 client_credentials_auth.py search 'iPhone 15'")
            
        elif command == "test":
            auth.test_token()
            
        elif command == "search":
            if len(sys.argv) > 2:
                query = " ".join(sys.argv[2:])
                products = auth.search_products(query, 5)
                
                if products:
                    print(f"\n📋 Resultados para '{query}':")
                    for i, product in enumerate(products, 1):
                        print(f"\n{i}. {product['title']}")
                        print(f"   💰 ${product['price']:,.2f} {product['currency']}")
                        print(f"   🔥 {product['sold_quantity']:,} vendidos")
                        print(f"   👤 {product['seller_nickname']}")
                        print(f"   🚚 {'✅ Envío gratis' if product['free_shipping'] else '💰 Envío pago'}")
            else:
                print("❌ Especifica qué buscar: python3 client_credentials_auth.py search 'iPhone 15'")
            
        else:
            print(f"❌ Comando desconocido: {command}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
