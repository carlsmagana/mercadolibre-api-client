#!/usr/bin/env python3
"""
Interfaz de línea de comandos para el cliente de MercadoLibre API
"""

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
from datetime import datetime
import json
import os
from mercadolibre_client import MercadoLibreClient, Product

console = Console()

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """🛒 Cliente oficial de MercadoLibre API
    
    Herramienta para buscar y analizar productos usando las APIs oficiales de MercadoLibre.
    
    Ejemplos:
      meli search "iPhone 15" --limit 20
      meli product MLM123456789
      meli categories
    """
    pass

@cli.command()
@click.argument('query')
@click.option('--limit', '-l', default=50, help='Número de resultados (máximo 50 por página)')
@click.option('--pages', '-p', default=1, help='Número de páginas a obtener')
@click.option('--category', '-c', help='ID de categoría para filtrar')
@click.option('--condition', help='Condición: new, used, not_specified')
@click.option('--sort', default='relevance', help='Ordenamiento: relevance, price_asc, price_desc')
@click.option('--export', '-e', help='Exportar a archivo (json/csv)')
@click.option('--site', default='MLM', help='Sitio de MercadoLibre (MLM=México)')
def search(query, limit, pages, category, condition, sort, export, site):
    """Busca productos en MercadoLibre"""
    
    console.print(f"\n🔍 [bold blue]Buscando productos: '{query}'[/bold blue]")
    console.print(f"📍 Sitio: {site} | 📄 Páginas: {pages} | 📊 Límite: {limit}")
    
    if category:
        console.print(f"🏷️  Categoría: {category}")
    if condition:
        console.print(f"📦 Condición: {condition}")
    
    console.print()
    
    try:
        with MercadoLibreClient(site_id=site) as client:
            
            # Calcular total de resultados a obtener
            max_results = limit * pages
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                
                task = progress.add_task("Obteniendo productos...", total=None)
                
                if pages == 1:
                    # Búsqueda simple de una página
                    response = client.search_products(
                        query=query,
                        limit=limit,
                        category=category,
                        condition=condition,
                        sort=sort
                    )
                    
                    results = response.get('results', [])
                    products = [Product.from_api_response(item) for item in results]
                    total_found = response.get('paging', {}).get('total', 0)
                    
                else:
                    # Búsqueda de múltiples páginas
                    products = client.search_all_pages(
                        query=query,
                        max_results=max_results,
                        category=category,
                        condition=condition
                    )
                    total_found = len(products)
            
            # Mostrar resultados
            if products:
                console.print(f"\n✅ [bold green]Encontrados {len(products)} productos[/bold green]")
                console.print(f"📊 Total disponible: {total_found:,}")
                
                # Crear tabla de resultados
                table = Table(title=f"Resultados para '{query}'")
                table.add_column("ID", style="cyan", no_wrap=True)
                table.add_column("Título", style="white", max_width=50)
                table.add_column("Precio", style="green", justify="right")
                table.add_column("Condición", style="yellow")
                table.add_column("Vendidos", style="magenta", justify="right")
                table.add_column("Envío", style="blue")
                
                for product in products[:20]:  # Mostrar solo los primeros 20
                    sold_qty = str(product.sold_quantity) if product.sold_quantity else "N/A"
                    shipping = "✅ Gratis" if product.free_shipping else "💰 Pago"
                    
                    table.add_row(
                        product.id,
                        product.title[:47] + "..." if len(product.title) > 50 else product.title,
                        f"${product.price:,.2f} {product.currency_id}",
                        product.condition,
                        sold_qty,
                        shipping
                    )
                
                console.print(table)
                
                if len(products) > 20:
                    console.print(f"\n[dim]... y {len(products) - 20} productos más[/dim]")
                
                # Exportar si se solicita
                if export:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    query_clean = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
                    
                    if export.lower() == 'json':
                        filename = f"{query_clean}_{timestamp}.json"
                        client.export_to_json(products, filename)
                        console.print(f"\n💾 [bold green]Exportado a: exports/{filename}[/bold green]")
                    
                    elif export.lower() == 'csv':
                        filename = f"{query_clean}_{timestamp}.csv"
                        client.export_to_csv(products, filename)
                        console.print(f"\n💾 [bold green]Exportado a: exports/{filename}[/bold green]")
                
            else:
                console.print("\n❌ [bold red]No se encontraron productos[/bold red]")
                
    except Exception as e:
        console.print(f"\n❌ [bold red]Error: {str(e)}[/bold red]")

@cli.command()
@click.argument('product_id')
@click.option('--details', '-d', is_flag=True, help='Mostrar detalles completos')
@click.option('--description', is_flag=True, help='Incluir descripción del producto')
def product(product_id, details, description):
    """Obtiene información detallada de un producto específico"""
    
    console.print(f"\n🔍 [bold blue]Obteniendo información del producto: {product_id}[/bold blue]\n")
    
    try:
        with MercadoLibreClient() as client:
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                
                task = progress.add_task("Obteniendo detalles...", total=None)
                
                # Obtener detalles del producto
                product_data = client.get_product_details(product_id)
                
                # Obtener descripción si se solicita
                desc_data = None
                if description:
                    try:
                        desc_data = client.get_product_description(product_id)
                    except:
                        console.print("[yellow]⚠️  No se pudo obtener la descripción[/yellow]")
            
            # Mostrar información básica
            console.print(Panel.fit(
                f"[bold]{product_data.get('title', 'Sin título')}[/bold]\n\n"
                f"💰 Precio: ${product_data.get('price', 0):,.2f} {product_data.get('currency_id', 'MXN')}\n"
                f"📦 Condición: {product_data.get('condition', 'N/A')}\n"
                f"📊 Disponible: {product_data.get('available_quantity', 'N/A')}\n"
                f"🛒 Vendidos: {product_data.get('sold_quantity', 'N/A')}\n"
                f"🔗 URL: {product_data.get('permalink', 'N/A')}",
                title="📱 Información del Producto"
            ))
            
            if details:
                # Mostrar detalles adicionales
                attributes = product_data.get('attributes', [])
                if attributes:
                    console.print("\n📋 [bold]Atributos:[/bold]")
                    attr_table = Table()
                    attr_table.add_column("Atributo", style="cyan")
                    attr_table.add_column("Valor", style="white")
                    
                    for attr in attributes[:10]:  # Mostrar solo los primeros 10
                        attr_table.add_row(
                            attr.get('name', 'N/A'),
                            str(attr.get('value_name', attr.get('value_id', 'N/A')))
                        )
                    
                    console.print(attr_table)
                
                # Información del vendedor
                seller = product_data.get('seller', {})
                if seller:
                    console.print(f"\n👤 [bold]Vendedor:[/bold] {seller.get('id', 'N/A')}")
                    
                    reputation = seller.get('seller_reputation', {})
                    if reputation:
                        console.print(f"⭐ Reputación: {reputation.get('level_id', 'N/A')}")
            
            if desc_data:
                desc_text = desc_data.get('plain_text', desc_data.get('text', 'Sin descripción'))
                if desc_text:
                    console.print(Panel(
                        desc_text[:500] + "..." if len(desc_text) > 500 else desc_text,
                        title="📝 Descripción"
                    ))
                
    except Exception as e:
        console.print(f"\n❌ [bold red]Error: {str(e)}[/bold red]")

@cli.command()
@click.option('--site', default='MLM', help='Sitio de MercadoLibre')
def categories(site):
    """Lista todas las categorías disponibles"""
    
    console.print(f"\n📂 [bold blue]Categorías de {site}[/bold blue]\n")
    
    try:
        with MercadoLibreClient(site_id=site) as client:
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                
                task = progress.add_task("Obteniendo categorías...", total=None)
                categories_data = client.get_categories()
            
            if categories_data:
                table = Table(title="Categorías Principales")
                table.add_column("ID", style="cyan", no_wrap=True)
                table.add_column("Nombre", style="white")
                
                for category in categories_data:
                    table.add_row(
                        category.get('id', 'N/A'),
                        category.get('name', 'N/A')
                    )
                
                console.print(table)
                console.print(f"\n📊 [bold green]Total: {len(categories_data)} categorías[/bold green]")
                
            else:
                console.print("❌ [bold red]No se pudieron obtener las categorías[/bold red]")
                
    except Exception as e:
        console.print(f"\n❌ [bold red]Error: {str(e)}[/bold red]")

@cli.command()
@click.argument('category_id')
def category(category_id):
    """Obtiene información detallada de una categoría"""
    
    console.print(f"\n📂 [bold blue]Información de la categoría: {category_id}[/bold blue]\n")
    
    try:
        with MercadoLibreClient() as client:
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                
                task = progress.add_task("Obteniendo información...", total=None)
                category_data = client.get_category_details(category_id)
            
            console.print(Panel.fit(
                f"[bold]{category_data.get('name', 'Sin nombre')}[/bold]\n\n"
                f"🆔 ID: {category_data.get('id', 'N/A')}\n"
                f"📊 Total de productos: {category_data.get('total_items_in_this_category', 'N/A'):,}",
                title="📂 Información de la Categoría"
            ))
            
            # Subcategorías
            children = category_data.get('children_categories', [])
            if children:
                console.print("\n📁 [bold]Subcategorías:[/bold]")
                sub_table = Table()
                sub_table.add_column("ID", style="cyan")
                sub_table.add_column("Nombre", style="white")
                sub_table.add_column("Productos", style="green", justify="right")
                
                for child in children[:15]:  # Mostrar solo las primeras 15
                    sub_table.add_row(
                        child.get('id', 'N/A'),
                        child.get('name', 'N/A'),
                        f"{child.get('total_items_in_this_category', 0):,}"
                    )
                
                console.print(sub_table)
                
    except Exception as e:
        console.print(f"\n❌ [bold red]Error: {str(e)}[/bold red]")

@cli.command()
def setup():
    """Configura el cliente con credenciales de API"""
    
    console.print("\n🔧 [bold blue]Configuración del Cliente de MercadoLibre[/bold blue]\n")
    
    console.print("Las APIs públicas de MercadoLibre no requieren autenticación.")
    console.print("Para APIs avanzadas, necesitas registrar una aplicación en:")
    console.print("👉 https://developers.mercadolibre.com.mx/\n")
    
    # Verificar si existe .env
    env_path = ".env"
    if os.path.exists(env_path):
        console.print("✅ Archivo .env encontrado")
    else:
        console.print("📝 Creando archivo .env desde plantilla...")
        
        # Copiar .env.example a .env
        if os.path.exists(".env.example"):
            with open(".env.example", 'r') as f:
                content = f.read()
            
            with open(".env", 'w') as f:
                f.write(content)
            
            console.print("✅ Archivo .env creado")
            console.print("📝 Edita el archivo .env para agregar tus credenciales")
        else:
            console.print("❌ No se encontró .env.example")
    
    # Probar conexión
    console.print("\n🧪 Probando conexión con la API...")
    
    try:
        with MercadoLibreClient() as client:
            categories = client.get_categories()
            console.print(f"✅ [bold green]Conexión exitosa! Encontradas {len(categories)} categorías[/bold green]")
    except Exception as e:
        console.print(f"❌ [bold red]Error de conexión: {str(e)}[/bold red]")

if __name__ == '__main__':
    cli()
