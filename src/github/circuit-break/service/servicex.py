import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import time

# Define o diretório base para o servidor
diretorio_base = "./seu_diretorio"

# Define a porta do servidor
porta = 8000

# Cria o manipulador HTTP
class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Verifica se a variável de ambiente "error" é definida como "yes"
        if os.environ.get('error') == 'yes':
            print("Erro 504 - Gateway Timeout")
            # Aguarda 5 segundos
            time.sleep(5)
            # Responde com o código de erro 504 - Gateway Timeout
            self.send_response(504)
            self.end_headers()
        else:
            print("OK")
            # Responde com o código 200 e a mensagem "OK"
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"OK")

# Cria o servidor web com o manipulador personalizado
httpd = TCPServer(("", porta), MyHandler)

print(f"Servidor rodando na porta {porta}")

# Inicia o servidor
httpd.serve_forever()
