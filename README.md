# 🛒 Cliente Oficial de MercadoLibre API

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/carlsmagana/mercadolibre-api-client/workflows/Tests/badge.svg)](https://github.com/carlsmagana/mercadolibre-api-client/actions)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](VERSION)
[![GitHub stars](https://img.shields.io/github/stars/carlsmagana/mercadolibre-api-client.svg)](https://github.com/carlsmagana/mercadolibre-api-client/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/carlsmagana/mercadolibre-api-client.svg)](https://github.com/carlsmagana/mercadolibre-api-client/network)
[![GitHub issues](https://img.shields.io/github/issues/carlsmagana/mercadolibre-api-client.svg)](https://github.com/carlsmagana/mercadolibre-api-client/issues)

Un cliente Python completo y fácil de usar para interactuar con las APIs oficiales de MercadoLibre. Permite buscar productos, obtener detalles, explorar categorías y exportar datos de manera eficiente y respetando los límites de la API.

![Demo](https://via.placeholder.com/800x400/2196F3/FFFFFF?text=MercadoLibre+API+Client+Demo)

## 🚀 Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/carlsmagana/mercadolibre-api-client.git
cd mercadolibre-api-client

# Instalar dependencias
pip install -r requirements.txt

# ¡Usar inmediatamente!
python3 simple_cli.py search "iPhone 15" --limit 5
```

## ✨ Características

- 🔍 **Búsqueda avanzada** de productos con filtros
- 📊 **Paginación automática** para obtener grandes cantidades de datos
- 🏷️ **Exploración de categorías** y subcategorías
- 👤 **Información de vendedores** y reputación
- 📈 **Rate limiting automático** para respetar los límites de la API
- 💾 **Exportación** a JSON y CSV
- 🎨 **CLI colorida** con Rich
- 🔧 **Configuración flexible** con variables de entorno
- 📚 **Documentación completa** y ejemplos

## 🚀 Instalación

### Requisitos

- Python 3.7+
- Conexión a internet

### Instalación rápida

```bash
# Clonar el proyecto
git clone <repository-url>
cd mercadolibre-api-client

# Instalar dependencias
pip install -r requirements.txt

# Configurar (opcional)
python cli.py setup
```

### Instalación manual

```bash
pip install requests python-dotenv pandas click rich pydantic httpx
```

## 🔑 Configuración

### APIs Públicas (No requiere autenticación)

La mayoría de las funciones funcionan sin autenticación:
- Búsqueda de productos
- Detalles de productos
- Categorías
- Información básica de vendedores

### APIs Avanzadas (Requiere registro)

Para funciones avanzadas, registra tu aplicación en:
👉 https://developers.mercadolibre.com.mx/

Luego configura tus credenciales:

```bash
# Copiar plantilla de configuración
cp .env.example .env

# Editar .env con tus credenciales
MELI_CLIENT_ID=tu_client_id
MELI_CLIENT_SECRET=tu_client_secret
```

## 📖 Uso

### CLI (Línea de Comandos)

#### Búsqueda básica
```bash
python cli.py search "iPhone 15"
```

#### Búsqueda avanzada
```bash
# Buscar con filtros
python cli.py search "MacBook Pro" --limit 20 --condition new --sort price_asc

# Múltiples páginas
python cli.py search "Samsung Galaxy" --pages 3 --export json

# Por categoría
python cli.py search "laptop" --category MLM1652 --limit 30
```

#### Detalles de producto
```bash
# Información básica
python cli.py product MLM123456789

# Detalles completos
python cli.py product MLM123456789 --details --description
```

#### Explorar categorías
```bash
# Listar todas las categorías
python cli.py categories

# Detalles de una categoría específica
python cli.py category MLM1652
```

### Uso Programático

#### Búsqueda básica
```python
from mercadolibre_client import create_client

# Crear cliente
with create_client() as client:
    # Buscar productos
    response = client.search_products("iPhone 15", limit=20)
    
    # Procesar resultados
    for item in response['results']:
        print(f"{item['title']} - ${item['price']}")
```

#### Búsqueda avanzada con múltiples páginas
```python
from mercadolibre_client import MercadoLibreClient, Product

with MercadoLibreClient() as client:
    # Obtener hasta 500 productos
    products = client.search_all_pages(
        query="MacBook Pro",
        max_results=500,
        condition="new"
    )
    
    # Análisis de datos
    prices = [p.price for p in products]
    avg_price = sum(prices) / len(prices)
    
    print(f"Precio promedio: ${avg_price:,.2f}")
```

#### Detalles de producto
```python
with create_client() as client:
    # Obtener detalles completos
    product = client.get_product_details("MLM123456789")
    
    print(f"Título: {product['title']}")
    print(f"Precio: ${product['price']}")
    print(f"Vendidos: {product.get('sold_quantity', 0)}")
    
    # Obtener descripción
    description = client.get_product_description("MLM123456789")
    print(f"Descripción: {description['plain_text']}")
```

#### Exportar datos
```python
with create_client() as client:
    # Buscar productos
    products = client.search_all_pages("iPad Pro", max_results=100)
    
    # Exportar a JSON
    client.export_to_json(products, "ipad_pro_products.json")
    
    # Exportar a CSV
    client.export_to_csv(products, "ipad_pro_products.csv")
```

## 📊 Ejemplos Avanzados

### Análisis de mercado
```python
from mercadolibre_client import create_client
import statistics

with create_client() as client:
    # Analizar precios de iPhones
    products = client.search_all_pages("iPhone", max_results=200)
    
    # Filtrar por modelo
    iphone_15 = [p for p in products if "iPhone 15" in p.title]
    
    # Estadísticas de precios
    prices = [p.price for p in iphone_15 if p.price > 0]
    
    print(f"Productos analizados: {len(iphone_15)}")
    print(f"Precio promedio: ${statistics.mean(prices):,.2f}")
    print(f"Precio mediano: ${statistics.median(prices):,.2f}")
    print(f"Rango: ${min(prices):,.2f} - ${max(prices):,.2f}")
```

### Comparación de vendedores
```python
with create_client() as client:
    # Buscar productos de una categoría
    response = client.search_products("laptop gaming", limit=50)
    
    # Agrupar por vendedor
    sellers = {}
    for item in response['results']:
        seller_id = item.get('seller', {}).get('id')
        if seller_id:
            if seller_id not in sellers:
                sellers[seller_id] = []
            sellers[seller_id].append(item)
    
    # Analizar cada vendedor
    for seller_id, products in sellers.items():
        avg_price = sum(p['price'] for p in products) / len(products)
        total_sales = sum(p.get('sold_quantity', 0) for p in products)
        
        print(f"Vendedor {seller_id}:")
        print(f"  Productos: {len(products)}")
        print(f"  Precio promedio: ${avg_price:,.2f}")
        print(f"  Ventas totales: {total_sales}")
```

## 🏗️ Estructura del Proyecto

```
mercadolibre-api-client/
├── mercadolibre_client.py    # Cliente principal de la API
├── cli.py                    # Interfaz de línea de comandos
├── examples.py               # Ejemplos de uso
├── requirements.txt          # Dependencias
├── .env.example             # Plantilla de configuración
├── .gitignore               # Archivos a ignorar
├── README.md                # Documentación
└── exports/                 # Archivos exportados
    ├── *.json
    └── *.csv
```

## 🔧 Configuración Avanzada

### Variables de entorno (.env)

```bash
# Credenciales de API (opcional)
MELI_CLIENT_ID=your_client_id
MELI_CLIENT_SECRET=your_client_secret

# Configuración del cliente
DEFAULT_SITE=MLM              # Sitio por defecto
DEFAULT_LIMIT=50              # Límite por defecto
CACHE_ENABLED=true            # Habilitar cache
CACHE_TTL=3600               # Tiempo de vida del cache

# Rate limiting
REQUESTS_PER_MINUTE=60        # Requests por minuto
DELAY_BETWEEN_REQUESTS=1.0    # Delay entre requests
```

### Sitios disponibles

| Código | País |
|--------|------|
| MLA | Argentina |
| MLB | Brasil |
| MLC | Chile |
| MCO | Colombia |
| MCR | Costa Rica |
| MEC | Ecuador |
| MLM | México |
| MLU | Uruguay |
| MLV | Venezuela |

## 📚 Referencia de la API

### Clase MercadoLibreClient

#### Métodos principales

- `search_products(query, limit, offset, category, condition, sort)` - Buscar productos
- `search_all_pages(query, max_results, category, condition)` - Búsqueda con paginación
- `get_product_details(product_id)` - Detalles de producto
- `get_product_description(product_id)` - Descripción de producto
- `get_categories()` - Listar categorías
- `get_category_details(category_id)` - Detalles de categoría
- `get_seller_info(seller_id)` - Información de vendedor
- `export_to_json(products, filename)` - Exportar a JSON
- `export_to_csv(products, filename)` - Exportar a CSV

#### Parámetros de búsqueda

- `query`: Término de búsqueda
- `limit`: Número de resultados (máximo 50)
- `offset`: Desplazamiento para paginación
- `category`: ID de categoría
- `condition`: `new`, `used`, `not_specified`
- `sort`: `relevance`, `price_asc`, `price_desc`

### Clase Product

Representa un producto con los siguientes atributos:

- `id`: ID del producto
- `title`: Título
- `price`: Precio
- `currency_id`: Moneda
- `permalink`: URL del producto
- `thumbnail`: Imagen miniatura
- `condition`: Condición
- `available_quantity`: Cantidad disponible
- `sold_quantity`: Cantidad vendida
- `free_shipping`: Envío gratis (boolean)
- `seller_id`: ID del vendedor

## 🚨 Límites y Mejores Prácticas

### Límites de la API

- **Requests por hora**: 10,000 (sin autenticación)
- **Requests por hora**: 20,000 (con autenticación)
- **Resultados por página**: Máximo 50
- **Timeout**: 30 segundos por request

### Mejores prácticas

1. **Rate limiting**: El cliente implementa delays automáticos
2. **Manejo de errores**: Siempre usar try/catch
3. **Paginación**: Usar `search_all_pages()` para grandes datasets
4. **Cache**: Habilitar cache para consultas repetitivas
5. **Exportación**: Procesar y exportar datos en lotes

## 🐛 Solución de Problemas

### Errores comunes

#### Error 429 (Rate Limit)
```
Error: Too Many Requests
```
**Solución**: El cliente maneja esto automáticamente esperando 1 minuto.

#### Error de conexión
```
Error: Connection timeout
```
**Solución**: Verificar conexión a internet y reintentar.

#### Producto no encontrado
```
Error: Item not found
```
**Solución**: Verificar que el ID del producto sea válido.

### Debug

Habilitar logging detallado:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🔗 Enlaces Útiles

- [Documentación oficial de MercadoLibre API](https://developers.mercadolibre.com.mx/)
- [Registro de aplicaciones](https://developers.mercadolibre.com.mx/application)
- [Referencia de la API](https://developers.mercadolibre.com.mx/es_ar/api-docs-es)
- [Códigos de país](https://api.mercadolibre.com/sites)

## 📞 Soporte

- 📧 Email: [tu-email@ejemplo.com]
- 🐛 Issues: [GitHub Issues](link-to-issues)
- 📖 Wiki: [GitHub Wiki](link-to-wiki)

---

⭐ Si este proyecto te fue útil, ¡dale una estrella en GitHub!

🚀 **¡Feliz scraping con las APIs oficiales de MercadoLibre!**
