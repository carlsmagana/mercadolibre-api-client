#!/usr/bin/env python3
"""
Herramientas de análisis para datos de MercadoLibre
"""

import json
import pandas as pd
import os
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime
import statistics

console = Console()

class MercadoLibreAnalytics:
    """Clase para análisis de datos de MercadoLibre"""
    
    def __init__(self):
        self.console = Console()
    
    def load_data_from_json(self, json_file: str) -> List[Dict]:
        """Carga datos desde un archivo JSON"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.console.print(f"❌ Error cargando {json_file}: {e}")
            return []
    
    def analyze_prices(self, products: List[Dict]) -> Dict[str, Any]:
        """Analiza los precios de los productos"""
        if not products:
            return {}
        
        prices = [p.get('precio', 0) for p in products if p.get('precio', 0) > 0]
        
        if not prices:
            return {}
        
        return {
            'total_products': len(products),
            'products_with_price': len(prices),
            'min_price': min(prices),
            'max_price': max(prices),
            'avg_price': statistics.mean(prices),
            'median_price': statistics.median(prices),
            'price_range': max(prices) - min(prices)
        }
    
    def analyze_sales(self, products: List[Dict]) -> Dict[str, Any]:
        """Analiza las ventas de los productos"""
        if not products:
            return {}
        
        sales = [p.get('cantidad_vendida', 0) for p in products if isinstance(p.get('cantidad_vendida'), (int, float))]
        
        if not sales:
            return {}
        
        return {
            'total_products': len(products),
            'products_with_sales': len([s for s in sales if s > 0]),
            'total_sales': sum(sales),
            'avg_sales': statistics.mean(sales),
            'median_sales': statistics.median(sales),
            'max_sales': max(sales),
            'min_sales': min(sales)
        }
    
    def analyze_sellers(self, products: List[Dict]) -> Dict[str, Any]:
        """Analiza los vendedores"""
        if not products:
            return {}
        
        sellers = {}
        for product in products:
            seller_id = product.get('vendedor_id')
            if seller_id and seller_id != 'No especificado':
                if seller_id not in sellers:
                    sellers[seller_id] = {
                        'products': 0,
                        'total_sales': 0,
                        'avg_price': 0,
                        'prices': []
                    }
                
                sellers[seller_id]['products'] += 1
                sellers[seller_id]['total_sales'] += product.get('cantidad_vendida', 0)
                price = product.get('precio', 0)
                if price > 0:
                    sellers[seller_id]['prices'].append(price)
        
        # Calcular promedios
        for seller_data in sellers.values():
            if seller_data['prices']:
                seller_data['avg_price'] = statistics.mean(seller_data['prices'])
        
        return {
            'total_sellers': len(sellers),
            'sellers_data': sellers
        }
    
    def generate_report(self, json_file: str) -> None:
        """Genera un reporte completo de análisis"""
        self.console.print(f"\n📊 [bold blue]Análisis de Datos: {os.path.basename(json_file)}[/bold blue]")
        self.console.print("=" * 70)
        
        # Cargar datos
        products = self.load_data_from_json(json_file)
        
        if not products:
            self.console.print("❌ No se pudieron cargar los datos")
            return
        
        # Análisis de precios
        price_analysis = self.analyze_prices(products)
        if price_analysis:
            price_panel = f"""
💰 Análisis de Precios:
   • Total de productos: {price_analysis['total_products']:,}
   • Con precio: {price_analysis['products_with_price']:,}
   • Precio mínimo: ${price_analysis['min_price']:,.2f}
   • Precio máximo: ${price_analysis['max_price']:,.2f}
   • Precio promedio: ${price_analysis['avg_price']:,.2f}
   • Precio mediano: ${price_analysis['median_price']:,.2f}
   • Rango de precios: ${price_analysis['price_range']:,.2f}
            """
            self.console.print(Panel(price_panel, title="💰 Precios"))
        
        # Análisis de ventas
        sales_analysis = self.analyze_sales(products)
        if sales_analysis:
            sales_panel = f"""
📈 Análisis de Ventas:
   • Total de productos: {sales_analysis['total_products']:,}
   • Con ventas: {sales_analysis['products_with_sales']:,}
   • Ventas totales: {sales_analysis['total_sales']:,}
   • Ventas promedio: {sales_analysis['avg_sales']:,.0f}
   • Ventas medianas: {sales_analysis['median_sales']:,.0f}
   • Máximo vendido: {sales_analysis['max_sales']:,}
   • Mínimo vendido: {sales_analysis['min_sales']:,}
            """
            self.console.print(Panel(sales_panel, title="📈 Ventas"))
        
        # Top productos por ventas
        top_products = sorted(products, key=lambda x: x.get('cantidad_vendida', 0), reverse=True)[:10]
        
        if top_products:
            self.console.print("\n🏆 [bold]Top 10 Productos Más Vendidos:[/bold]")
            
            table = Table()
            table.add_column("Pos", style="cyan", width=4)
            table.add_column("Título", style="white", max_width=40)
            table.add_column("Precio", style="green", justify="right")
            table.add_column("Vendidos", style="magenta", justify="right")
            table.add_column("Condición", style="yellow")
            
            for i, product in enumerate(top_products, 1):
                table.add_row(
                    str(i),
                    product.get('titulo', 'Sin título')[:37] + "..." if len(product.get('titulo', '')) > 40 else product.get('titulo', 'Sin título'),
                    f"${product.get('precio', 0):,.2f}",
                    f"{product.get('cantidad_vendida', 0):,}",
                    product.get('condicion', 'N/A')
                )
            
            self.console.print(table)
        
        # Análisis de vendedores
        seller_analysis = self.analyze_sellers(products)
        if seller_analysis and seller_analysis['total_sellers'] > 0:
            self.console.print(f"\n👥 [bold]Análisis de Vendedores:[/bold]")
            self.console.print(f"   Total de vendedores únicos: {seller_analysis['total_sellers']}")
            
            # Top vendedores por número de productos
            top_sellers = sorted(
                seller_analysis['sellers_data'].items(),
                key=lambda x: x[1]['products'],
                reverse=True
            )[:5]
            
            seller_table = Table(title="Top 5 Vendedores por Productos")
            seller_table.add_column("Vendedor", style="cyan")
            seller_table.add_column("Productos", style="green", justify="right")
            seller_table.add_column("Ventas Tot.", style="magenta", justify="right")
            seller_table.add_column("Precio Prom.", style="yellow", justify="right")
            
            for seller_id, data in top_sellers:
                seller_table.add_row(
                    seller_id,
                    str(data['products']),
                    f"{data['total_sales']:,}",
                    f"${data['avg_price']:,.2f}" if data['avg_price'] > 0 else "N/A"
                )
            
            self.console.print(seller_table)
        
        # Distribución de condiciones
        conditions = {}
        for product in products:
            condition = product.get('condicion', 'N/A')
            conditions[condition] = conditions.get(condition, 0) + 1
        
        if conditions:
            self.console.print(f"\n📦 [bold]Distribución por Condición:[/bold]")
            for condition, count in sorted(conditions.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(products)) * 100
                self.console.print(f"   • {condition}: {count} ({percentage:.1f}%)")
        
        # Envío gratis
        free_shipping = len([p for p in products if p.get('envio_gratis', False)])
        paid_shipping = len(products) - free_shipping
        
        self.console.print(f"\n🚚 [bold]Análisis de Envío:[/bold]")
        self.console.print(f"   • Envío gratis: {free_shipping} ({free_shipping/len(products)*100:.1f}%)")
        self.console.print(f"   • Envío pago: {paid_shipping} ({paid_shipping/len(products)*100:.1f}%)")
        
        self.console.print("\n" + "=" * 70)

def main():
    """Función principal para análisis interactivo"""
    console.print("📊 [bold blue]Analizador de Datos de MercadoLibre[/bold blue]")
    console.print("=" * 50)
    
    # Buscar archivos JSON en exports
    exports_dir = 'exports'
    if not os.path.exists(exports_dir):
        console.print("❌ No existe el directorio exports")
        return
    
    json_files = [f for f in os.listdir(exports_dir) if f.endswith('.json')]
    
    if not json_files:
        console.print("❌ No se encontraron archivos JSON en exports/")
        return
    
    # Ordenar por fecha de modificación
    json_files.sort(key=lambda x: os.path.getmtime(os.path.join(exports_dir, x)), reverse=True)
    
    console.print(f"📁 Archivos encontrados: {len(json_files)}")
    
    # Analizar los archivos más recientes
    analyzer = MercadoLibreAnalytics()
    
    for i, json_file in enumerate(json_files[:3], 1):  # Analizar los 3 más recientes
        file_path = os.path.join(exports_dir, json_file)
        console.print(f"\n{'='*20} ANÁLISIS {i} {'='*20}")
        analyzer.generate_report(file_path)
        
        if i < min(3, len(json_files)):
            console.print("\n" + "─" * 70)

if __name__ == "__main__":
    main()
