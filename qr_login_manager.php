<?php
// qr_login_manager.php — PHP версия

require_once 'vendor/autoload.php'; // для endroid/qr-code

use Endroid\QrCode\Builder\Builder;
use Endroid\QrCode\Writer\PngWriter;
use Endroid\QrCode\Encoding\Encoding;
use Endroid\QrCode\ErrorCorrectionLevel\ErrorCorrectionLevelLow;

$ttl = isset($argv[1]) ? (int)$argv[1] : 60;
$outputFile = isset($argv[2]) ? $argv[2] : 'qrcode.png';
$tokenFile = isset($argv[3]) ? $argv[3] : 'token.json';

echo "🔐 QR Login Manager (PHP)\n";
$token = uniqid('', true);
$now = date('c');
$expires = date('c', time() + $ttl);

echo "✅ Токен сгенерирован: $token\n";
echo "⏳ Срок действия: $ttl секунд\n";
echo "📱 Отсканируйте QR-код для входа:\n\n";

$data = ['token' => $token, 'timestamp' => $now, 'ttl' => $ttl, 'expires' => $expires];
$qrData = json_encode($data);

// Генерация QR с помощью endroid/qr-code
$result = Builder::create()
    ->writer(new PngWriter())
    ->data($qrData)
    ->encoding(new Encoding('UTF-8'))
    ->errorCorrectionLevel(new ErrorCorrectionLevelLow())
    ->size(300)
    ->build();

// Сохранение PNG
$result->saveToFile($outputFile);
echo "💾 Сохранено PNG: $outputFile\n";

// Сохранение токена
file_put_contents($tokenFile, json_encode($data, JSON_PRETTY_PRINT));
echo "💾 Сохранено токен: $tokenFile\n";

// Вывод ASCII (простой вариант - только для демонстрации, обычно не выводим)
// Можно использовать библиотеку для ASCII, но для простоты пропустим.
?>
