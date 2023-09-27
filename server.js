const express = require('express');
const fs = require('fs');

const app = express();
const port = 3000;

app.use(express.static('public'));

// JSON verilerini yükle
let veriler = require('./db.json');

app.get('/', (req, res) => {
    res.send('Hoş Geldiniz!');
});

// Kayıt işlemi için GET isteği
app.get('/kaydet', (req, res) => {
    try {
        const kullaniciAdi = req.query.kullanici_adi;
        const ogrenciNo = req.query.ogrenci_no;

        // Yeni kullanıcı verisi oluştur
        const yeniKullanici = {
            nickname: kullaniciAdi,
            öğrenciNo: ogrenciNo,
        };

        // Yeni kullanıcı verisini ekleyin
        veriler.kullanicilar.push(yeniKullanici);

        // JSON verilerini güncel dosyaya yaz
        fs.writeFileSync('db.json', JSON.stringify(veriler, null, 4));

        res.json({ message: 'Kayıt başarıyla tamamlandı!' });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

app.listen(port, () => {
    console.log(`Sunucu ${port} portunda çalışıyor.`);
});
