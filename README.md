# projektovanje-i-implementacija-sigurnog-softvera

Ova aplikacija implementira sigurnu chat komunikaciju između klijenata pomoću RabbitMQ servera koji radi na Linuxu i podržava TLS.
Korisnici se mogu registrovati sa jedinstvenim username-om i javnim ključem, a poruke se razmenjuju tako da su potpuno enkriptovane koristeći RSA.
Sistem koristi princip Sign-then-Encrypt, što omogućava i verifikaciju pošiljaoca i sigurnu enkripciju sadržaja poruke.
Klijentska aplikacija je konzolna i omogućava slanje i primanje poruka, uključujući proveru integriteta i autentičnosti poruka.
Klijenti rade na macOS-u, dok je server postavljen na Ubuntu mašini unutar VirtualBox virtuelne mašine.

## Postavka projekta

### Instalacija nove virtuelne mašine

**Virtual machine name and operating system:**  
- **VM Name:** Ubuntu  
- **ISO Image:** ubuntu-24.04.3-live-server-arm64.iso  
- **OS:** Linux  
- **OS Distribution:** Ubuntu  
- **OS Version:** Ubuntu 24.04 LTS (Noble Numbat) (ARM 64-bit)  
- **Opcija:** Odčekirati *Proceed with Unattended Installation*  

**Set up unattended guest OS installation:**  
- **Host name:** Ubuntu  
- **Domain name:** myquest.virtualbox.org  
- **Opcija:** Cekirati *Install Guest Additions*  
- **Guest Additions ISO Image:** `/Applications/Virtu...app/Contents/MacOS/VBoxGuestAdditions.iso`  

**Specify virtual hardware:**  
- **Base memory:** 4096 MB  
- **Number of CPUs:** 4  
- **Opcija:** Cekirano *Use EFI*  

**Create a new virtual hard disk:**  
- **Disk path:** `/Users/andreavalcic/VirtualBox VMs/Ubuntu/Ubuntu.vdi`  
- **Disk size:** 60.00 GB  


### Network konfiguracija virtuelne mašine
**NAT + Port forwarding:**
- `VM → Settings → Network → Adapter 1 → Advanced → Port Forwarding`
<img width="1721" height="982" alt="Screenshot 2026-01-21 at 01 48 44" src="https://github.com/user-attachments/assets/510f3328-49f8-4ea4-bede-e204c6515a41" />

### Preduslovi za pokretanje

**Klijentska strana (macOS):**  
- **Python 3:** verzija 3.12.3  
- **Visual Studio Code**: (ili drugi editor po izboru)
- **Aktivno Python virtuelno okruženje**

**Serverska strana (Ubuntu – VirtualBox):**  
- **Python 3:** verzija 3.12.3
- **RabbitMQ server (sa omogućenim TLS-om)**: verzija 3.12.1 sa sa omogućenim TLS-om
- **Uvicorn:** verzija 0.27.1

**Instalacija i podešavanje projekta**
1. **Kreirati direktorijum projekta:**
      * projektovanje-i-implementacija-sigurnog-softvera
2. **Kreirati Python virtuelno okruženje:***
      * python3 -m venv venv
3. **Aktivirati virtuelno okruženje:**
      * source venv/bin/activate
4. **Instalirati neophodne Python biblioteke na serverskoj strani:**
      * FastAPI
      * Uvicorn
5. **Instalirati neophodne Python biblioteke na klijentskoj strani:**
      * cryptography
      * requests
      * pika

**Podešavanje RabbitMQ servera (TLS)**
1. **Kreirati direktorijum za sertifikate:**
      - rabbitmq-certs
2. **Generisati CA sertifikat i kopirati ga na klijentskoj strani:**
      - ca.pem
3. **Generisati serverski privatni ključ:**
      - server.key
4. **Generisati serverski sertifikat potpisan od strane CA:**
      - server.pem
5. **Kreiranje RabbitMQ korisnika**
      - test_client

**Pokretanje serverske aplikacije**
1. cd projektovanje-i-implementacija-sigurnog-softvera
2. source venv/bin/activate
3. uvicorn server:app --host 0.0.0.0 --port 8000 --ssl-keyfile /home/anja/rabbitmq-certs/server.key --ssl-certfile /home/anja/rabbitmq-certs/server.pem

**Pokretanje klijentske aplikacije**
1. cd projektovanje-i-implementacija-sigurnog-softvera
2. source venv/bin/activate
3. python3 client.py

