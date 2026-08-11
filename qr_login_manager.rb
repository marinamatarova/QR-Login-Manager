# qr_login_manager.rb — Ruby версия

require 'rqrcode'
require 'securerandom'
require 'json'
require 'time'

ttl = (ARGV[0] || 60).to_i
output_file = ARGV[1] || 'qrcode.png'
token_file = ARGV[2] || 'token.json'

puts "🔐 QR Login Manager (Ruby)"
token = SecureRandom.uuid
now = Time.now.utc.iso8601
expires = (Time.now.utc + ttl).iso8601

puts "✅ Токен сгенерирован: #{token}"
puts "⏳ Срок действия: #{ttl} секунд"
puts "📱 Отсканируйте QR-код для входа:\n"

data = { token: token, timestamp: now, ttl: ttl, expires: expires }
qr_data = data.to_json

# Генерация QR
qr = RQRCode::QRCode.new(qr_data)
# ASCII вывод
puts qr.to_s

# PNG сохранение (используем rqrcode_png)
require 'rqrcode_png'
png = qr.as_png(size: 300)
File.write(output_file, png.to_s)
puts "💾 Сохранено PNG: #{output_file}"

# Сохранение токена
File.write(token_file, JSON.pretty_generate(data))
puts "💾 Сохранено токен: #{token_file}"
