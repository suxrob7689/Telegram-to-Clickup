from http.server import BaseHTTPRequestHandler
import json
import requests
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Vercel'dagi maxfiy o'zgaruvchidan Make.com manzilini olish
        MAKE_WEBHOOK_URL = os.environ.get('MAKE_WEBHOOK_URL')

        if not MAKE_WEBHOOK_URL:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Server configuration error: MAKE_WEBHOOK_URL is not set.')
            return

        try:
            content_length = int(self.headers['Content-Length'])
            update = json.loads(self.rfile.read(content_length))
            
            message = update.get('message', {})
            text = message.get('text', '')
            caption = message.get('caption', '')

            # Agar xabar matni yoki izohi "/" bilan boshlansa, Make.com'ga yuborish
            if text.startswith('/') or caption.startswith('/'):
                requests.post(MAKE_WEBHOOK_URL, json=update, timeout=5)

        except Exception:
            # Xatolik bo'lsa ham, Telegramga muammo bo'lmasligi uchun OK javobini qaytarish
            pass
        
        # Telegram serveriga har doim muvaffaqiyatli javob qaytarish
        self.send_response(200)
        self.end_headers()
        return
