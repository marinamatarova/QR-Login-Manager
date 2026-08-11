// qr_login_manager.rs — Rust версия

use qrcode::QrCode;
use qrcode::render::unicode;
use uuid::Uuid;
use chrono::{Utc, Duration};
use std::fs;
use std::env;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    let ttl: i64 = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(60);
    let output_file = args.get(2).unwrap_or(&"qrcode.png".to_string()).clone();
    let token_file = args.get(3).unwrap_or(&"token.json".to_string()).clone();

    println!("🔐 QR Login Manager (Rust)");
    let token = Uuid::new_v4().to_string();
    let now = Utc::now().to_rfc3339();
    let expires = (Utc::now() + Duration::seconds(ttl)).to_rfc3339();

    println!("✅ Токен сгенерирован: {}", token);
    println!("⏳ Срок действия: {} секунд", ttl);
    println!("📱 Отсканируйте QR-код для входа:\n");

    let data = serde_json::json!({
        "token": token,
        "timestamp": now,
        "ttl": ttl,
        "expires": expires
    });
    let qr_data = serde_json::to_string(&data)?;

    let qr = QrCode::new(qr_data.as_bytes())?;
    // ASCII вывод
    let image = qr.render::<unicode::Dense1x2>().build();
    println!("{}", image);

    // PNG сохранение
    let img = qr.render::<qrcode::render::svg::Color>().build();
    let svg = img.to_string();
    // Для PNG используем библиотеку image, но для простоты сохраним SVG
    // В реальности можно использовать image-rs для PNG.
    // Вместо PNG сохраним SVG для простоты.
    let svg_filename = output_file.replace(".png", ".svg");
    fs::write(&svg_filename, svg)?;
    println!("💾 Сохранено SVG: {}", svg_filename);

    // Сохранение токена
    let json = serde_json::to_string_pretty(&data)?;
    fs::write(token_file, json)?;
    println!("💾 Сохранено токен: {}", token_file);

    Ok(())
}
