// qr_login_manager.js — JavaScript версия

const QRCode = require('qrcode');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');

const ttl = parseInt(process.argv[2]) || 60;
const outputFile = process.argv[3] || 'qrcode.png';
const tokenFile = process.argv[4] || 'token.json';

console.log('🔐 QR Login Manager (JavaScript)');
const token = uuidv4();
const now = new Date().toISOString();
const expires = new Date(Date.now() + ttl * 1000).toISOString();

console.log(`✅ Токен сгенерирован: ${token}`);
console.log(`⏳ Срок действия: ${ttl} секунд`);
console.log('📱 Отсканируйте QR-код для входа:\n');

const data = { token, timestamp: now, ttl, expires };
const qrData = JSON.stringify(data);

// Вывод ASCII QR
QRCode.toString(qrData, { type: 'terminal', small: true }, (err, string) => {
    if (err) throw err;
    console.log(string);
});

// Сохранение PNG
QRCode.toFile(outputFile, qrData, { width: 300 }, (err) => {
    if (err) throw err;
    console.log(`💾 Сохранено PNG: ${outputFile}`);
});

// Сохранение токена
fs.writeFileSync(tokenFile, JSON.stringify(data, null, 2));
console.log(`💾 Сохранено токен: ${tokenFile}`);
