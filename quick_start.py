#!/usr/bin/env python3
"""
🚀 Guía de inicio rápido para el Cliente de MercadoLibre API

Este script te guía paso a paso para comenzar a usar el cliente.
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
import os
import sys

console = Console()

def show_welcome():
    """Muestra mensaje de bienvenida"""
    welcome_text = """
🛒 ¡Bienvenido al Cliente de MercadoLibre API!

Este asistente te ayudará a configurar y usar el cliente paso a paso.

📋 Lo que haremos:
1. Verificar instalación
2. Configurar el cliente
3. Ejecutar primera búsqueda
4. Mostrar ejemplos avanzados
    """
    
    console.print(Panel(welcome_text, title="🚀 Inicio Rápido", border_style="blue"))

def check_installation():
    """Verifica que todo esté instalado correctamente"""
    console.print("\n🔍 [bold blue]Paso 1: Verificando instalación[/bold blue]")
    
    try:
        # Verificar imports
        from public_client import create_public_client
        from mercadolibre_client import MercadoLibreClient
        import requests
        import rich
        
        console.print("✅ Todas las dependencias están instaladas")
        
        # Verificar estructura de archivos
        required_files = [
            'mercadolibre_client.py',
            'public_client.py', 
            'cli.py',
            'simple_cli.py',
            'examples.py',
            'requirements.txt'
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            console.print(f"⚠️  Archivos faltantes: {', '.join(missing_files)}")
            return False
        else:
            console.print("✅ Todos los archivos están presentes")
            return True
            
    except ImportError as e:
        console.print(f"❌ Error de importación: {e}")
        console.print("💡 Ejecuta: pip install -r requirements.txt")
        return False

def configure_client():
    """Configura el cliente"""
    console.print("\n⚙️ [bold blue]Paso 2: Configuración[/bold blue]")
    
    # Verificar archivo .env
    if os.path.exists('.env'):
        console.print("✅ Archivo .env encontrado")
    else:
        console.print("📝 Creando archivo .env...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)
            console.print("✅ Archivo .env creado desde plantilla")
        else:
            console.print("⚠️  .env.example no encontrado")
    
    # Preguntar sobre credenciales
    has_credentials = Confirm.ask("¿Tienes credenciales de MercadoLibre API?")
    
    if has_credentials:
        console.print("\n📋 Para configurar credenciales:")
        console.print("1. Edita el archivo .env")
        console.print("2. Agrega tu MELI_CLIENT_ID y MELI_CLIENT_SECRET")
        console.print("3. Reinicia este script")
        console.print("\n🔗 Obtén credenciales en: https://developers.mercadolibre.com.mx/")
    else:
        console.print("✅ Usaremos el cliente público (funcionalidad limitada)")
    
    return not has_credentials

def run_first_search(use_public_client=True):
    """Ejecuta la primera búsqueda"""
    console.print("\n🔍 [bold blue]Paso 3: Primera búsqueda[/bold blue]")
    
    # Pedir término de búsqueda
    query = Prompt.ask("¿Qué producto quieres buscar?", default="iPhone")
    limit = int(Prompt.ask("¿Cuántos resultados?", default="5"))
    
    console.print(f"\n🚀 Buscando '{query}'...")
    
    try:
        if use_public_client:
            from public_client import create_public_client
            
            with create_public_client() as client:
                products = client.search_products_public(query, limit)
                
                if products:
                    console.print(f"\n✅ [bold green]¡Encontrados {len(products)} productos![/bold green]")
                    
                    # Mostrar resultados en tabla
                    table = Table(title=f"Resultados para '{query}'")
                    table.add_column("Título", style="white", max_width=40)
                    table.add_column("Precio", style="green", justify="right")
                    table.add_column("Condición", style="yellow")
                    
                    for product in products:
                        table.add_row(
                            product.title[:37] + "..." if len(product.title) > 40 else product.title,
                            f"${product.price:,.2f}",
                            product.condition
                        )
                    
                    console.print(table)
                    
                    # Preguntar si exportar
                    export = Confirm.ask("¿Quieres exportar los resultados?")
                    if export:
                        filename = f"{query.replace(' ', '_')}_resultados"
                        client.export_to_json(products, f"{filename}.json")
                        console.print(f"💾 Exportado a: exports/{filename}.json")
                
                else:
                    console.print("❌ No se encontraron productos")
        
        return True
        
    except Exception as e:
        console.print(f"❌ Error: {str(e)}")
        return False

def show_next_steps():
    """Muestra los próximos pasos"""
    console.print("\n🎯 [bold blue]Paso 4: Próximos pasos[/bold blue]")
    
    next_steps = """
🚀 ¡Felicidades! Ya tienes el cliente funcionando.

📚 Comandos útiles:

• Búsqueda simple:
  python3 simple_cli.py search "MacBook Pro" --limit 10

• Búsqueda avanzada:
  python3 cli.py search "iPhone 15" --condition new --export json

• Ver categorías:
  python3 simple_cli.py categories

• Ejecutar demostración:
  python3 simple_cli.py demo

• Ejemplos programáticos:
  python3 examples.py

📖 Documentación completa:
  Revisa README.md para guías detalladas

🔗 APIs oficiales:
  https://developers.mercadolibre.com.mx/

💡 Para funcionalidad completa:
  1. Registra tu aplicación en MercadoLibre
  2. Configura credenciales en .env
  3. Usa cli.py en lugar de simple_cli.py
    """
    
    console.print(Panel(next_steps, title="🎉 ¡Listo para usar!", border_style="green"))

def main():
    """Función principal del inicio rápido"""
    console.clear()
    show_welcome()
    
    # Paso 1: Verificar instalación
    if not check_installation():
        console.print("\n❌ [bold red]Instalación incompleta[/bold red]")
        console.print("💡 Ejecuta: python3 setup.py")
        return
    
    # Paso 2: Configurar
    use_public = configure_client()
    
    # Paso 3: Primera búsqueda
    if run_first_search(use_public):
        # Paso 4: Próximos pasos
        show_next_steps()
    
    console.print("\n🎉 [bold green]¡Inicio rápido completado![/bold green]")
    console.print("💬 ¿Preguntas? Revisa la documentación en README.md")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n👋 ¡Hasta luego!")
    except Exception as e:
        console.print(f"\n❌ Error inesperado: {e}")
        console.print("💡 Reporta este error si persiste")
