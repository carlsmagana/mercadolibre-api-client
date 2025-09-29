# 🤝 Contribuir al Proyecto

¡Gracias por tu interés en contribuir al Cliente de MercadoLibre API! 

## 🚀 Cómo Contribuir

### 1. Fork del Repositorio
```bash
# Fork en GitHub y luego clona tu fork
git clone https://github.com/tu-usuario/mercadolibre-api-client.git
cd mercadolibre-api-client
```

### 2. Configurar Entorno de Desarrollo
```bash
# Instalar dependencias
python3 -m pip install -r requirements.txt

# Ejecutar pruebas
python3 test_client.py

# Probar funcionalidad
python3 simple_cli.py search "test" --limit 3
```

### 3. Crear Rama para tu Feature
```bash
git checkout -b feature/nueva-funcionalidad
```

### 4. Hacer Cambios
- Mantén el código limpio y bien documentado
- Agrega pruebas para nuevas funcionalidades
- Actualiza la documentación si es necesario

### 5. Ejecutar Pruebas
```bash
# Pruebas unitarias
python3 test_client.py

# Pruebas de integración
python3 simple_cli.py demo
```

### 6. Commit y Push
```bash
git add .
git commit -m "feat: descripción clara del cambio"
git push origin feature/nueva-funcionalidad
```

### 7. Crear Pull Request
- Describe claramente los cambios
- Incluye capturas de pantalla si es relevante
- Menciona issues relacionados

## 📋 Tipos de Contribuciones

### 🐛 Reportar Bugs
- Usa el template de issue para bugs
- Incluye pasos para reproducir
- Especifica tu entorno (OS, Python version)

### ✨ Nuevas Funcionalidades
- Discute la idea en un issue primero
- Mantén la compatibilidad hacia atrás
- Agrega documentación

### 📚 Documentación
- Mejoras en README.md
- Ejemplos adicionales
- Correcciones de typos

### 🧪 Pruebas
- Aumentar cobertura de pruebas
- Pruebas de casos edge
- Pruebas de rendimiento

## 🎨 Estilo de Código

### Python
- Seguir PEP 8
- Usar type hints cuando sea posible
- Documentar funciones con docstrings
- Nombres descriptivos para variables

### Commits
- Usar conventional commits
- `feat:` para nuevas funcionalidades
- `fix:` para correcciones
- `docs:` para documentación
- `test:` para pruebas

## 🔍 Proceso de Review

1. **Automated Tests**: Deben pasar todas las pruebas
2. **Code Review**: Al menos un maintainer debe aprobar
3. **Documentation**: Cambios deben estar documentados
4. **Backwards Compatibility**: No romper APIs existentes

## 🆘 ¿Necesitas Ayuda?

- 💬 Abre un issue con la etiqueta `question`
- 📧 Contacta a los maintainers
- 📚 Revisa la documentación existente

## 📜 Código de Conducta

- Sé respetuoso con otros contribuidores
- Acepta críticas constructivas
- Enfócate en lo que es mejor para la comunidad
- Mantén un ambiente inclusivo y acogedor

¡Gracias por contribuir! 🎉
