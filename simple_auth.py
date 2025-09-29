#!/usr/bin/env python3
"""
Autenticación simplificada para MercadoLibre
"""

import os
import requests
import json
from dotenv import load_dotenv
from urllib.parse import urlencode

def get_simple_auth_url():
    """Genera URL de autorización simplificada"""
    load_dotenv()
    
    client_id = os.getenv('MELI_CLIENT_ID')
    if not client_id:
        print("❌ Error: MELI_CLIENT_ID no configurado en .env")
        return None
    
    # Usar una URL más simple que funcione mejor
    redirect_uri = "https://httpbin.org/get"
    
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri
    }
    
    auth_url = f"https://auth.mercadolibre.com.mx/authorization?{urlencode(params)}"
    
    print("🔗 URL de Autorización Simplificada:")
    print(auth_url)
    print()
    print("📋 Instrucciones:")
    print("1. Copia y pega esta URL en tu navegador")
    print("2. Inicia sesión en MercadoLibre")
    print("3. Autoriza la aplicación")
    print("4. En la página de respuesta, busca el parámetro 'code' en la URL")
    print("5. Copia solo el valor del código (después de 'code=')")
    print()
    
    return auth_url, redirect_uri

def authenticate_with_code(code):
    """Autentica usando el código obtenido"""
    load_dotenv()
    
    client_id = os.getenv('MELI_CLIENT_ID')
    client_secret = os.getenv('MELI_CLIENT_SECRET')
    redirect_uri = "https://httpbin.org/get"
    
    if not client_id or not client_secret:
        print("❌ Error: Credenciales no configuradas en .env")
        return False
    
    # Intercambiar código por token
    token_url = "https://api.mercadolibre.com/oauth/token"
    
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri
    }
    
    try:
        response = requests.post(token_url, json=data)
        
        if response.status_code == 200:
            token_data = response.json()
            
            # Guardar token
            with open('.meli_token.json', 'w') as f:
                json.dump(token_data, f, indent=2)
            
            print("✅ ¡Autenticación exitosa!")
            print(f"🔑 Access Token: {token_data['access_token'][:20]}...")
            print(f"⏰ Expira en: {token_data.get('expires_in', 'N/A')} segundos")
            
            return True
        else:
            print(f"❌ Error en autenticación: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_token():
    """Prueba el token guardado"""
    if not os.path.exists('.meli_token.json'):
        print("❌ No hay token guardado")
        return False
    
    try:
        with open('.meli_token.json', 'r') as f:
            token_data = json.load(f)
        
        access_token = token_data.get('access_token')
        if not access_token:
            print("❌ Token inválido")
            return False
        
        # Probar con una búsqueda simple
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(
            'https://api.mercadolibre.com/sites/MLM/search?q=test&limit=1',
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Token funcionando correctamente")
            print(f"📊 Resultados disponibles: {data.get('paging', {}).get('total', 'N/A')}")
            return True
        else:
            print(f"❌ Token no válido: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando token: {str(e)}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "url":
            get_simple_auth_url()
        elif sys.argv[1] == "auth":
            if len(sys.argv) > 2:
                code = sys.argv[2]
                authenticate_with_code(code)
            else:
                code = input("🔑 Ingresa el código de autorización: ")
                authenticate_with_code(code)
        elif sys.argv[1] == "test":
            test_token()
    else:
        print("Uso:")
        print("  python3 simple_auth.py url     # Generar URL de autorización")
        print("  python3 simple_auth.py auth    # Autenticar con código")
        print("  python3 simple_auth.py test    # Probar token guardado")
