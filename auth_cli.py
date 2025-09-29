#!/usr/bin/env python3
"""
CLI para cliente autenticado de MercadoLibre
Usa datos reales de la API oficial
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from auth_client import create_authenticated_client
from datetime import datetime
import json
import os

console = Console()

@click.group()
def cli():
    """🔐 Cliente Autenticado de MercadoLibre
    
    Usa APIs oficiales con tu App ID y Client Secret para obtener datos reales.
    """
    pass

@cli.command()
def setup():
    """Configurar autenticación inicial"""
    console.print("\n🔐 [bold blue]Configuración de Autenticación[/bold blue]")
    console.print("=" * 50)
    
    try:
        client = create_authenticated_client()
        
        if client.access_token:
            console.print("✅ [bold green]Ya tienes un token válido[/bold green]")
            return
        
        # Mostrar URL de autorización
        auth_url = client.get_auth_url()
        
        console.print("\n📋 [bold]Pasos para autorizar:[/bold]")
        console.print("1. Ve a la siguiente URL en tu navegador:")
        console.print(f"   [link]{auth_url}[/link]")
        console.print("\n2. Autoriza la aplicación")
        console.print("3. Copia el código de la URL de callback")
        
        # Abrir automáticamente en navegador
        import webbrowser
        if click.confirm("\n¿Abrir URL automáticamente en el navegador?"):
            webbrowser.open(auth_url)
        
        # Pedir código
        code = Prompt.ask("\n🔑 Ingresa el código de autorización")
        
        if client.authenticate_with_code(code):
            console.print("\n✅ [bold green]¡Autenticación exitosa![/bold green]")
            console.print("🎉 Ahora puedes usar todas las funciones con datos reales")
        else:
            console.print("\n❌ [bold red]Error en autenticación[/bold red]")
            console.print("Verifica que el código sea correcto")
    
    except Exception as e:
        console.print(f"\n❌ [bold red]Error: {str(e)}[/bold red]")

@cli.command()
@click.argument('query')
@click.option('--limit', '-l', default=10, help='Número de resultados')
@click.option('--condition', help='Condición: new, used')
@click.option('--category', help='ID de categoría')
@click.option('--sort', help='Ordenamiento: price_asc, price_desc, relevance')
@click.option('--export', '-e', help='Exportar a archivo')
def search(query, limit, condition, category, sort, export):
    """Buscar productos con API autenticada"""
    
    console.print(f"\n🔍 [bold blue]Búsqueda Autenticada: '{query}'[/bold blue]")
    console.print(f"📊 Límite: {limit}")
    
    try:
        client = create_authenticated_client()
        
        if not client.access_token:
            console.print("❌ [bold red]No estás autenticado[/bold red]")
            console.print("💡 Ejecuta: python3 auth_cli.py setup")
            return
        
        # Preparar filtros
        filters = {}
        if condition:
            filters['condition'] = condition
        if category:
            filters['category'] = category
        if sort:
            filters['sort'] = sort
        
        # Buscar productos
        products = client.search_products_authenticated(query, limit, **filters)
        
        if products:
            console.print(f"\n✅ [bold green]Encontrados {len(products)} productos REALES[/bold green]")
            
            # Crear tabla
            table = Table(title=f"Resultados Reales para '{query}'")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Título", style="white", max_width=35)
            table.add_column("Precio", style="green", justify="right")
            table.add_column("Vendidos", style="magenta", justify="right")
            table.add_column("Stock", style="yellow", justify="right")
            table.add_column("Vendedor", style="blue", max_width=15)
            
            for product in products:
                table.add_row(
                    product.id,
                    product.title[:32] + "..." if len(product.title) > 35 else product.title,
                    f"${product.price:,.2f}",
                    f"{product.sold_quantity:,}",
                    f"{product.available_quantity:,}",
                    product.seller_nickname[:12] + "..." if len(product.seller_nickname) > 15 else product.seller_nickname
                )
            
            console.print(table)
            
            # Exportar si se solicita
            if export:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{export}_real_{timestamp}.json"
                
                export_data = []
                for product in products:
                    export_data.append({
                        'id': product.id,
                        'titulo': product.title,
                        'precio': product.price,
                        'moneda': product.currency,
                        'cantidad_vendida': product.sold_quantity,
                        'stock_disponible': product.available_quantity,
                        'condicion': product.condition,
                        'vendedor_id': product.seller_id,
                        'vendedor_nickname': product.seller_nickname,
                        'categoria_id': product.category_id,
                        'categoria_nombre': product.category_name,
                        'envio_gratis': product.free_shipping,
                        'ubicacion': product.location,
                        'url': product.permalink,
                        'tipo_publicacion': product.listing_type
                    })
                
                os.makedirs('exports', exist_ok=True)
                filepath = f"exports/{filename}"
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                console.print(f"\n💾 [bold green]Datos REALES exportados a: {filepath}[/bold green]")
        
        else:
            console.print("\n❌ [bold red]No se encontraron productos[/bold red]")
    
    except Exception as e:
        console.print(f"\n❌ [bold red]Error: {str(e)}[/bold red]")

@cli.command()
@click.argument('product_id')
def product(product_id):
    """Obtener detalles completos de un producto"""
    
    console.print(f"\n📱 [bold blue]Detalles del Producto: {product_id}[/bold blue]")
    
    try:
        client = create_authenticated_client()
        
        if not client.access_token:
            console.print("❌ [bold red]No estás autenticado[/bold red]")
            console.print("💡 Ejecuta: python3 auth_cli.py setup")
            return
        
        product = client.get_product_details(product_id)
        
        if product:
            # Información básica
            basic_info = f"""
📱 **{product.title}**

💰 **Precio**: ${product.price:,.2f} {product.currency}
🔥 **Vendidos**: {product.sold_quantity:,}
📦 **Stock**: {product.available_quantity:,}
🏷️ **Condición**: {product.condition}
🚚 **Envío gratis**: {'✅ Sí' if product.free_shipping else '❌ No'}

👤 **Vendedor**: {product.seller_nickname} ({product.seller_id})
📍 **Ubicación**: {product.location}
🏪 **Categoría**: {product.category_name}
📋 **Tipo**: {product.listing_type}

🔗 **URL**: {product.permalink}
            """
            
            console.print(Panel(basic_info, title="📋 Información Básica"))
            
            # Reputación del vendedor
            if product.seller_reputation:
                rep = product.seller_reputation
                reputation_info = f"""
⭐ **Nivel**: {rep.get('level_id', 'N/A')}
📊 **Transacciones**: {rep.get('transactions', {}).get('total', 0):,}
👍 **Calificaciones positivas**: {rep.get('transactions', {}).get('positive', 0):,}
👎 **Calificaciones negativas**: {rep.get('transactions', {}).get('negative', 0):,}
                """
                console.print(Panel(reputation_info, title="👤 Reputación del Vendedor"))
            
            # Atributos
            if product.attributes:
                console.print("\n🏷️ [bold]Atributos:[/bold]")
                attr_table = Table()
                attr_table.add_column("Atributo", style="cyan")
                attr_table.add_column("Valor", style="white")
                
                for attr in product.attributes[:10]:  # Mostrar solo los primeros 10
                    attr_table.add_row(
                        attr.get('name', 'N/A'),
                        str(attr.get('value_name', attr.get('value_id', 'N/A')))
                    )
                
                console.print(attr_table)
            
            # Descripción
            if product.description:
                desc_preview = product.description[:200] + "..." if len(product.description) > 200 else product.description
                console.print(Panel(desc_preview, title="📝 Descripción"))
        
        else:
            console.print(f"\n❌ [bold red]No se encontró el producto {product_id}[/bold red]")
    
    except Exception as e:
        console.print(f"\n❌ [bold red]Error: {str(e)}[/bold red]")

@cli.command()
def status():
    """Verificar estado de autenticación"""
    
    console.print("\n🔐 [bold blue]Estado de Autenticación[/bold blue]")
    console.print("=" * 40)
    
    try:
        client = create_authenticated_client()
        
        if client.access_token:
            console.print("✅ [bold green]Autenticado correctamente[/bold green]")
            console.print(f"🔑 Token expira: {client.token_expires_at}")
            console.print(f"🌍 Sitio: {client.site_id}")
            
            # Probar con una búsqueda simple
            try:
                products = client.search_products_authenticated("test", 1)
                console.print("✅ [bold green]API funcionando correctamente[/bold green]")
                console.print(f"📊 Límite de requests: ~300/minuto")
            except Exception as e:
                console.print(f"⚠️ [bold yellow]Advertencia: {str(e)}[/bold yellow]")
        
        else:
            console.print("❌ [bold red]No autenticado[/bold red]")
            console.print("💡 Ejecuta: python3 auth_cli.py setup")
    
    except Exception as e:
        console.print(f"❌ [bold red]Error: {str(e)}[/bold red]")

@cli.command()
def demo():
    """Demostración con datos reales"""
    
    console.print("\n🎬 [bold blue]Demo con Datos REALES[/bold blue]")
    console.print("=" * 50)
    
    try:
        client = create_authenticated_client()
        
        if not client.access_token:
            console.print("❌ [bold red]No estás autenticado[/bold red]")
            console.print("💡 Ejecuta: python3 auth_cli.py setup")
            return
        
        queries = ["iPhone 15", "MacBook Pro", "Samsung Galaxy"]
        
        for query in queries:
            console.print(f"\n🔍 Buscando: [bold]{query}[/bold]")
            
            products = client.search_products_authenticated(query, 2)
            
            if products:
                console.print(f"✅ {len(products)} productos REALES encontrados")
                
                for i, product in enumerate(products, 1):
                    console.print(f"  {i}. {product.title[:50]}...")
                    console.print(f"     💰 ${product.price:,.2f}")
                    console.print(f"     🔥 {product.sold_quantity:,} vendidos")
                    console.print(f"     👤 {product.seller_nickname}")
            else:
                console.print("❌ Sin resultados")
        
        console.print(f"\n🎉 [bold green]Demo completada con datos REALES[/bold green]")
    
    except Exception as e:
        console.print(f"❌ [bold red]Error: {str(e)}[/bold red]")

if __name__ == '__main__':
    cli()
