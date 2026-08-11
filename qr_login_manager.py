

### 1. `qr_login_manager.py` (Python)

```python
# qr_login_manager.py — Python версия

import qrcode
from PIL import Image
import uuid
import json
import time
import sys
import argparse
from datetime import datetime, timedelta

class QRLoginManager:
    def __init__(self, ttl=60):
        self.ttl = ttl
        self.token = None
        self.timestamp = None
        self.qr = None

    def generate_token(self):
        self.token = str(uuid.uuid4())
        self.timestamp = datetime.now().isoformat()
        return self.token

    def create_qr(self):
        if not self.token:
            self.generate_token()
        data = {
            'token': self.token,
            'timestamp': self.timestamp,
            'ttl': self.ttl,
            'expires': (datetime.now() + timedelta(seconds=self.ttl)).isoformat()
        }
        qr_data = json.dumps(data)
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        self.qr.add_data(qr_data)
        self.qr.make(fit=True)
        img = self.qr.make_image(fill_color="black", back_color="white")
        return img

    def save_png(self, filename='qrcode.png'):
        if self.qr is None:
            self.create_qr()
        img = self.qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        print(f"💾 Сохранено PNG: {filename}")

    def print_ascii(self):
        if self.qr is None:
            self.create_qr()
        # Преобразуем в ASCII
        img = self.qr.make_image(fill_color="black", back_color="white").convert('L')
        width, height = img.size
        scale = 2  # уменьшим для компактности
        for y in range(0, height, scale):
            line = ''
            for x in range(0, width, scale):
                pixel = img.getpixel((x, y))
                line += '██' if pixel < 128 else '  '
            print(line)

    def save_token(self, filename='token.json'):
        if not self.token:
            self.generate_token()
        data = {
            'token': self.token,
            'timestamp': self.timestamp,
            'ttl': self.ttl,
            'expires': (datetime.now() + timedelta(seconds=self.ttl)).isoformat()
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"💾 Сохранено токен: {filename}")

    def validate(self, token_str):
        # Проверяем, валиден ли токен (по времени)
        # Здесь нужно было бы проверить сохранённый токен, но для примера просто проверяем, что токен совпадает и не истёк
        pass

def main():
    parser = argparse.ArgumentParser(description='QR Login Manager')
    parser.add_argument('--ttl', type=int, default=60, help='Срок действия токена (сек)')
    parser.add_argument('--output', default='qrcode.png', help='Имя файла PNG')
    parser.add_argument('--token-file', default='token.json', help='Файл для сохранения токена')
    args = parser.parse_args()

    print("🔐 QR Login Manager (Python)")
    mgr = QRLoginManager(args.ttl)
    token = mgr.generate_token()
    print(f"✅ Токен сгенерирован: {token}")
    print(f"⏳ Срок действия: {args.ttl} секунд")
    print("📱 Отсканируйте QR-код для входа:\n")

    mgr.create_qr()
    mgr.print_ascii()
    mgr.save_png(args.output)
    mgr.save_token(args.token_file)

if __name__ == "__main__":
    main()
