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
