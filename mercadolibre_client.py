#!/usr/bin/env python3
"""
Cliente oficial para las APIs de MercadoLibre México
Documentación: https://developers.mercadolibre.com.mx/
"""

import requests
import time
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
from urllib.parse import urlencode
from dataclasses import dataclass
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

@dataclass
class Product:
    """Clase para representar un producto de MercadoLibre"""
    id: str
    title: str
    price: float
    currency_id: str
    permalink: str
    thumbnail: str
    condition: str
    listing_type_id: str
    seller_id: Optional[str] = None
    category_id: Optional[str] = None
    available_quantity: Optional[int] = None
    sold_quantity: Optional[int] = None
    free_shipping: bool = False
    official_store_id: Optional[str] = None
    seller_reputation: Optional[Dict] = None
    
    @classmethod
    def from_api_response(cls, data: Dict) -> 'Product':
        """Crea un Product desde la respuesta de la API"""
        shipping = data.get('shipping', {})
        seller = data.get('seller', {})
        
        return cls(
            id=data.get('id', ''),
            title=data.get('title', ''),
            price=data.get('price', 0.0),
            currency_id=data.get('currency_id', 'MXN'),
            permalink=data.get('permalink', ''),
            thumbnail=data.get('thumbnail', ''),
            condition=data.get('condition', ''),
            listing_type_id=data.get('listing_type_id', ''),
            seller_id=seller.get('id'),
            category_id=data.get('category_id'),
            available_quantity=data.get('available_quantity'),
            sold_quantity=data.get('sold_quantity'),
            free_shipping=shipping.get('free_shipping', False),
            official_store_id=data.get('official_store_id'),
            seller_reputation=seller.get('seller_reputation')
        )

class MercadoLibreClient:
    """Cliente para interactuar con las APIs oficiales de MercadoLibre"""
    
    BASE_URL = "https://api.mercadolibre.com"
    
    def __init__(self, site_id: str = "MLM", client_id: Optional[str] = None, 
                 client_secret: Optional[str] = None):
        """
        Inicializa el cliente de MercadoLibre
        
        Args:
            site_id: ID del sitio (MLM=México, MLA=Argentina, MLB=Brasil, etc.)
            client_id: Client ID para APIs autenticadas (opcional)
            client_secret: Client Secret para APIs autenticadas (opcional)
        """
        self.site_id = site_id
        self.client_id = client_id or os.getenv('MELI_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('MELI_CLIENT_SECRET')
        
        # Configuración de rate limiting
        self.requests_per_minute = int(os.getenv('REQUESTS_PER_MINUTE', 60))
        self.delay_between_requests = float(os.getenv('DELAY_BETWEEN_REQUESTS', 1.0))
        self.last_request_time = 0
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Session para reutilizar conexiones
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MercadoLibre-API-Client/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        # Token de acceso (si está disponible)
        self.access_token = None
        
        self.logger.info(f"Cliente inicializado para sitio: {site_id}")
    
    def _rate_limit(self):
        """Implementa rate limiting para respetar los límites de la API"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.delay_between_requests:
            sleep_time = self.delay_between_requests - time_since_last_request
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Hace una petición a la API con manejo de errores y rate limiting
        
        Args:
            endpoint: Endpoint de la API
            params: Parámetros de la petición
            
        Returns:
            Respuesta de la API como diccionario
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            self.logger.debug(f"Haciendo petición a: {url}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                self.logger.warning("Rate limit excedido, esperando...")
                time.sleep(60)  # Esperar 1 minuto
                return self._make_request(endpoint, params)  # Reintentar
            else:
                self.logger.error(f"Error HTTP {response.status_code}: {e}")
                raise
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error en la petición: {e}")
            raise
    
    def search_products(self, query: str, limit: int = 50, offset: int = 0, 
                       category: Optional[str] = None, condition: Optional[str] = None,
                       sort: str = 'relevance') -> Dict:
        """
        Busca productos usando la API de búsqueda
        
        Args:
            query: Término de búsqueda
            limit: Número de resultados (máximo 50)
            offset: Desplazamiento para paginación
            category: ID de categoría para filtrar
            condition: Condición del producto (new, used, not_specified)
            sort: Ordenamiento (relevance, price_asc, price_desc)
            
        Returns:
            Diccionario con los resultados de la búsqueda
        """
        endpoint = f"/sites/{self.site_id}/search"
        
        params = {
            'q': query,
            'limit': min(limit, 50),  # API limita a 50
            'offset': offset,
            'sort': sort
        }
        
        if category:
            params['category'] = category
        if condition:
            params['condition'] = condition
        
        self.logger.info(f"Buscando productos: '{query}' (limit={limit}, offset={offset})")
        
        return self._make_request(endpoint, params)
    
    def get_product_details(self, product_id: str) -> Dict:
        """
        Obtiene detalles completos de un producto
        
        Args:
            product_id: ID del producto
            
        Returns:
            Diccionario con los detalles del producto
        """
        endpoint = f"/items/{product_id}"
        
        self.logger.info(f"Obteniendo detalles del producto: {product_id}")
        
        return self._make_request(endpoint)
    
    def get_product_description(self, product_id: str) -> Dict:
        """
        Obtiene la descripción de un producto
        
        Args:
            product_id: ID del producto
            
        Returns:
            Diccionario con la descripción del producto
        """
        endpoint = f"/items/{product_id}/description"
        
        return self._make_request(endpoint)
    
    def get_categories(self) -> List[Dict]:
        """
        Obtiene todas las categorías disponibles
        
        Returns:
            Lista de categorías
        """
        endpoint = f"/sites/{self.site_id}/categories"
        
        self.logger.info("Obteniendo categorías")
        
        return self._make_request(endpoint)
    
    def get_category_details(self, category_id: str) -> Dict:
        """
        Obtiene detalles de una categoría específica
        
        Args:
            category_id: ID de la categoría
            
        Returns:
            Diccionario con los detalles de la categoría
        """
        endpoint = f"/categories/{category_id}"
        
        return self._make_request(endpoint)
    
    def get_seller_info(self, seller_id: str) -> Dict:
        """
        Obtiene información de un vendedor
        
        Args:
            seller_id: ID del vendedor
            
        Returns:
            Diccionario con la información del vendedor
        """
        endpoint = f"/users/{seller_id}"
        
        return self._make_request(endpoint)
    
    def search_all_pages(self, query: str, max_results: int = 1000, 
                        category: Optional[str] = None, condition: Optional[str] = None) -> List[Product]:
        """
        Busca productos en todas las páginas hasta alcanzar max_results
        
        Args:
            query: Término de búsqueda
            max_results: Número máximo de resultados
            category: ID de categoría para filtrar
            condition: Condición del producto
            
        Returns:
            Lista de productos encontrados
        """
        all_products = []
        offset = 0
        limit = 50
        
        self.logger.info(f"Iniciando búsqueda completa: '{query}' (max_results={max_results})")
        
        while len(all_products) < max_results:
            try:
                response = self.search_products(
                    query=query,
                    limit=limit,
                    offset=offset,
                    category=category,
                    condition=condition
                )
                
                results = response.get('results', [])
                
                if not results:
                    self.logger.info("No hay más resultados")
                    break
                
                # Convertir a objetos Product
                products = [Product.from_api_response(item) for item in results]
                all_products.extend(products)
                
                self.logger.info(f"Obtenidos {len(products)} productos (total: {len(all_products)})")
                
                # Verificar si hay más páginas
                paging = response.get('paging', {})
                total = paging.get('total', 0)
                
                if offset + limit >= total or len(all_products) >= max_results:
                    break
                
                offset += limit
                
            except Exception as e:
                self.logger.error(f"Error en búsqueda: {e}")
                break
        
        # Limitar al número máximo solicitado
        return all_products[:max_results]
    
    def export_to_json(self, products: List[Product], filename: str):
        """
        Exporta productos a un archivo JSON
        
        Args:
            products: Lista de productos
            filename: Nombre del archivo
        """
        os.makedirs('exports', exist_ok=True)
        filepath = f"exports/{filename}"
        
        # Convertir productos a diccionarios
        products_data = []
        for product in products:
            product_dict = {
                'id': product.id,
                'titulo': product.title,
                'precio': product.price,
                'moneda': product.currency_id,
                'url': product.permalink,
                'imagen': product.thumbnail,
                'condicion': product.condition,
                'tipo_publicacion': product.listing_type_id,
                'vendedor_id': product.seller_id,
                'categoria_id': product.category_id,
                'cantidad_disponible': product.available_quantity,
                'cantidad_vendida': product.sold_quantity,
                'envio_gratis': product.free_shipping,
                'tienda_oficial_id': product.official_store_id
            }
            products_data.append(product_dict)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(products_data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Productos exportados a: {filepath}")
    
    def export_to_csv(self, products: List[Product], filename: str):
        """
        Exporta productos a un archivo CSV
        
        Args:
            products: Lista de productos
            filename: Nombre del archivo
        """
        try:
            import pandas as pd
            
            os.makedirs('exports', exist_ok=True)
            filepath = f"exports/{filename}"
            
            # Convertir a DataFrame
            data = []
            for product in products:
                data.append({
                    'id': product.id,
                    'titulo': product.title,
                    'precio': product.price,
                    'moneda': product.currency_id,
                    'url': product.permalink,
                    'imagen': product.thumbnail,
                    'condicion': product.condition,
                    'tipo_publicacion': product.listing_type_id,
                    'vendedor_id': product.seller_id,
                    'categoria_id': product.category_id,
                    'cantidad_disponible': product.available_quantity,
                    'cantidad_vendida': product.sold_quantity,
                    'envio_gratis': product.free_shipping,
                    'tienda_oficial_id': product.official_store_id
                })
            
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8')
            
            self.logger.info(f"Productos exportados a: {filepath}")
            
        except ImportError:
            self.logger.error("pandas no está instalado. Usa export_to_json en su lugar.")
    
    def close(self):
        """Cierra la sesión"""
        self.session.close()
        self.logger.info("Cliente cerrado")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# Función de conveniencia
def create_client(site_id: str = "MLM") -> MercadoLibreClient:
    """
    Crea un cliente de MercadoLibre con configuración por defecto
    
    Args:
        site_id: ID del sitio (MLM=México por defecto)
        
    Returns:
        Cliente configurado
    """
    return MercadoLibreClient(site_id=site_id)
