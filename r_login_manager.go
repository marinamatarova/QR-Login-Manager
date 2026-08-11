// qr_login_manager.go — Go версия

package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"time"

	"github.com/google/uuid"
	qrcode "github.com/skip2/go-qrcode"
)

type TokenData struct {
	Token     string `json:"token"`
	Timestamp string `json:"timestamp"`
	TTL       int    `json:"ttl"`
	Expires   string `json:"expires"`
}

func main() {
	ttl := flag.Int("ttl", 60, "Срок действия токена (сек)")
	output := flag.String("output", "qrcode.png", "Имя файла PNG")
	tokenFile := flag.String("token-file", "token.json", "Файл для сохранения токена")
	flag.Parse()

	fmt.Println("🔐 QR Login Manager (Go)")
	token := uuid.New().String()
	now := time.Now().Format(time.RFC3339)
	expires := time.Now().Add(time.Duration(*ttl) * time.Second).Format(time.RFC3339)

	fmt.Printf("✅ Токен сгенерирован: %s\n", token)
	fmt.Printf("⏳ Срок действия: %d секунд\n", *ttl)
	fmt.Println("📱 Отсканируйте QR-код для входа:\n")

	data := TokenData{
		Token:     token,
		Timestamp: now,
		TTL:       *ttl,
		Expires:   expires,
	}
	jsonData, _ := json.Marshal(data)
	qrStr := string(jsonData)

	qr, err := qrcode.New(qrStr, qrcode.Medium)
	if err != nil {
		fmt.Printf("Ошибка генерации QR: %v\n", err)
		return
	}
	// Вывод ASCII
	fmt.Println(qr.ToSmallString(false))
	// Сохранение PNG
	err = qr.WriteFile(256, *output)
	if err != nil {
		fmt.Printf("Ошибка сохранения PNG: %v\n", err)
	} else {
		fmt.Printf("💾 Сохранено PNG: %s\n", *output)
	}
	// Сохранение токена в JSON
	fileData, _ := json.MarshalIndent(data, "", "  ")
	err = os.WriteFile(*tokenFile, fileData, 0644)
	if err != nil {
		fmt.Printf("Ошибка сохранения токена: %v\n", err)
	} else {
		fmt.Printf("💾 Сохранено токен: %s\n", *tokenFile)
	}
}
