// qr_login_manager.java — Java версия

import com.google.zxing.BarcodeFormat;
import com.google.zxing.WriterException;
import com.google.zxing.client.j2se.MatrixToImageWriter;
import com.google.zxing.common.BitMatrix;
import com.google.zxing.qrcode.QRCodeWriter;

import java.io.IOException;
import java.nio.file.FileSystems;
import java.nio.file.Path;
import java.util.UUID;
import java.time.Instant;
import java.time.format.DateTimeFormatter;

public class qr_login_manager {
    public static void main(String[] args) throws WriterException, IOException {
        int ttl = 60;
        String outputFile = "qrcode.png";
        String tokenFile = "token.json";
        if (args.length > 0) ttl = Integer.parseInt(args[0]);
        if (args.length > 1) outputFile = args[1];
        if (args.length > 2) tokenFile = args[2];

        System.out.println("🔐 QR Login Manager (Java)");
        String token = UUID.randomUUID().toString();
        String now = Instant.now().toString();
        String expires = Instant.now().plusSeconds(ttl).toString();

        System.out.println("✅ Токен сгенерирован: " + token);
        System.out.println("⏳ Срок действия: " + ttl + " секунд");
        System.out.println("📱 Отсканируйте QR-код для входа:\n");

        String qrData = "{\"token\":\"" + token + "\",\"timestamp\":\"" + now + "\",\"ttl\":" + ttl + ",\"expires\":\"" + expires + "\"}";

        // Генерация QR
        QRCodeWriter qrCodeWriter = new QRCodeWriter();
        BitMatrix bitMatrix = qrCodeWriter.encode(qrData, BarcodeFormat.QR_CODE, 300, 300);
        Path path = FileSystems.getDefault().getPath(outputFile);
        MatrixToImageWriter.writeToPath(bitMatrix, "PNG", path);
        System.out.println("💾 Сохранено PNG: " + outputFile);

        // Сохранение токена
        String json = String.format("{\"token\":\"%s\",\"timestamp\":\"%s\",\"ttl\":%d,\"expires\":\"%s\"}", token, now, ttl, expires);
        java.nio.file.Files.write(java.nio.file.Paths.get(tokenFile), json.getBytes());
        System.out.println("💾 Сохранено токен: " + tokenFile);
    }
}
