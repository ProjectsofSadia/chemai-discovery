from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ChemAI Discovery</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin: 0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        h1 { font-size: 3rem; margin-bottom: 1rem; }
        p { font-size: 1.2rem; margin: 1rem 0; }
        a { color: #4facfe; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <h1>&#129516; ChemAI Discovery</h1>
    <p>Revolutionary AI-Powered Drug Discovery Platform</p>
    <p>HP x NVIDIA AI Hackathon 2025</p>
    <p>Status: Live and Ready! &#128640;</p>
</body>
</html>"""
        
        self.wfile.write(html.encode("utf-8"))

