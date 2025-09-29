#!/usr/bin/env python3
"""
CLI simplificado para el cliente público de MercadoLibre
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime
from public_client import create_public_client

console = Console()

@click.group()
def cli():
    """🛒 Cliente Público de MercadoLibre
    
    Herramienta simplificada para explorar productos de MercadoLibre.
    
    Nota: Debido a cambios en las políticas de MercadoLibre, 
    este cliente usa métodos alternativos y puede mostrar datos de ejemplo.
    """
    pass

@cli.command()
@click.argument('query')
@click.option('--limit', '-l', default=10, help='Número de resultados')
@click.option('--export', '-e', help='Exportar a archivo JSON')
def search(query, limit, export):
    """Busca productos en MercadoLibre"""
    
    console.print(f"\n🔍 [bold blue]Buscando: '{query}'[/bold blue]")
    console.print(f"📊 Límite: {limit}")
    
    try:
        with create_public_client() as client:
            products = client.search_products_public(query, limit)
            
            if products:
                console.print(f"\n✅ [bold green]Encontrados {len(products)} productos[/bold green]")
                
                # Crear tabla
                table = Table(title=f"Resultados para '{query}'")
                table.add_column("ID", style="cyan", no_wrap=True)
                table.add_column("Título", style="white", max_width=35)
                table.add_column("Precio", style="green", justify="right")
                table.add_column("Vendidos", style="magenta", justify="right")
                table.add_column("Envío", style="blue")
                
                for product in products:
                    shipping = "✅ Gratis" if product.free_shipping else "💰 Pago"
                    condition_short = "new" if product.condition == "new" else "used" if product.condition == "used" else "n/a"
                    
                    table.add_row(
                        product.id,
                        product.title[:32] + "..." if len(product.title) > 35 else product.title,
                        f"${product.price:,.2f}",
                        f"{product.sold_quantity:,}",
                        shipping
                    )
                
                console.print(table)
                
                # Generar archivos de salida automáticamente
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                query_clean = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
                
                # Exportar JSON
                json_filename = f"{query_clean}_{timestamp}.json"
                client.export_to_json(products, json_filename)
                
                # Exportar CSV
                csv_filename = f"{query_clean}_{timestamp}.csv"
                try:
                    import pandas as pd
                    import os
                    
                    os.makedirs('exports', exist_ok=True)
                    csv_filepath = f"exports/{csv_filename}"
                    
                    # Convertir productos a DataFrame
                    data = []
                    for product in products:
                        data.append({
                            'id': product.id,
                            'titulo': product.title,
                            'precio': product.price,
                            'moneda': product.currency,
                            'url': product.permalink,
                            'imagen': product.thumbnail,
                            'condicion': product.condition,
                            'vendedor_id': product.seller_id,
                            'categoria_id': product.category_id,
                            'envio_gratis': product.free_shipping,
                            'cantidad_vendida': product.sold_quantity
                        })
                    
                    df = pd.DataFrame(data)
                    df.to_csv(csv_filepath, index=False, encoding='utf-8')
                    
                    console.print(f"\n💾 [bold green]Archivos generados:[/bold green]")
                    console.print(f"   📄 JSON: exports/{json_filename}")
                    console.print(f"   📊 CSV:  exports/{csv_filename}")
                    
                except ImportError:
                    console.print(f"\n💾 [bold green]Archivo generado:[/bold green]")
                    console.print(f"   📄 JSON: exports/{json_filename}")
                    console.print(f"   ⚠️  CSV no disponible (requiere pandas)")
                
                # Exportar adicional si se especifica nombre personalizado
                if export:
                    custom_filename = f"{export}_{timestamp}.json"
                    client.export_to_json(products, custom_filename)
                    console.print(f"   📄 Personalizado: exports/{custom_filename}")
                
            else:
                console.print("\n❌ [bold red]No se encontraron productos[/bold red]")
                
    except Exception as e:
        console.print(f"\n❌ [bold red]Error: {str(e)}[/bold red]")

@cli.command()
def categories():
    """Lista categorías disponibles"""
    
    console.print("\n📂 [bold blue]Categorías Principales[/bold blue]")
    
    try:
        with create_public_client() as client:
            categories = client.get_categories_public()
            
            if categories:
                table = Table(title="Categorías")
                table.add_column("ID", style="cyan")
                table.add_column("Nombre", style="white")
                
                for category in categories:
                    table.add_row(
                        category.get('id', 'N/A'),
                        category.get('name', 'N/A')
                    )
                
                console.print(table)
            else:
                console.print("❌ No se pudieron obtener categorías")
                
    except Exception as e:
        console.print(f"❌ Error: {str(e)}")

@cli.command()
def demo():
    """Ejecuta una demostración completa"""
    
    console.print("\n🎬 [bold blue]Demostración del Cliente Público[/bold blue]")
    console.print("=" * 50)
    
    queries = ["iPhone", "MacBook", "Samsung Galaxy", "iPad"]
    
    for query in queries:
        console.print(f"\n🔍 Buscando: [bold]{query}[/bold]")
        
        try:
            with create_public_client() as client:
                products = client.search_products_public(query, 3)
                
                if products:
                    console.print(f"✅ {len(products)} productos encontrados")
                    
                    for i, product in enumerate(products, 1):
                        console.print(f"  {i}. {product.title[:50]}...")
                        console.print(f"     💰 ${product.price:,.2f}")
                else:
                    console.print("❌ Sin resultados")
                    
        except Exception as e:
            console.print(f"❌ Error: {str(e)}")
    
    console.print(f"\n🎉 [bold green]Demostración completada[/bold green]")

@cli.command()
def info():
    """Muestra información sobre el cliente"""
    
    info_text = """
🛒 Cliente Público de MercadoLibre

📋 Características:
• Búsqueda de productos sin autenticación
• Exploración de categorías
• Exportación a JSON
• Interfaz colorida con Rich

⚠️  Limitaciones:
• MercadoLibre requiere autenticación para APIs completas
• Algunos datos pueden ser ejemplos
• Funcionalidad limitada comparada con APIs oficiales

💡 Para acceso completo:
• Registra tu aplicación en: https://developers.mercadolibre.com.mx/
• Usa el cliente completo con credenciales

🚀 Comandos disponibles:
• search "término" - Buscar productos
• categories - Listar categorías  
• demo - Ejecutar demostración
• info - Esta información
    """
    
    console.print(Panel(info_text, title="ℹ️  Información del Cliente"))

if __name__ == '__main__':
    cli()
