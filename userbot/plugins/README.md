## Zorunlu İthalat
```python3
None
```
Zorunlu Alma Yok. Çünkü Var, bot ve komut zaten otomatik olarak içe aktarılıyor.

## açıklama 
Zorunlu İçe Aktarmalar artık otomatik olarak içe aktarılıyor.

### formasyon
Şimdi istenen senaryonun oluşumunu göstermek için kısa bir senaryo göstereceğim..
```python3
@command(pattern="^.alive", outgoing=True)
async def hello_world(event):
    if event.fwd_from:
        return
    await event.edit("**Merhaba Dünya**\n\nAşağıdakiler beni de kontrol ediyor.!\n" + Var.SUDO_USERS)
```
