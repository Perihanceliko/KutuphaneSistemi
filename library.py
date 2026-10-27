from models import BasiliKitap,EKitap, Ogrenci, Akademisyen
# import işlemi yaptık  models sınıfındaki classlaımızı burada kullanmak için 


class Kutuphane:
    def __init__(self):
        self.kitaplar = {}
        self.uyeler = {}

    def kitap_ekle(self, kitap):
        if kitap.kitap_id in self.kitaplar:
            raise ValueError("Bu kitap ID zaten kayıtlı.")

        self.kitaplar[kitap.kitap_id] = kitap

    def uye_ekle(self, uye):
        if uye.uye_id in self.uyeler:
            raise ValueError("Bu üye ID zaten kayıtlı.")

        self.uyeler[uye.uye_id] = uye

    def kitap_bul(self, kitap_id):
        if kitap_id not in self.kitaplar:
            raise ValueError("Kitap bulunamadı.")
        
        return self.kitaplar[kitap_id]

    def uye_bul(self, uye_id):
        if uye_id not in self.uyeler:
            raise ValueError("Üye bulunamadı")
        return self.uyeler[uye_id]

    def odunc_ver(self, uye_id, kitap_id):
        uye = self.uye_bul(uye_id)          # üye kayıtlı mı ?
        kitap = self.kitap_bul(kitap_id)    # kitap var mı ?

        if kitap_id in uye.odunc_kitaplar:
            raise ValueError("Üye bu kitabı zaten almış.")

        if not uye.kitap_alabilir_mi():
            raise ValueError("Üyenin ödünç alma limiti dolu.")

        if isinstance(kitap, BasiliKitap):
            kitap.stok_azalt()

        uye.odunc_kitaplar.append(kitap_id)  # listeye ekleme 
        kitap.odunc_sayisi += 1

        return kitap

    def iade_al(self, uye_id, kitap_id):
        uye = self.uye_bul(uye_id)
        kitap = self.kitap_bul(kitap_id)

        if kitap_id not in uye.odunc_kitaplar:
            raise ValueError("Bu kitap üyede bulunmuyor.")

        uye.odunc_kitaplar.remove(kitap_id)

        if isinstance(kitap, BasiliKitap):
            kitap.stok_artir()

        return kitap

    def kitap_ara(self, aranan):
        sonuc = []

        for kitap in self.kitaplar.values():
            if aranan.lower() in kitap.ad.lower():
                sonuc.append(kitap)

        return sonuc

    def kategoriye_gore_listele(self, kategori):
        sonuc = []

        for kitap in self.kitaplar.values():
            if kitap.kategori.lower() == kategori.lower():
                sonuc.append(kitap)

        return sonuc

    def rapor_olustur(self):
        toplam_stok = 0
        ogrenci_sayisi = 0
        akademisyen_sayisi = 0
        aktif_odunc = 0
        en_populer = None

        for kitap in self.kitaplar.values():
            if isinstance(kitap, BasiliKitap):
                toplam_stok += kitap.stok

            if en_populer is None:
                en_populer = kitap
            elif kitap.odunc_sayisi > en_populer.odunc_sayisi:
                en_populer = kitap

        for uye in self.uyeler.values():
            aktif_odunc += len(uye.odunc_kitaplar)

            if isinstance(uye, Ogrenci):
                ogrenci_sayisi += 1
            elif isinstance(uye, Akademisyen):
                akademisyen_sayisi += 1

        populer_ad = "Henüz ödünç alınan kitap yok"

        if en_populer is not None and en_populer.odunc_sayisi > 0:
            populer_ad = en_populer.ad

        return {
            "kitap_cesidi": len(self.kitaplar),
            "basili_stok": toplam_stok,
            "uye_sayisi": len(self.uyeler),
            "ogrenci": ogrenci_sayisi,
            "akademisyen": akademisyen_sayisi,
            "aktif_odunc": aktif_odunc,
            "en_populer": populer_ad
        }

