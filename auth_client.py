#!/usr/bin/env python3
"""
Cliente autenticado mejorado para MercadoLibre API
Maneja OAuth 2.0 y obtiene datos reales
"""

import os
import requests
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from urllib.parse import urlencode
import webbrowser

# Configurar logging
logging.basicConfig(level=logging.INFO)

@dataclass
class AuthenticatedProduct:
    """Producto con datos completos de API autenticada"""
    id: str
    title: str
    price: float
    currency: str
    permalink: str
    thumbnail: str
    condition: str
    sold_quantity: int
    available_quantity: int
    seller_id: str
    seller_nickname: str
    seller_reputation: Dict
    category_id: str
    category_name: str
    free_shipping: bool
    listing_type: str
    buying_mode: str
    location: str
    attributes: List[Dict]
    pictures: List[str]
    description: Optional[str] = None
    warranty: Optional[str] = None

class AuthenticatedMercadoLibreClient:
    """Cliente autenticado para MercadoLibre API"""
    
    def __init__(self, client_id: str, client_secret: str, site_id: str = "MLM"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.site_id = site_id
        self.base_url = "https://api.mercadolibre.com"
        self.auth_url = "https://auth.mercadolibre.com.mx/authorization"
        self.token_url = f"{self.base_url}/oauth/token"
        
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = None
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MercadoLibre-Python-Client/1.0.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        self.logger = logging.getLogger(__name__)
        
        # Cargar token existente si existe
        self._load_token()
    
    def _load_token(self):
        """Carga token guardado si existe"""
        token_file = '.meli_token.json'
        if os.path.exists(token_file):
            try:
                with open(token_file, 'r') as f:
                    token_data = json.load(f)
                
                self.access_token = token_data.get('access_token')
                self.refresh_token = token_data.get('refresh_token')
                expires_str = token_data.get('expires_at')
                
                if expires_str:
                    self.token_expires_at = datetime.fromisoformat(expires_str)
                
                self.logger.info("Token cargado desde archivo")
                
            except Exception as e:
                self.logger.warning(f"Error cargando token: {e}")
    
    def _save_token(self):
        """Guarda el token actual"""
        token_data = {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_at': self.token_expires_at.isoformat() if self.token_expires_at else None
        }
        
        with open('.meli_token.json', 'w') as f:
            json.dump(token_data, f)
        
        self.logger.info("Token guardado")
    
    def get_auth_url(self, redirect_uri: str = "http://localhost:8080/callback") -> str:
        """Genera URL de autorización"""
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': redirect_uri
        }
        
        return f"{self.auth_url}?{urlencode(params)}"
    
    def authenticate_with_code(self, code: str, redirect_uri: str = "http://localhost:8080/callback"):
        """Autentica usando código de autorización"""
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': redirect_uri
        }
        
        response = self.session.post(self.token_url, json=data)
        
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.refresh_token = token_data.get('refresh_token')
            
            # Calcular expiración
            expires_in = token_data.get('expires_in', 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            self._save_token()
            self.logger.info("Autenticación exitosa")
            return True
        else:
            self.logger.error(f"Error en autenticación: {response.text}")
            return False
    
    def refresh_access_token(self):
        """Refresca el token de acceso"""
        if not self.refresh_token:
            return False
        
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }
        
        response = self.session.post(self.token_url, json=data)
        
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            
            expires_in = token_data.get('expires_in', 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            self._save_token()
            self.logger.info("Token refrescado")
            return True
        else:
            self.logger.error(f"Error refrescando token: {response.text}")
            return False
    
    def _ensure_valid_token(self):
        """Asegura que el token sea válido"""
        if not self.access_token:
            raise Exception("No hay token de acceso. Ejecuta authenticate() primero.")
        
        # Verificar si el token está por expirar
        if self.token_expires_at and datetime.now() >= self.token_expires_at - timedelta(minutes=5):
            self.logger.info("Token por expirar, refrescando...")
            if not self.refresh_access_token():
                raise Exception("No se pudo refrescar el token")
    
    def _make_authenticated_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Hace request autenticado"""
        self._ensure_valid_token()
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = f"{self.base_url}{endpoint}"
        
        response = self.session.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            # Token inválido, intentar refrescar
            if self.refresh_access_token():
                headers = {'Authorization': f'Bearer {self.access_token}'}
                response = self.session.get(url, params=params, headers=headers)
                if response.status_code == 200:
                    return response.json()
            
            raise Exception("Token inválido y no se pudo refrescar")
        else:
            raise Exception(f"Error en API: {response.status_code} - {response.text}")
    
    def search_products_authenticated(self, query: str, limit: int = 50, **filters) -> List[AuthenticatedProduct]:
        """Busca productos con API autenticada"""
        params = {
            'q': query,
            'limit': min(limit, 50),  # Máximo 50 por request
            'site_id': self.site_id
        }
        
        # Agregar filtros
        if 'category' in filters:
            params['category'] = filters['category']
        if 'condition' in filters:
            params['condition'] = filters['condition']
        if 'sort' in filters:
            params['sort'] = filters['sort']
        
        try:
            data = self._make_authenticated_request(f"/sites/{self.site_id}/search", params)
            products = []
            
            for item in data.get('results', []):
                try:
                    # Obtener información adicional del vendedor
                    seller_info = self._get_seller_info(item.get('seller', {}).get('id'))
                    
                    product = AuthenticatedProduct(
                        id=item.get('id', ''),
                        title=item.get('title', ''),
                        price=item.get('price', 0.0),
                        currency=item.get('currency_id', 'MXN'),
                        permalink=item.get('permalink', ''),
                        thumbnail=item.get('thumbnail', ''),
                        condition=item.get('condition', ''),
                        sold_quantity=item.get('sold_quantity', 0),
                        available_quantity=item.get('available_quantity', 0),
                        seller_id=item.get('seller', {}).get('id', ''),
                        seller_nickname=seller_info.get('nickname', ''),
                        seller_reputation=seller_info.get('seller_reputation', {}),
                        category_id=item.get('category_id', ''),
                        category_name=self._get_category_name(item.get('category_id', '')),
                        free_shipping=item.get('shipping', {}).get('free_shipping', False),
                        listing_type=item.get('listing_type_id', ''),
                        buying_mode=item.get('buying_mode', ''),
                        location=item.get('seller_address', {}).get('city', {}).get('name', ''),
                        attributes=item.get('attributes', []),
                        pictures=[pic.get('url', '') for pic in item.get('pictures', [])]
                    )
                    
                    products.append(product)
                    
                except Exception as e:
                    self.logger.warning(f"Error procesando producto: {e}")
                    continue
            
            return products
            
        except Exception as e:
            self.logger.error(f"Error en búsqueda autenticada: {e}")
            return []
    
    def _get_seller_info(self, seller_id: str) -> Dict:
        """Obtiene información del vendedor"""
        if not seller_id:
            return {}
        
        try:
            return self._make_authenticated_request(f"/users/{seller_id}")
        except:
            return {}
    
    def _get_category_name(self, category_id: str) -> str:
        """Obtiene nombre de categoría"""
        if not category_id:
            return ''
        
        try:
            data = self._make_authenticated_request(f"/categories/{category_id}")
            return data.get('name', '')
        except:
            return ''
    
    def get_product_details(self, product_id: str) -> Optional[AuthenticatedProduct]:
        """Obtiene detalles completos de un producto"""
        try:
            # Obtener datos básicos
            product_data = self._make_authenticated_request(f"/items/{product_id}")
            
            # Obtener descripción
            try:
                desc_data = self._make_authenticated_request(f"/items/{product_id}/description")
                description = desc_data.get('plain_text', '')
            except:
                description = None
            
            # Obtener info del vendedor
            seller_info = self._get_seller_info(product_data.get('seller_id', ''))
            
            product = AuthenticatedProduct(
                id=product_data.get('id', ''),
                title=product_data.get('title', ''),
                price=product_data.get('price', 0.0),
                currency=product_data.get('currency_id', 'MXN'),
                permalink=product_data.get('permalink', ''),
                thumbnail=product_data.get('thumbnail', ''),
                condition=product_data.get('condition', ''),
                sold_quantity=product_data.get('sold_quantity', 0),
                available_quantity=product_data.get('available_quantity', 0),
                seller_id=product_data.get('seller_id', ''),
                seller_nickname=seller_info.get('nickname', ''),
                seller_reputation=seller_info.get('seller_reputation', {}),
                category_id=product_data.get('category_id', ''),
                category_name=self._get_category_name(product_data.get('category_id', '')),
                free_shipping=product_data.get('shipping', {}).get('free_shipping', False),
                listing_type=product_data.get('listing_type_id', ''),
                buying_mode=product_data.get('buying_mode', ''),
                location=product_data.get('seller_address', {}).get('city', {}).get('name', ''),
                attributes=product_data.get('attributes', []),
                pictures=[pic.get('url', '') for pic in product_data.get('pictures', [])],
                description=description,
                warranty=product_data.get('warranty', '')
            )
            
            return product
            
        except Exception as e:
            self.logger.error(f"Error obteniendo detalles del producto: {e}")
            return None

def create_authenticated_client() -> AuthenticatedMercadoLibreClient:
    """Factory para crear cliente autenticado"""
    from dotenv import load_dotenv
    load_dotenv()
    
    client_id = os.getenv('MELI_CLIENT_ID')
    client_secret = os.getenv('MELI_CLIENT_SECRET')
    site_id = os.getenv('DEFAULT_SITE', 'MLM')
    
    if not client_id or not client_secret:
        raise Exception("MELI_CLIENT_ID y MELI_CLIENT_SECRET deben estar configurados en .env")
    
    return AuthenticatedMercadoLibreClient(client_id, client_secret, site_id)

if __name__ == "__main__":
    # Ejemplo de uso
    try:
        client = create_authenticated_client()
        
        # Si no hay token, mostrar URL de autorización
        if not client.access_token:
            auth_url = client.get_auth_url()
            print(f"Ve a esta URL para autorizar la aplicación:")
            print(auth_url)
            print("\nDespués de autorizar, copia el código de la URL de callback")
            
            code = input("Ingresa el código: ")
            if client.authenticate_with_code(code):
                print("✅ Autenticación exitosa!")
            else:
                print("❌ Error en autenticación")
                exit(1)
        
        # Probar búsqueda
        print("\n🔍 Probando búsqueda autenticada...")
        products = client.search_products_authenticated("iPhone 15", 3)
        
        for product in products:
            print(f"📱 {product.title}")
            print(f"   💰 ${product.price:,.2f}")
            print(f"   🔥 {product.sold_quantity:,} vendidos")
            print(f"   👤 {product.seller_nickname}")
            print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
