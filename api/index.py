from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import sys
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import your main app
try:
    from main import app
    print("✅ Successfully imported ChemAI Discovery app")    
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    # Create simple fallback
    app = FastAPI(title="ChemAI Discovery")

    @app.get("/")
    def home():
        return HTMLResponse('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>🧬 ChemAI Discovery</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 2rem;
                       background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
                h1 { font-size: 3rem; margin-bottom: 1rem; }  
                p { font-size: 1.2rem; margin: 1rem 0; }      
                a { color: #4facfe; text-decoration: none; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>🧬 ChemAI Discovery</h1>
            <p>Revolutionary AI-Powered Drug Discovery Platform</p>
            <p>HP × NVIDIA AI Hackathon 2025</p>
            <p><a href="/docs">📚 API Documentation</a></p>   
            <p><a href="/health">❤️ Health Check</a></p>      
        </body>
        </html>
        ''')

# Vercel serverless handler
handler = app
