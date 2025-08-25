from http.server import BaseHTTPRequestHandler
import json
import requests
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Maxfiy Make.com manzilini Vercel'dan xavfsiz tarzda olish
        MAKE_WEBHOOK_URL = os.environ.get('MAKE_WEBHOOK_URL')

        # Agar Vercel'da manzil sozlanmagan bo'lsa, xatolik berish
        if not MAKE_WEBHOOK_URL:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Server configuration error: MAKE_WEBHOOK_URL is not set.')
            return

        try:
            # 2. Telegramdan kelgan ma'lumotni o'qish
            content_length = int(self.headers['Content-Length'])
            update = json.loads(self.rfile.read(content_length))
            
            # 3. Xabar va izohni xatoliksiz, xavfsiz tarzda olish
            message = update.get('message', {})
            text = message.get('text', '')
            caption = message.get('caption', '')

            # 4. ASOSIY FILTR: Matn yoki izoh ichida 'task:' so'zi borligini tekshirish
            # .lower() - matnni kichik harflarga o'giradi (case-insensitive)
            # 'in' - so'z matnning istalgan joyida bo'lishini tekshiradi
            if 'task:' in text.lower() or 'task:' in caption.lower():
                # Agar shart bajarilsa, ma'lumotni o'zgartirmasdan Make.com'ga yuborish
                requests.post(MAKE_WEBHOOK_URL, json=update, timeout=5)

        except Exception:
            # Kodda biror xatolik yuz bersa ham, Telegramga muammo bo'lmasligi uchun jim o'tish
            pass
        
        # 5. Telegram serveriga har doim "OK" (200) javobini qaytarish. Bu juda muhim!
        self.send_response(200)
        self.end_headers()
        return
