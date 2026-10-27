from models import BasiliKitap, EKitap, Ogrenci, Akademisyen
from library import Kutuphane

def sayi_al(mesaj, sifir_kabul = False):
    while True:
        try:
            sayi = int(input(mesaj))

            if sayi < 0 or (sayi == 0 and not sifir_kabul): # sifir_kabul = False; buna varsayılan değerli parametre denir 
                print("Geçersiz sayı.")
                continue

            return sayi
        except ValueError:
            print("Lütfen geçerli bir tam sayı girin.")


def metin_al(mesaj):
    while True:
        deger = input(mesaj).strip() # strip() metodu baştaki ve sondaki boşlukları silen fonk.
        if deger:
            return deger
        print("Boş değer girilemez.") 

def kitap_ekleme(sistem):
    kitap_id = sayi_al("Kitap ID: ")
    ad = metin_al("Kitap adı: ")
    yazar = metin_al("Yazar: ")
    kategori = metin_al("Kategori: ")

    print("1. Basılı Kitap")
    print("2. E-Kitap")
    tur = input("Tür: ").strip()

    if tur == "1":
        stok = sayi_al("Stok: ", sifir_kabul=True)
        raf = metin_al("Raf numarası: ")
        kitap = BasiliKitap(kitap_id, ad, yazar, kategori, stok, raf)
    elif tur == "2":
        format = metin_al("Dosya formatı (PDF/EPUB): ")
        kitap = EKitap(kitap_id, ad, yazar, kategori, format)
    else:
        raise ValueError("Geçersiz kitap türü.")

    sistem.kitap_ekle(kitap)
    print("Kitap başarıyla eklendi.")


def uye_ekleme(sistem):
    uye_id = sayi_al("Üye ID: ")
    ad = metin_al("Ad Soyad: ")

    print("1. Öğrenci")
    print("2. Akademisyen")
    tur = input("Üye türü: ").strip()

    if tur == "1":
        uye = Ogrenci(uye_id, ad)
    elif tur == "2":
        uye = Akademisyen(uye_id, ad)
    else:
        raise ValueError("Geçersiz üye türü.")

    sistem.uye_ekle(uye)
    print("Üye başarıyla kaydedildi.")

def kitaplari_yazdir(kitaplar):
    if not kitaplar:
        print("Kitap bulunamadı.")
        return

    for kitap in kitaplar:
        print("-" * 40)
        print(kitap.bilgileri_goster())


def odunc_verme(sistem):
    uye_id = sayi_al("Üye ID: ")
    kitap_id = sayi_al("Kitap ID: ")

    kitap = sistem.odunc_ver(uye_id, kitap_id)
    print(f"'{kitap.ad}' ödünç verildi.")


def iade_islemi(sistem):
    uye_id = sayi_al("Üye ID: ")
    kitap_id = sayi_al("Kitap ID: ")

    kitap = sistem.iade_al(uye_id, kitap_id)
    print(f"'{kitap.ad}' iade edildi.")

def uye_kitaplarini_goster(sistem):
    uye_id = sayi_al("Üye ID: ")
    uye = sistem.uye_bul(uye_id)

    print(uye.bilgileri_goster())

    if not uye.odunc_kitaplar:
        print("Üyenin aktif ödünç kitabı yok.")
        return

    for kitap_id in uye.odunc_kitaplar:
        kitap = sistem.kitap_bul(kitap_id)
        print(kitap.bilgileri_goster())


def rapor_goster(sistem):
    rapor = sistem.rapor_olustur()

    print("\n========== KÜTÜPHANE RAPORU ==========")
    print(f"Kitap Çeşidi: {rapor['kitap_cesidi']}")
    print(f"Basılı Kitap Stoğu: {rapor['basili_stok']}")
    print(f"Toplam Üye: {rapor['uye_sayisi']}")
    print(f"Öğrenci: {rapor['ogrenci']}")
    print(f"Akademisyen: {rapor['akademisyen']}")
    print(f"Aktif Ödünç: {rapor['aktif_odunc']}")
    print(f"En Popüler Kitap: {rapor['en_populer']}")

def menu_goster():
    print("\n========== KÜTÜPHANE SİSTEMİ ==========")
    print("1. Kitap Ekle")
    print("2. Üye Kaydet")
    print("3. Kitap Ödünç Ver")
    print("4. Kitap İade Al")
    print("5. Kitap Ara")
    print("6. Kategoriye Göre Listele")
    print("7. Tüm Kitapları Listele")
    print("8. Üyenin Kitaplarını Göster")
    print("9. Kütüphane Raporu")
    print("0. Çıkış")
    print("======================================")


def main():
    sistem = Kutuphane()

    while True:
        menu_goster()
        secim = input("Seçiminiz: ").strip()

        try:
            if secim == "1":
                kitap_ekleme(sistem)

            elif secim == "2":
                uye_ekleme(sistem)

            elif secim == "3":
                odunc_verme(sistem)

            elif secim == "4":
                iade_islemi(sistem)

            elif secim == "5":
                aranan = metin_al("Kitap adı: ")
                kitaplari_yazdir(sistem.kitap_ara(aranan))

            elif secim == "6":
                kategori = metin_al("Kategori: ")
                kitaplari_yazdir(
                    sistem.kategoriye_gore_listele(kategori)
                )

            elif secim == "7":
                kitaplari_yazdir(
                    list(sistem.kitaplar.values())
                )

            elif secim == "8":
                uye_kitaplarini_goster(sistem)

            elif secim == "9":
                rapor_goster(sistem)

            elif secim == "0":
                print("Program kapatılıyor.")
                break

            else:
                print("Geçersiz menü seçimi.")

        except ValueError as hata:
            print(f"Hata: {hata}")

        except (KeyboardInterrupt, EOFError):
            print("\nProgram sonlandırılıyor.")
            break


if __name__ == "__main__":
    main()