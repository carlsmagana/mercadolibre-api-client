# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

## [1.0.0] - 2024-09-29

### Agregado
- ✨ Cliente completo para APIs oficiales de MercadoLibre
- 🔍 Búsqueda avanzada de productos con filtros
- 📊 Paginación automática para grandes datasets
- 🏷️ Exploración de categorías y subcategorías
- 👤 Información de vendedores y reputación
- 📈 Rate limiting automático
- 💾 Exportación a JSON y CSV
- 🎨 CLI colorida con Rich
- 🔧 Configuración flexible con variables de entorno
- 📚 Documentación completa y ejemplos
- 🛡️ Cliente público alternativo para casos sin autenticación

### Características Principales
- **Búsqueda de productos**: Búsqueda con múltiples filtros y ordenamiento
- **Detalles de productos**: Información completa incluyendo atributos y descripción
- **Categorías**: Exploración de categorías principales y subcategorías
- **Vendedores**: Información y reputación de vendedores
- **Exportación**: Datos en formato JSON y CSV
- **CLI**: Interfaz de línea de comandos intuitiva
- **Ejemplos**: Scripts de ejemplo para diferentes casos de uso

### Estructura del Proyecto
```
mercadolibre-api-client/
├── mercadolibre_client.py    # Cliente principal (requiere autenticación)
├── public_client.py          # Cliente público alternativo
├── cli.py                    # CLI completa
├── simple_cli.py             # CLI simplificada
├── examples.py               # Ejemplos de uso
├── setup.py                  # Script de instalación
├── requirements.txt          # Dependencias
├── .env.example             # Plantilla de configuración
├── README.md                # Documentación principal
├── CHANGELOG.md             # Este archivo
├── LICENSE                  # Licencia MIT
└── .gitignore              # Archivos a ignorar
```

### Comandos CLI Disponibles

#### CLI Completa (`cli.py`)
- `search` - Búsqueda avanzada con filtros
- `product` - Detalles de producto específico
- `categories` - Listar categorías
- `category` - Detalles de categoría específica
- `setup` - Configuración inicial

#### CLI Simplificada (`simple_cli.py`)
- `search` - Búsqueda básica
- `categories` - Listar categorías
- `demo` - Demostración completa
- `info` - Información del cliente

### Ejemplos de Uso

```bash
# Búsqueda básica
python3 simple_cli.py search "iPhone 15" --limit 10

# Búsqueda avanzada con exportación
python3 cli.py search "MacBook Pro" --limit 20 --export json

# Demostración completa
python3 simple_cli.py demo

# Ejecutar ejemplos programáticos
python3 examples.py
```

### Limitaciones Conocidas
- MercadoLibre requiere autenticación para APIs completas desde 2024
- El cliente público genera datos de ejemplo cuando no puede acceder a APIs reales
- Algunas funciones avanzadas requieren registro de aplicación

### Próximas Versiones
- [ ] Soporte para autenticación OAuth 2.0
- [ ] Cache inteligente de resultados
- [ ] Análisis de tendencias de precios
- [ ] Notificaciones de cambios de precio
- [ ] Integración con bases de datos
- [ ] API REST propia para el cliente

### Agradecimientos
- Equipo de MercadoLibre por las APIs públicas
- Comunidad de Python por las librerías utilizadas
- Usuarios beta por el feedback inicial
