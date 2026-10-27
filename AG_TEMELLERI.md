# Ağ Temelleri (Networking) Raporu

Bu raporda bir yazılımın internet üzerinden nasıl iletişim kurduğunu inceliyorum. Her konuyu açıkladıktan sonra kendi bilgisayarımda ilgili komutları çalıştırarak gözlemlerimi ekledim.

## İçindekiler

1. [Genel Bakış](#genel-bakış)
2. [IP Adresi](#1-ip-adresi)
3. [Port](#2-port)
4. [DNS](#3-dns)
5. [TCP](#4-tcp)
6. [UDP ve TCP Karşılaştırması](#5-udp-ve-tcp-karşılaştırması)
7. [Paket Yapısı](#6-paket-yapısı)
8. [Ağ Araçları: ping, tracert, nslookup](#7-ağ-araçları-ping-tracert-nslookup)
9. [Sonuç: Tarayıcıya Bir Adres Yazınca Ne Olur?](#8-sonuç-tarayıcıya-bir-adres-yazınca-ne-olur)

---

## Genel Bakış

İnternetteki iletişim, kurallarla işleyen bir posta sistemine benzer. Bu kurallara **protokol** denir: iki cihazın nasıl iletişim kuracağını belirleyen ortak kurallar bütünü. IP, TCP, UDP, DNS ve HTTP birer protokoldür.

| Posta sisteminde | Ağda |
| --- | --- |
| Apartmanın sokak adresi | IP adresi |
| Daire numarası | Port |
| Adres defteri | DNS |
| İadeli taahhütlü mektup | TCP |
| Kartpostal | UDP |
| Zarf ve üzerindeki etiketler | Paket |

---

## 1. IP Adresi

**IP (Internet Protocol) adresi, ağdaki bir cihazın adresidir.** Verinin doğru cihaza ulaşmasını sağlar.

### IPv4 ve IPv6

- **IPv4:** 32 bitlik, `192.168.1.25` gibi dört sayıdan oluşan adres. Her sayı 0–255 arasındadır. Yaklaşık 4,3 milyar adres içerir ve bu sayı günümüzde yetersiz kalmıştır.
- **IPv6:** 128 bitlik, `2001:db8::8a2e:370:7334` gibi yazılan adres. Pratikte tükenmeyecek kadar geniş bir adres alanı sunar.

### Özel IP, genel IP ve NAT

| | Özel (Private) IP | Genel (Public) IP |
| --- | --- | --- |
| Geçerli olduğu yer | Yalnızca yerel ağ | Tüm internet |
| Veren | Modem / yerel ağ | İnternet servis sağlayıcı |
| Örnek aralıklar | `10.x.x.x`, `172.16–31.x.x`, `192.168.x.x` | Bu aralıkların dışındaki adresler |

- **NAT (Network Address Translation):** Yerel ağdaki birçok cihazın tek bir genel IP ile internete çıkmasını sağlar. Modem, giden paketlerdeki özel IP'yi kendi genel IP'siyle değiştirir.
- **127.0.0.1 (localhost):** Cihazın kendisini ifade eder. Bu adrese giden veri ağa çıkmaz.
- **Varsayılan ağ geçidi (default gateway):** Yerel ağın dışına giden trafiğin gönderildiği cihaz, genellikle modem.
- **Alt ağ maskesi (subnet mask):** IP adresinin hangi kısmının ağı, hangi kısmının cihazı gösterdiğini belirler.

### Kendi bilgisayarımda: `ipconfig`

```
ipconfig
```

| Bilgi | Değer | Yorum |
| --- | --- | --- |
| IPv4 adresi | 10.15.9.223 | 10.x.x.x aralığında, yani özel IP |
| Alt ağ maskesi | 255.255.248.0 | İlk 21 bit ağı, kalan 11 bit cihazı gösterir; bu ağda yaklaşık 2000 cihaz olabilir |
| Varsayılan ağ geçidi | 10.15.8.1 | Ağın dışına çıkan veriler önce buraya gider |
| Link-local IPv6 | fe80:: ile başlayan adres | Yalnızca yerel ağda kullanılan IPv6 adresi |
| WSL sanal adaptörü | 172.18.240.1 | Windows'un Linux alt sistemiyle iletişim için kurduğu sanal ağ |

Bilgisayarımda üç özel IP aralığından ikisini (`10.x.x.x` ve `172.16–31.x.x`) gözlemledim. IP adresim ile ağ geçidimin son iki sayısı farklı görünse de alt ağ maskesi sayesinde ikisinin aynı ağda (`10.15.8.0 – 10.15.15.255`) olduğunu anladım.

---

## 2. Port

**Port, bir cihaz üzerinde çalışan uygulamalardan hangisine gidileceğini gösteren numaradır.** IP adresi doğru cihazı, port ise o cihazdaki doğru programı bulur.

Port numaraları 0–65535 arasındadır. 0–1023 arası bilinen servislere ayrılmıştır (well-known ports). Bir IP adresi ile bir portun birleşimine **soket (socket)** denir: `142.250.187.110:443`.

| Port | Servis | Kullanım |
| --- | --- | --- |
| 80 | HTTP | Şifresiz web trafiği |
| 443 | HTTPS | Şifreli web trafiği |
| 53 | DNS | Alan adı çözümleme |
| 22 | SSH | Güvenli uzak terminal bağlantısı |
| 21 | FTP | Dosya aktarımı |
| 25 | SMTP | E-posta gönderimi |
| 3306 | MySQL | Veritabanı bağlantısı |
| 5432 | PostgreSQL | Veritabanı bağlantısı |

Aynı IP adresinde aynı portu aynı anda yalnızca bir program dinleyebilir. İkinci bir program aynı portu kullanmaya çalışırsa "port already in use" hatası oluşur.

---

## 3. DNS

**DNS (Domain Name System), alan adlarını IP adreslerine çeviren sistemdir.** İnsanlar `google.com` gibi isimleri hatırlar; bilgisayarlar ise IP adresleriyle çalışır.

### Bir DNS sorgusu nasıl çözülür?

1. **Önbellek:** Tarayıcı ve işletim sistemi, adresi yakın zamanda öğrenip öğrenmediğine bakar.
2. **Çözümleyici (resolver):** Bulunamazsa soru bir DNS sunucusuna gider (servis sağlayıcının sunucusu ya da `8.8.8.8` gibi genel bir sunucu).
3. **Kök sunucu (root):** Çözümleyici bilmiyorsa kök sunucuya sorar; kök sunucu ilgili TLD sunucusunu gösterir.
4. **TLD sunucusu:** `.com` sunucusu, alan adını yöneten sunucuyu gösterir.
5. **Yetkili sunucu (authoritative):** Alan adının kendi DNS sunucusu IP adresini verir.
6. Cevap geri dönerken önbelleğe alınır.

### DNS kayıt türleri

| Kayıt | Tuttuğu bilgi |
| --- | --- |
| A | Alan adının IPv4 adresi |
| AAAA | Alan adının IPv6 adresi |
| CNAME | Başka bir alan adına yönlendirme (takma ad) |
| MX | E-postaların teslim edileceği sunucu |
| NS | Alan adını yöneten DNS sunucuları |
| TXT | Serbest metin, genellikle doğrulama amaçlı |

**TTL (Time To Live):** Bir kaydın önbellekte ne kadar süre tutulacağını belirtir. Bir sitenin IP'si değiştiğinde değişikliğin herkese aynı anda yansımamasının nedeni budur.

DNS genellikle **UDP** ve **53 numaralı port** üzerinden çalışır, çünkü sorgular kısadır ve hızlı yanıt gerektirir.

---

## 4. TCP

**TCP (Transmission Control Protocol), verinin eksiksiz, hatasız ve doğru sırada ulaşmasını garanti eden, bağlantı tabanlı bir protokoldür.**

### Üçlü el sıkışma (3-way handshake)

TCP veri göndermeden önce bağlantı kurar:

1. **SYN** (istemci → sunucu): Bağlantı isteği
2. **SYN-ACK** (sunucu → istemci): İsteğin kabulü ve onayı
3. **ACK** (istemci → sunucu): Onayın onayı; bağlantı kuruldu

Bağlantı sonlandırılırken **FIN** ve **ACK** mesajları kullanılır.

### TCP güvenilirliği nasıl sağlar?

- **Sıra numaraları:** Paketler alıcıda doğru sıraya dizilir.
- **Onay (ACK):** Alıcı aldığı veriyi onaylar.
- **Yeniden gönderme:** Onay gelmeyen paketler tekrar gönderilir.
- **Checksum:** Yolda bozulan paketler tespit edilir.
- **Akış kontrolü:** Gönderici, alıcının kapasitesine göre hızını ayarlar.

**Kullanım alanları:** Web sayfaları (HTTP/HTTPS), e-posta, dosya indirme, SSH, veritabanı bağlantıları.

---

## 5. UDP ve TCP Karşılaştırması

**UDP (User Datagram Protocol), bağlantı kurmadan ve onay beklemeden veri gönderen hızlı bir protokoldür.** Teslim, sıra ya da yeniden gönderme garantisi vermez.

Bazı uygulamalarda geç gelen veri, hiç gelmeyen veriden daha zararlıdır. Örneğin görüntülü bir aramada kaybolan bir kareyi sonradan göndermenin anlamı yoktur; görüntünün akmaya devam etmesi daha önemlidir.

| | TCP | UDP |
| --- | --- | --- |
| Bağlantı | Önce kurulur (3-way handshake) | Kurulmaz |
| Teslim garantisi | Var | Yok |
| Sıra | Korunur | Korunmaz |
| Kayıp paket | Tekrar gönderilir | Gönderilmez |
| Hız | Daha yavaş | Daha hızlı |
| Kullanım | Web, e-posta, dosya aktarımı, SSH | Görüntülü/sesli arama, online oyun, canlı yayın, DNS |

**Seçim kriteri:** "Bir parça eksik gelirse ne olur?" Veri bozuluyorsa TCP, yalnızca anlık bir takılma oluyorsa UDP tercih edilir.

---

## 6. Paket Yapısı

**Paket, ağda taşınan küçük veri parçasıdır ve iki bölümden oluşur: başlık (header) ve yük (payload).** Başlık adres ve kontrol bilgilerini, yük ise asıl veriyi taşır.

Veri paketlere bölünür, çünkü bir hata olduğunda yalnızca bozulan parça tekrar gönderilir ve ağ birçok kullanıcı arasında paylaşılabilir. Bir paket genellikle en fazla yaklaşık 1500 bayttır (MTU).

### Kapsülleme (encapsulation)

Veri gönderilirken her katman, üst katmandan gelen veriyi kendi başlığını ekleyerek sarmalar:

```
[ Ethernet/Wi-Fi başlığı | IP başlığı | TCP/UDP başlığı | Uygulama verisi ]
      MAC adresleri         IP adresleri      Port numaraları     ör. HTTP isteği
```

| Katman (TCP/IP modeli) | Eklenen başlıktaki önemli bilgiler |
| --- | --- |
| Uygulama | Asıl veri (ör. HTTP isteği) |
| Taşıma (TCP/UDP) | Kaynak ve hedef port; TCP'de sıra/onay numaraları ve SYN, ACK, FIN bayrakları |
| İnternet (IP) | Kaynak ve hedef IP adresi, TTL, taşınan protokol |
| Bağlantı (Ethernet/Wi-Fi) | Kaynak ve hedef MAC adresi |

Alıcı tarafta bu işlemin tersi (decapsulation) yapılır: her katman kendi başlığını okuyup kaldırır ve veriyi üst katmana iletir.

- **MAC adresi:** Ağ kartının donanımsal kimliği. IP adresi son hedefi, MAC adresi bir sonraki durağı gösterir.
- **TTL:** IP başlığındaki sayaç. Paket her router'dan geçtiğinde 1 azalır; 0 olunca paket atılır. Böylece kaybolan paketler ağda sonsuza kadar dolaşmaz.

### OSI modeli

OSI modeli aynı süreci 7 katmanda inceler: Fiziksel, Veri Bağlantı, Ağ, Taşıma, Oturum, Sunum, Uygulama. **IP 3. katmanda, TCP ve UDP 4. katmanda, HTTP ve DNS 7. katmanda** çalışır.

---

## 7. Ağ Araçları: ping, tracert, nslookup

| Komut | Amacı |
| --- | --- |
| `ping` | Hedefe ulaşılabiliyor mu ve yanıt süresi ne? |
| `tracert` | Paket hedefe giderken hangi duraklardan geçiyor? |
| `nslookup` | Bir alan adının IP adresi ne? |

### ping

ICMP protokolüyle hedefe "Echo Request" gönderir ve "Echo Reply" bekler. Çıktıda yanıt süresi (ms), TTL ve paket kaybı oranı görülür. `Request timed out` her zaman hedefin kapalı olduğunu göstermez; bazı sunucular güvenlik nedeniyle ICMP'ye yanıt vermez.


### tracert

Paketin hedefe giderken geçtiği her router'ı (hop) listeler. Çalışma mantığı TTL'ye dayanır: önce TTL=1 olan paket gönderilir, ilk router TTL'yi sıfırlayıp "Time Exceeded" mesajı döndürür ve böylece ilk durak öğrenilir. TTL her seferinde bir artırılarak hedefe kadar tüm duraklar bulunur. `* * *` satırı, o durağın yanıt vermediğini gösterir.


### nslookup

DNS sunucusuna doğrudan sorgu gönderir ve alan adının IP adreslerini gösterir. Çıktının üst kısmı sorgunun gönderildiği DNS sunucusunu, alt kısmı alan adı ve IP adreslerini gösterir. "Non-authoritative answer" ifadesi, cevabın yetkili sunucudan değil bir önbellekten geldiğini belirtir.


### Sorun giderme sırası

İnternet bağlantısı sorunlarında şu sırayla ilerlenebilir:

1. `ipconfig` → Cihaz IP adresi almış mı?
2. `ping 10.15.8.1` (ağ geçidi) → Yerel ağ çalışıyor mu?
3. `ping 8.8.8.8` → İnternete çıkılabiliyor mu?
4. `ping google.com` → DNS çalışıyor mu? (3 çalışıp 4 çalışmıyorsa sorun DNS'tedir.)
5. `tracert` → Bağlantı hangi noktada kopuyor?

---

## 8. Sonuç: Tarayıcıya Bir Adres Yazınca Ne Olur?

Bu raporda incelenen tüm kavramlar, tarayıcıya `google.com` yazıldığında yaşanan süreçte bir araya gelir:

1. **DNS:** `google.com` alan adı bir IP adresine çevrilir (UDP, port 53).
2. **TCP:** Bu IP adresinin 443 numaralı portuna üçlü el sıkışma ile bağlantı kurulur.
3. **TLS:** HTTPS kullanıldığı için iletişim şifrelenir.
4. **HTTP:** Tarayıcı sayfa isteğini gönderir.
5. **Paket:** İstek paketlere bölünür; her pakete port, IP ve MAC bilgileri eklenir.
6. **Yönlendirme:** Paketler ağ geçidine gider, NAT ile genel IP'ye çevrilir ve router'lar üzerinden hedefe ulaşır.
7. **Yanıt:** Sunucu sayfayı paketler hâlinde geri gönderir; TCP paketleri doğru sıraya koyar.
8. **Gösterim:** Tarayıcı gelen içeriği işleyip sayfayı ekrana çizer.

Bu çalışma sayesinde bir yazılımın internette nasıl "konuştuğunu" katman katman öğrendim: IP doğru cihazı, port doğru programı bulur; DNS isimleri adreslere çevirir; TCP ve UDP verinin nasıl taşınacağını belirler; paketler ise tüm bu bilgileri başlıklarında taşıyarak veriyi hedefe ulaştırır.