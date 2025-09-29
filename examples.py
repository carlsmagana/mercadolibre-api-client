#!/usr/bin/env python3
"""
Ejemplos de uso del cliente de MercadoLibre API
"""

from mercadolibre_client import MercadoLibreClient, create_client
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import time

console = Console()

def example_basic_search():
    """Ejemplo básico de búsqueda de productos"""
    console.print("\n🔍 [bold blue]Ejemplo 1: Búsqueda básica[/bold blue]")
    
    with create_client() as client:
        # Buscar iPhones
        response = client.search_products("iPhone 15", limit=10)
        
        results = response.get('results', [])
        total = response.get('paging', {}).get('total', 0)
        
        console.print(f"✅ Encontrados {len(results)} productos de {total:,} totales")
        
        # Mostrar algunos resultados
        for i, item in enumerate(results[:3], 1):
            console.print(f"\n{i}. [bold]{item['title']}[/bold]")
            console.print(f"   💰 ${item['price']:,.2f} {item['currency_id']}")
            console.print(f"   🔗 {item['permalink']}")

def example_detailed_search():
    """Ejemplo de búsqueda con filtros y múltiples páginas"""
    console.print("\n🔍 [bold blue]Ejemplo 2: Búsqueda avanzada[/bold blue]")
    
    with create_client() as client:
        # Buscar laptops nuevas, ordenadas por precio
        products = client.search_all_pages(
            query="MacBook Pro",
            max_results=100,
            condition="new"
        )
        
        console.print(f"✅ Encontrados {len(products)} MacBooks Pro nuevos")
        
        # Análisis de precios
        prices = [p.price for p in products if p.price > 0]
        if prices:
            avg_price = sum(prices) / len(prices)
            min_price = min(prices)
            max_price = max(prices)
            
            console.print(Panel.fit(
                f"💰 Precio promedio: ${avg_price:,.2f}\n"
                f"💸 Precio mínimo: ${min_price:,.2f}\n"
                f"💎 Precio máximo: ${max_price:,.2f}",
                title="📊 Análisis de Precios"
            ))

def example_product_details():
    """Ejemplo de obtención de detalles de producto"""
    console.print("\n🔍 [bold blue]Ejemplo 3: Detalles de producto[/bold blue]")
    
    with create_client() as client:
        # Primero buscar un producto
        response = client.search_products("iPad Pro", limit=1)
        results = response.get('results', [])
        
        if results:
            product_id = results[0]['id']
            console.print(f"📱 Analizando producto: {product_id}")
            
            # Obtener detalles completos
            details = client.get_product_details(product_id)
            
            console.print(f"\n[bold]{details['title']}[/bold]")
            console.print(f"💰 ${details['price']:,.2f} {details['currency_id']}")
            console.print(f"📦 Condición: {details['condition']}")
            console.print(f"📊 Disponible: {details.get('available_quantity', 'N/A')}")
            console.print(f"🛒 Vendidos: {details.get('sold_quantity', 'N/A')}")
            
            # Mostrar algunos atributos
            attributes = details.get('attributes', [])[:5]
            if attributes:
                console.print("\n📋 [bold]Atributos principales:[/bold]")
                for attr in attributes:
                    name = attr.get('name', 'N/A')
                    value = attr.get('value_name', attr.get('value_id', 'N/A'))
                    console.print(f"   • {name}: {value}")

def example_categories():
    """Ejemplo de exploración de categorías"""
    console.print("\n🔍 [bold blue]Ejemplo 4: Explorar categorías[/bold blue]")
    
    with create_client() as client:
        # Obtener categorías principales
        categories = client.get_categories()
        
        console.print(f"📂 Encontradas {len(categories)} categorías principales")
        
        # Mostrar algunas categorías
        tech_categories = [cat for cat in categories if 'tecnología' in cat['name'].lower() or 'electrónicos' in cat['name'].lower()]
        
        if tech_categories:
            console.print("\n💻 [bold]Categorías de tecnología:[/bold]")
            for cat in tech_categories[:3]:
                console.print(f"   • {cat['name']} ({cat['id']})")
                
                # Obtener detalles de la categoría
                try:
                    cat_details = client.get_category_details(cat['id'])
                    total_items = cat_details.get('total_items_in_this_category', 0)
                    console.print(f"     📊 {total_items:,} productos")
                    
                    time.sleep(1)  # Rate limiting
                except:
                    pass

def example_seller_analysis():
    """Ejemplo de análisis de vendedores"""
    console.print("\n🔍 [bold blue]Ejemplo 5: Análisis de vendedores[/bold blue]")
    
    with create_client() as client:
        # Buscar productos de una marca específica
        response = client.search_products("iPhone Apple", limit=20)
        results = response.get('results', [])
        
        # Analizar vendedores
        sellers = {}
        for item in results:
            seller_id = item.get('seller', {}).get('id')
            if seller_id:
                if seller_id not in sellers:
                    sellers[seller_id] = {
                        'products': 0,
                        'total_sales': 0,
                        'avg_price': 0
                    }
                
                sellers[seller_id]['products'] += 1
                sellers[seller_id]['total_sales'] += item.get('sold_quantity', 0)
                sellers[seller_id]['avg_price'] += item.get('price', 0)
        
        # Calcular promedios
        for seller_id, data in sellers.items():
            if data['products'] > 0:
                data['avg_price'] = data['avg_price'] / data['products']
        
        # Mostrar top vendedores
        top_sellers = sorted(sellers.items(), key=lambda x: x[1]['products'], reverse=True)[:5]
        
        console.print(f"\n👥 [bold]Top 5 vendedores por número de productos:[/bold]")
        
        table = Table()
        table.add_column("Vendedor ID", style="cyan")
        table.add_column("Productos", style="green", justify="right")
        table.add_column("Ventas Totales", style="yellow", justify="right")
        table.add_column("Precio Promedio", style="magenta", justify="right")
        
        for seller_id, data in top_sellers:
            table.add_row(
                seller_id,
                str(data['products']),
                str(data['total_sales']),
                f"${data['avg_price']:,.2f}"
            )
        
        console.print(table)

def example_export_data():
    """Ejemplo de exportación de datos"""
    console.print("\n🔍 [bold blue]Ejemplo 6: Exportar datos[/bold blue]")
    
    with create_client() as client:
        # Buscar productos para exportar
        products = client.search_all_pages("Samsung Galaxy", max_results=50)
        
        if products:
            console.print(f"📊 Exportando {len(products)} productos Samsung Galaxy")
            
            # Exportar a JSON
            client.export_to_json(products, "samsung_galaxy_products.json")
            
            # Exportar a CSV
            try:
                client.export_to_csv(products, "samsung_galaxy_products.csv")
                console.print("✅ Datos exportados en ambos formatos")
            except:
                console.print("⚠️  CSV requiere pandas. Solo se exportó JSON")
        else:
            console.print("❌ No se encontraron productos para exportar")

def run_all_examples():
    """Ejecuta todos los ejemplos"""
    console.print("🚀 [bold green]Ejecutando ejemplos del cliente de MercadoLibre API[/bold green]")
    console.print("=" * 60)
    
    examples = [
        example_basic_search,
        example_detailed_search,
        example_product_details,
        example_categories,
        example_seller_analysis,
        example_export_data
    ]
    
    for i, example in enumerate(examples, 1):
        try:
            example()
            console.print(f"\n✅ [green]Ejemplo {i} completado[/green]")
            
            if i < len(examples):
                console.print("\n" + "─" * 60)
                time.sleep(2)  # Pausa entre ejemplos
                
        except Exception as e:
            console.print(f"\n❌ [red]Error en ejemplo {i}: {str(e)}[/red]")
    
    console.print("\n🎉 [bold green]¡Todos los ejemplos completados![/bold green]")

if __name__ == "__main__":
    run_all_examples()
