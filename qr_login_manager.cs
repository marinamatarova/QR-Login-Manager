// qr_login_manager.cs — C# версия

using System;
using System.IO;
using System.Text.Json;
using QRCoder;

class TokenData
{
    public string Token { get; set; }
    public string Timestamp { get; set; }
    public int Ttl { get; set; }
    public string Expires { get; set; }
}

class Program
{
    static void Main(string[] args)
    {
        int ttl = 60;
        string outputFile = "qrcode.png";
        string tokenFile = "token.json";
        if (args.Length > 0) ttl = int.Parse(args[0]);
        if (args.Length > 1) outputFile = args[1];
        if (args.Length > 2) tokenFile = args[2];

        Console.WriteLine("🔐 QR Login Manager (C#)");
        string token = Guid.NewGuid().ToString();
        string now = DateTime.UtcNow.ToString("o");
        string expires = DateTime.UtcNow.AddSeconds(ttl).ToString("o");

        Console.WriteLine($"✅ Токен сгенерирован: {token}");
        Console.WriteLine($"⏳ Срок действия: {ttl} секунд");
        Console.WriteLine("📱 Отсканируйте QR-код для входа:\n");

        var data = new TokenData { Token = token, Timestamp = now, Ttl = ttl, Expires = expires };
        string qrData = JsonSerializer.Serialize(data);

        // Генерация QR
        QRCodeGenerator qrGenerator = new QRCodeGenerator();
        QRCodeData qrCodeData = qrGenerator.CreateQrCode(qrData, QRCodeGenerator.ECCLevel.Q);
        QRCode qrCode = new QRCode(qrCodeData);
        var bitmap = qrCode.GetGraphic(20);
        bitmap.Save(outputFile, System.Drawing.Imaging.ImageFormat.Png);
        Console.WriteLine($"💾 Сохранено PNG: {outputFile}");

        // Сохранение токена
        File.WriteAllText(tokenFile, JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true }));
        Console.WriteLine($"💾 Сохранено токен: {tokenFile}");
    }
}
