# 🚀 Guía para Subir a GitHub

## 📋 Pasos para Crear el Repositorio en GitHub

### 1. Crear Repositorio en GitHub
1. Ve a https://github.com/new
2. **Repository name**: `mercadolibre-api-client`
3. **Description**: `🛒 Complete Python client for MercadoLibre official APIs with advanced analytics and export capabilities`
4. **Visibility**: Public (recomendado) o Private
5. **NO** marcar "Add a README file" (ya tenemos uno)
6. **NO** marcar "Add .gitignore" (ya tenemos uno)
7. **NO** marcar "Choose a license" (ya tenemos LICENSE)
8. Click "Create repository"

### 2. Conectar Repositorio Local con GitHub
```bash
# Agregar remote origin (reemplaza 'tu-usuario' con tu username de GitHub)
git remote add origin https://github.com/tu-usuario/mercadolibre-api-client.git

# Verificar remote
git remote -v

# Subir código y tags
git push -u origin main
git push origin --tags
```

### 3. Configurar Repositorio en GitHub

#### A. Configurar About Section
- Ve a tu repositorio en GitHub
- Click en ⚙️ (Settings) en la sección "About"
- **Description**: `🛒 Complete Python client for MercadoLibre official APIs with advanced analytics and export capabilities`
- **Website**: (opcional)
- **Topics**: `python`, `mercadolibre`, `api-client`, `data-analysis`, `ecommerce`, `scraping`, `analytics`

#### B. Configurar Branch Protection (Opcional)
1. Ve a Settings > Branches
2. Add rule para `main`
3. Marcar "Require pull request reviews before merging"

#### C. Habilitar Issues y Discussions
1. Ve a Settings > General
2. En "Features" asegurar que estén habilitados:
   - ✅ Issues
   - ✅ Discussions (opcional)
   - ✅ Wiki (opcional)

### 4. Crear Release en GitHub
1. Ve a tu repositorio
2. Click en "Releases" (lado derecho)
3. Click "Create a new release"
4. **Tag version**: `v1.0.0`
5. **Release title**: `🎉 v1.0.0 - Complete MercadoLibre API Client`
6. **Description**:
```markdown
## 🚀 First Stable Release

### ✨ Features
- 🔍 Complete API client for MercadoLibre official APIs
- 📊 Advanced product search with filters and pagination
- 💾 Automatic export to JSON and CSV formats
- 📈 Sales quantity tracking and analytics
- 🔧 Multiple CLI interfaces (simple and advanced)
- 📋 Product comparison utilities
- 🧪 Comprehensive test suite
- 📚 Professional documentation

### 🛠️ Installation
```bash
git clone https://github.com/tu-usuario/mercadolibre-api-client.git
cd mercadolibre-api-client
pip install -r requirements.txt
python3 simple_cli.py search "iPhone 15" --limit 5
```

### 📊 What's Included
- **25+ commands** available
- **10+ analysis types**
- **3 export formats**
- **9 countries** supported
- **Ready for production** use

### 🎯 Perfect for
- Market research and analysis
- Price monitoring and comparison
- Competitive intelligence
- Data export for Excel/Sheets
- Academic research
```

7. **Assets**: Los archivos se subirán automáticamente
8. Click "Publish release"

## 🔧 Comandos de Git Útiles

### Verificar Estado
```bash
git status
git log --oneline
git tag
```

### Actualizar Repositorio
```bash
# Hacer cambios
git add .
git commit -m "feat: nueva funcionalidad"
git push origin main

# Crear nueva versión
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin --tags
```

### Clonar en Otra Máquina
```bash
git clone https://github.com/tu-usuario/mercadolibre-api-client.git
cd mercadolibre-api-client
pip install -r requirements.txt
```

## 📋 Checklist Final

- [ ] Repositorio creado en GitHub
- [ ] Código subido con `git push -u origin main`
- [ ] Tags subidos con `git push origin --tags`
- [ ] About section configurada
- [ ] Topics agregados
- [ ] Release v1.0.0 creada
- [ ] README.md se ve bien en GitHub
- [ ] Actions/Tests funcionando (opcional)

## 🎉 ¡Listo!

Tu repositorio estará disponible en:
`https://github.com/tu-usuario/mercadolibre-api-client`

### 📊 Badges para README
Después de subir, puedes actualizar los badges en README.md:
```markdown
[![Tests](https://github.com/tu-usuario/mercadolibre-api-client/workflows/Tests/badge.svg)](https://github.com/tu-usuario/mercadolibre-api-client/actions)
[![GitHub release](https://img.shields.io/github/release/tu-usuario/mercadolibre-api-client.svg)](https://github.com/tu-usuario/mercadolibre-api-client/releases)
[![GitHub stars](https://img.shields.io/github/stars/tu-usuario/mercadolibre-api-client.svg)](https://github.com/tu-usuario/mercadolibre-api-client/stargazers)
```
