#!/usr/bin/env python3
"""
Script de instalación y configuración para el cliente de MercadoLibre API
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Muestra el banner de instalación"""
    print("🛒" + "=" * 60 + "🛒")
    print("    CLIENTE OFICIAL DE MERCADOLIBRE API - INSTALACIÓN")
    print("🛒" + "=" * 60 + "🛒")
    print()

def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando versión de Python...")
    
    if sys.version_info < (3, 7):
        print("❌ Error: Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def install_dependencies():
    """Instala las dependencias del proyecto"""
    print("\n📦 Instalando dependencias...")
    
    try:
        # Verificar si pip está disponible
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        
        # Instalar dependencias
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        
        print("✅ Dependencias instaladas correctamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False
    except FileNotFoundError:
        print("❌ Error: pip no encontrado")
        return False

def setup_environment():
    """Configura el archivo de entorno"""
    print("\n🔧 Configurando entorno...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ Archivo .env ya existe")
        return True
    
    if env_example.exists():
        # Copiar .env.example a .env
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Archivo .env creado desde plantilla")
        print("📝 Puedes editar .env para personalizar la configuración")
        return True
    else:
        print("⚠️  Archivo .env.example no encontrado")
        return False

def create_directories():
    """Crea directorios necesarios"""
    print("\n📁 Creando directorios...")
    
    directories = ['exports', 'cache', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directorio '{directory}' creado")

def test_installation():
    """Prueba la instalación"""
    print("\n🧪 Probando instalación...")
    
    try:
        # Importar el cliente
        from mercadolibre_client import create_client
        
        # Probar conexión básica
        with create_client() as client:
            categories = client.get_categories()
            
        print(f"✅ Conexión exitosa - {len(categories)} categorías encontradas")
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def show_usage_examples():
    """Muestra ejemplos de uso"""
    print("\n📚 EJEMPLOS DE USO:")
    print("-" * 40)
    
    examples = [
        ("Búsqueda básica", "python cli.py search 'iPhone 15'"),
        ("Búsqueda avanzada", "python cli.py search 'MacBook Pro' --limit 20 --export json"),
        ("Detalles de producto", "python cli.py product MLM123456789 --details"),
        ("Listar categorías", "python cli.py categories"),
        ("Ejecutar ejemplos", "python examples.py"),
    ]
    
    for description, command in examples:
        print(f"• {description}:")
        print(f"  {command}")
        print()

def main():
    """Función principal de instalación"""
    print_banner()
    
    # Verificaciones
    if not check_python_version():
        sys.exit(1)
    
    # Instalación
    steps = [
        ("Instalar dependencias", install_dependencies),
        ("Configurar entorno", setup_environment),
        ("Crear directorios", create_directories),
        ("Probar instalación", test_installation),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Falló: {step_name}")
            sys.exit(1)
    
    # Éxito
    print("\n🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 50)
    
    show_usage_examples()
    
    print("📖 Para más información, consulta README.md")
    print("🔗 Documentación oficial: https://developers.mercadolibre.com.mx/")
    print("\n🚀 ¡Listo para usar las APIs oficiales de MercadoLibre!")

if __name__ == "__main__":
    main()
