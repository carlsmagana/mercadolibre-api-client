#!/usr/bin/env python3
"""
Herramienta para comparar productos entre diferentes búsquedas
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from public_client import create_public_client
from datetime import datetime
import statistics

console = Console()

@click.command()
@click.argument('products', nargs=-1, required=True)
@click.option('--limit', '-l', default=5, help='Productos por búsqueda')
@click.option('--export', '-e', help='Exportar comparación')
def compare(products, limit, export):
    """Compara múltiples productos
    
    Ejemplo: python3 compare_products.py "iPhone 15" "Samsung Galaxy S24" "Google Pixel 8"
    """
    
    console.print(f"\n🔍 [bold blue]Comparando {len(products)} productos[/bold blue]")
    console.print("=" * 60)
    
    all_results = {}
    
    # Buscar cada producto
    for product_name in products:
        console.print(f"\n🔍 Buscando: [bold]{product_name}[/bold]")
        
        try:
            with create_public_client() as client:
                results = client.search_products_public(product_name, limit)
                all_results[product_name] = results
                console.print(f"✅ Encontrados {len(results)} productos")
                
        except Exception as e:
            console.print(f"❌ Error: {str(e)}")
            all_results[product_name] = []
    
    # Generar comparación
    if all_results:
        generate_comparison_report(all_results)
        
        # Exportar si se solicita
        if export:
            export_comparison(all_results, export)

def generate_comparison_report(all_results):
    """Genera reporte de comparación"""
    console.print(f"\n📊 [bold blue]Reporte de Comparación[/bold blue]")
    console.print("=" * 60)
    
    # Tabla de resumen
    summary_table = Table(title="Resumen por Producto")
    summary_table.add_column("Producto", style="cyan")
    summary_table.add_column("Encontrados", style="green", justify="right")
    summary_table.add_column("Precio Min", style="yellow", justify="right")
    summary_table.add_column("Precio Max", style="yellow", justify="right")
    summary_table.add_column("Precio Prom", style="magenta", justify="right")
    summary_table.add_column("Ventas Tot", style="blue", justify="right")
    
    comparison_data = {}
    
    for product_name, results in all_results.items():
        if results:
            prices = [p.price for p in results if p.price > 0]
            sales = [p.sold_quantity for p in results if p.sold_quantity > 0]
            
            comparison_data[product_name] = {
                'count': len(results),
                'min_price': min(prices) if prices else 0,
                'max_price': max(prices) if prices else 0,
                'avg_price': statistics.mean(prices) if prices else 0,
                'total_sales': sum(sales) if sales else 0
            }
            
            summary_table.add_row(
                product_name,
                str(len(results)),
                f"${comparison_data[product_name]['min_price']:,.2f}",
                f"${comparison_data[product_name]['max_price']:,.2f}",
                f"${comparison_data[product_name]['avg_price']:,.2f}",
                f"{comparison_data[product_name]['total_sales']:,}"
            )
        else:
            summary_table.add_row(product_name, "0", "N/A", "N/A", "N/A", "N/A")
    
    console.print(summary_table)
    
    # Análisis de ganador
    if comparison_data:
        console.print(f"\n🏆 [bold]Análisis de Competencia:[/bold]")
        
        # Producto más barato
        cheapest = min(comparison_data.items(), key=lambda x: x[1]['min_price'] if x[1]['min_price'] > 0 else float('inf'))
        console.print(f"💰 Más barato: [green]{cheapest[0]}[/green] (${cheapest[1]['min_price']:,.2f})")
        
        # Producto más caro
        most_expensive = max(comparison_data.items(), key=lambda x: x[1]['max_price'])
        console.print(f"💎 Más caro: [red]{most_expensive[0]}[/red] (${most_expensive[1]['max_price']:,.2f})")
        
        # Producto más vendido
        best_seller = max(comparison_data.items(), key=lambda x: x[1]['total_sales'])
        console.print(f"🔥 Más vendido: [blue]{best_seller[0]}[/blue] ({best_seller[1]['total_sales']:,} ventas)")
        
        # Mejor relación precio-ventas
        value_products = [(name, data['total_sales'] / data['avg_price'] if data['avg_price'] > 0 else 0) 
                         for name, data in comparison_data.items()]
        best_value = max(value_products, key=lambda x: x[1])
        console.print(f"⭐ Mejor valor: [yellow]{best_value[0]}[/yellow] ({best_value[1]:.2f} ventas/$)")
    
    # Detalles por producto
    console.print(f"\n📋 [bold]Detalles por Producto:[/bold]")
    
    for product_name, results in all_results.items():
        if results:
            console.print(f"\n🔸 [bold]{product_name}[/bold]:")
            
            detail_table = Table()
            detail_table.add_column("Título", style="white", max_width=40)
            detail_table.add_column("Precio", style="green", justify="right")
            detail_table.add_column("Vendidos", style="magenta", justify="right")
            detail_table.add_column("Envío", style="blue")
            
            for product in results[:3]:  # Mostrar solo los primeros 3
                shipping = "✅ Gratis" if product.free_shipping else "💰 Pago"
                detail_table.add_row(
                    product.title[:37] + "..." if len(product.title) > 40 else product.title,
                    f"${product.price:,.2f}",
                    f"{product.sold_quantity:,}",
                    shipping
                )
            
            console.print(detail_table)

def export_comparison(all_results, filename):
    """Exporta la comparación a JSON"""
    import json
    import os
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_data = {
        'timestamp': timestamp,
        'comparison': {}
    }
    
    for product_name, results in all_results.items():
        export_data['comparison'][product_name] = []
        for product in results:
            export_data['comparison'][product_name].append({
                'id': product.id,
                'titulo': product.title,
                'precio': product.price,
                'cantidad_vendida': product.sold_quantity,
                'condicion': product.condition,
                'envio_gratis': product.free_shipping
            })
    
    os.makedirs('exports', exist_ok=True)
    filepath = f"exports/comparison_{filename}_{timestamp}.json"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    console.print(f"\n💾 [bold green]Comparación exportada a: {filepath}[/bold green]")

if __name__ == '__main__':
    compare()
