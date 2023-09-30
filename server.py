from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Verilerin depolandığı JSON dosyasını okuma
with open("db.json", "r") as json_file:
    veriler = json.load(json_file)

@app.route("/")
def hello():
    return "Merhaba, Dünya!"

@app.route("/kaydet", methods=["GET"])
def kaydet():
    try:
        kullaniciAdi = request.args.get("kullanici_adi")
        ogrenciNo = request.args.get("ogrenci_no")

        # Kullanıcı adının benzersiz olup olmadığını kontrol et
        kullaniciVarMi = any(
            kullanici["nickname"] == kullaniciAdi for kullanici in veriler["kullanicilar"]
        )

        if kullaniciVarMi:
            # Kullanıcı adı zaten alınmışsa 409 Conflict yanıtını gönder
            return jsonify({"message": "Bu kullanıcı adı zaten kullanılıyor."}), 400
        else:
            yeniKullanici = {
                "nickname": kullaniciAdi,
                "ogrenciNo": ogrenciNo,
                "yakalananPokemonlar": [],
            }

            veriler["kullanicilar"].append(yeniKullanici)

            # Verileri JSON dosyasına yazma
            with open("db.json", "w") as json_file:
                json.dump(veriler, json_file, indent=4)

            return jsonify({"message": "Kaydınız başarıyla tamamlandı!"}), 200
    except Exception as error:
        return jsonify({"message": str(error)}), 500

@app.route("/pokemon-ekle", methods=["GET"])
def pokemon_ekle():
    ogrenciNo = request.args.get("ogrenciNo")
    yeniPokemon = request.args.get("yeniPokemon")

    # Öğrenci numarasına göre kullanıcıyı bul
    kullanici = next(
        (
            kullanici
            for kullanici in veriler["kullanicilar"]
            if kullanici["ogrenciNo"] == ogrenciNo
        ),
        None,
    )

    # Kullanıcı bulunamazsa hata mesajı döndür
    if not kullanici:
        return jsonify({"error": "Kullanıcı bulunamadı"}), 404

    # Yeni Pokémon'i kullanıcının listesine ekle
    if yeniPokemon not in kullanici["yakalananPokemonlar"]:
        kullanici["yakalananPokemonlar"].append(yeniPokemon)

    # Verileri JSON dosyasına yazma
    with open("db.json", "w") as json_file:
        json.dump(veriler, json_file, indent=4)

    return jsonify({"message": yeniPokemon + " başarıyla yakalandı."}), 200

@app.route("/giris", methods=["GET"])
def giris():
    ogrenciNo = request.args.get("ogrenciNo")
    kullanici = next(
        (
            kullanici
            for kullanici in veriler["kullanicilar"]
            if kullanici["ogrenciNo"] == ogrenciNo
        ),
        None,
    )
    if kullanici:
        return jsonify({"message": "Giriş başarılı"}), 200
    else:
        return jsonify({"message": "Bu öğrenci numarası kayıtlı değil"}), 401

if __name__ == "__main__":
    app.run(port=3000)
