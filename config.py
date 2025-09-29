#!/usr/bin/env python3
"""
Configuración centralizada para el cliente de MercadoLibre API
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Clase de configuración centralizada"""
    
    # Configuración de API
    MELI_CLIENT_ID = os.getenv('MELI_CLIENT_ID')
    MELI_CLIENT_SECRET = os.getenv('MELI_CLIENT_SECRET')
    DEFAULT_SITE = os.getenv('DEFAULT_SITE', 'MLM')
    DEFAULT_LIMIT = int(os.getenv('DEFAULT_LIMIT', 50))
    
    # Rate limiting
    REQUESTS_PER_MINUTE = int(os.getenv('REQUESTS_PER_MINUTE', 60))
    DELAY_BETWEEN_REQUESTS = float(os.getenv('DELAY_BETWEEN_REQUESTS', 1.0))
    
    # Cache
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
    CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))
    
    # URLs base
    API_BASE_URL = "https://api.mercadolibre.com"
    AUTH_URL = "https://auth.mercadolibre.com.mx"
    
    # Directorios
    EXPORTS_DIR = "exports"
    CACHE_DIR = "cache"
    LOGS_DIR = "logs"
    
    # Configuración de logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Sitios disponibles
    AVAILABLE_SITES = {
        'MLA': 'Argentina',
        'MLB': 'Brasil', 
        'MLC': 'Chile',
        'MCO': 'Colombia',
        'MCR': 'Costa Rica',
        'MEC': 'Ecuador',
        'MLM': 'México',
        'MLU': 'Uruguay',
        'MLV': 'Venezuela'
    }
    
    # Condiciones de productos
    PRODUCT_CONDITIONS = {
        'new': 'Nuevo',
        'used': 'Usado',
        'not_specified': 'No especificado'
    }
    
    # Tipos de ordenamiento
    SORT_OPTIONS = {
        'relevance': 'Relevancia',
        'price_asc': 'Precio: menor a mayor',
        'price_desc': 'Precio: mayor a menor'
    }
    
    @classmethod
    def get_site_name(cls, site_id: str) -> str:
        """Obtiene el nombre del sitio por su ID"""
        return cls.AVAILABLE_SITES.get(site_id, site_id)
    
    @classmethod
    def is_authenticated(cls) -> bool:
        """Verifica si hay credenciales configuradas"""
        return bool(cls.MELI_CLIENT_ID and cls.MELI_CLIENT_SECRET)
    
    @classmethod
    def get_config_summary(cls) -> Dict[str, Any]:
        """Obtiene un resumen de la configuración"""
        return {
            'site': cls.DEFAULT_SITE,
            'site_name': cls.get_site_name(cls.DEFAULT_SITE),
            'authenticated': cls.is_authenticated(),
            'cache_enabled': cls.CACHE_ENABLED,
            'rate_limit': f"{cls.REQUESTS_PER_MINUTE}/min",
            'default_limit': cls.DEFAULT_LIMIT
        }
    
    @classmethod
    def validate_config(cls) -> Dict[str, bool]:
        """Valida la configuración"""
        validations = {
            'site_valid': cls.DEFAULT_SITE in cls.AVAILABLE_SITES,
            'limit_valid': 1 <= cls.DEFAULT_LIMIT <= 50,
            'rate_limit_valid': cls.REQUESTS_PER_MINUTE > 0,
            'delay_valid': cls.DELAY_BETWEEN_REQUESTS >= 0,
            'cache_ttl_valid': cls.CACHE_TTL > 0
        }
        
        return validations

# Instancia global de configuración
config = Config()
