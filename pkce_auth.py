#!/usr/bin/env python3
"""
Autenticación con PKCE para MercadoLibre API
Maneja el nuevo requerimiento de code_verifier
"""

import os
import requests
import json
import base64
import hashlib
import secrets
from dotenv import load_dotenv
from urllib.parse import urlencode

class PKCEAuth:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('MELI_CLIENT_ID')
        self.client_secret = os.getenv('MELI_CLIENT_SECRET')
        self.redirect_uri = "https://httpbin.org/get"
        
        if not self.client_id or not self.client_secret:
            raise Exception("MELI_CLIENT_ID y MELI_CLIENT_SECRET deben estar configurados en .env")
        
        # Generar PKCE parameters
        self.code_verifier = self._generate_code_verifier()
        self.code_challenge = self._generate_code_challenge(self.code_verifier)
        
        # Guardar para usar después
        self._save_pkce_data()
    
    def _generate_code_verifier(self):
        """Genera code_verifier para PKCE"""
        return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
    
    def _generate_code_challenge(self, verifier):
        """Genera code_challenge a partir del verifier"""
        digest = hashlib.sha256(verifier.encode('utf-8')).digest()
        return base64.urlsafe_b64encode(digest).decode('utf-8').rstrip('=')
    
    def _save_pkce_data(self):
        """Guarda datos PKCE para usar en el intercambio"""
        pkce_data = {
            'code_verifier': self.code_verifier,
            'code_challenge': self.code_challenge
        }
        
        with open('.pkce_data.json', 'w') as f:
            json.dump(pkce_data, f)
    
    def _load_pkce_data(self):
        """Carga datos PKCE guardados"""
        try:
            with open('.pkce_data.json', 'r') as f:
                data = json.load(f)
            return data.get('code_verifier'), data.get('code_challenge')
        except:
            return None, None
    
    def get_auth_url(self):
        """Genera URL de autorización con PKCE"""
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'code_challenge': self.code_challenge,
            'code_challenge_method': 'S256'
        }
        
        auth_url = f"https://auth.mercadolibre.com.mx/authorization?{urlencode(params)}"
        
        print("🔗 URL de Autorización con PKCE:")
        print(auth_url)
        print()
        print("📋 Instrucciones:")
        print("1. Copia y pega esta URL en tu navegador")
        print("2. Inicia sesión en MercadoLibre")
        print("3. Autoriza la aplicación")
        print("4. En la página de respuesta JSON, busca el parámetro 'code'")
        print("5. Copia solo el valor del código")
        print()
        
        return auth_url
    
    def authenticate_with_code(self, code):
        """Autentica usando código con PKCE"""
        # Cargar code_verifier guardado
        code_verifier, _ = self._load_pkce_data()
        
        if not code_verifier:
            print("❌ Error: No se encontraron datos PKCE. Ejecuta 'url' primero.")
            return False
        
        token_url = "https://api.mercadolibre.com/oauth/token"
        
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri,
            'code_verifier': code_verifier
        }
        
        try:
            print("🔄 Intercambiando código por token...")
            response = requests.post(token_url, json=data)
            
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                token_data = response.json()
                
                # Guardar token
                with open('.meli_token.json', 'w') as f:
                    json.dump(token_data, f, indent=2)
                
                print("✅ ¡Autenticación exitosa!")
                print(f"🔑 Access Token: {token_data['access_token'][:20]}...")
                print(f"⏰ Expira en: {token_data.get('expires_in', 'N/A')} segundos")
                
                # Limpiar datos PKCE
                if os.path.exists('.pkce_data.json'):
                    os.remove('.pkce_data.json')
                
                return True
            else:
                print(f"❌ Error en autenticación: {response.status_code}")
                print(f"Respuesta: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_token(self):
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
            
            print("🔄 Probando token...")
            
            # Probar con una búsqueda simple
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(
                'https://api.mercadolibre.com/sites/MLM/search?q=iPhone&limit=1',
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Token funcionando correctamente")
                print(f"📊 Resultados disponibles: {data.get('paging', {}).get('total', 'N/A'):,}")
                
                # Mostrar un producto de ejemplo
                if data.get('results'):
                    product = data['results'][0]
                    print(f"📱 Ejemplo: {product.get('title', 'N/A')}")
                    print(f"💰 Precio: ${product.get('price', 0):,.2f}")
                    print(f"🔥 Vendidos: {product.get('sold_quantity', 0):,}")
                
                return True
            else:
                print(f"❌ Token no válido: {response.status_code}")
                print(f"Respuesta: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error probando token: {str(e)}")
            return False

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python3 pkce_auth.py url      # Generar URL de autorización")
        print("  python3 pkce_auth.py auth     # Autenticar con código")
        print("  python3 pkce_auth.py test     # Probar token guardado")
        return
    
    command = sys.argv[1]
    
    try:
        auth = PKCEAuth()
        
        if command == "url":
            auth.get_auth_url()
            
        elif command == "auth":
            if len(sys.argv) > 2:
                code = sys.argv[2]
            else:
                code = input("🔑 Ingresa el código de autorización: ")
            
            auth.authenticate_with_code(code)
            
        elif command == "test":
            auth.test_token()
            
        else:
            print(f"❌ Comando desconocido: {command}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
