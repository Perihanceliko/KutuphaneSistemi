class Kitap:
    def __init__(self, kitap_id, ad, yazar, kategori, stok):
        if stok< 0:
            raise ValueError("Stok negatif olamaz.")
        
        self.kitap_id = kitap_id
        self.ad = ad
        self.yazar = yazar
        self.kategori = kategori
        self.stok = stok
        self.odunc_sayisi = 0

    def stok_azalt(self):
        if self.stok <= 0:
            raise ValueError("Kitap stokta yok.")
        self.stok -=1
    def stok_artir(self):
        self.stok += 1

    def bilgileri_goster(self):
        return (f"ID: {self.kitap_id} | "
            f"Ad: {self.ad} | "
            f"Yazar: {self.yazar} | "
            f"Kategori: {self.kategori} | "
            f"Stok: {self.stok} | "
            f"Ödünç: {self.odunc_sayisi}"
        )

class BasiliKitap(Kitap): # Basili_Kitap sınıfı , Kitap sınıfından miras aldı 
    def __init__(self, kitap_id, ad, yazar, kategori, stok, raf):
        super().__init__(kitap_id, ad, yazar, kategori, stok) # yukaridakinin yapıcısını çalıştırdık.
        self.raf = raf 

    def bilgileri_goster(self):
        return super().bilgileri_goster() + f" | Raf: {self.raf}"

class EKitap(Kitap):
    def __init__(self, kitap_id, ad, yazar, kategori, format):
        super().__init__(kitap_id, ad, yazar, kategori, 0)
        self.format = format

    def bilgileri_goster(self):
        return (
            f"ID: {self.kitap_id} | Ad: {self.ad} | "
            f"Yazar: {self.yazar} | Kategori: {self.kategori} | "
            f"E-Kitap: {self.format} | Ödünç: {self.odunc_sayisi}"
        )
    
class Uye:
    def __init__(self, uye_id, ad, limit):
        self.uye_id = uye_id
        self.ad = ad
        self.limit = limit
        self.odunc_kitaplar = []

    def kitap_alabilir_mi(self):
        return len(self.odunc_kitaplar) < self.limit

    def bilgileri_goster(self):
        return (
            f"ID: {self.uye_id} | Ad: {self.ad} | "
            f"Limit: {self.limit} | "
            f"Aktif: {len(self.odunc_kitaplar)}"
        )
    
class Ogrenci(Uye):
    def __init__(self, uye_id, ad):
        super().__init__(uye_id, ad, 3)


class Akademisyen(Uye):
    def __init__(self, uye_id, ad):
        super().__init__(uye_id, ad, 5)

