import random
import datetime

def tallenna_peli_lkm(pelit_lkm):
    nykyinen_pelit_lkm, nykyinen_teksti = lue_peli_lkm()
    yhteensa_pelit_lkm = nykyinen_pelit_lkm + pelit_lkm

    with open("peli_lkm.txt", "w") as tiedosto:
        tiedosto.write(f"Peliä on pelattu yhteensä {str(yhteensa_pelit_lkm)} kertaa.\n")
        tiedosto.write(f"Viimeisin päivitys: {datetime.datetime.now()}")
    print("Pelilukumäärä tallennettu onnistuneesti.")

def lue_peli_lkm():
    try:
        with open("peli_lkm.txt", "r") as tiedosto:
            sisalto = tiedosto.read()
            sanat = sisalto.split()
            peli_lkm_indeksi = sanat.index('kertaa.') - 1
            peli_lkm = int(sanat[peli_lkm_indeksi])
            return peli_lkm, sisalto
    except (FileNotFoundError, ValueError, IndexError):
        return 0, ""
        

def main():
    print("Tervetuloa pelaamaan bussikuskia!\nTässä pelissä ei ole voittajia, vaan arvauspelissä oikein arvaamalla välttää juomisen.\nAloitamme lisäämällä pelaajat.\n")
    pelaa = 1
    pelit = 0
    print(lue_peli_lkm())
    while pelaa != 0:
        try:
            pelaajat = lisaaPelaajat()
            korttipakka = luoKorttipakka()
            for peli in range(1, pelaa + 1):
                aloitaPeli(pelaajat, korttipakka)
                pelit += 1
            pelitilanne(pelaajat)
            try:
                tallenna_peli_lkm(pelit)
            except Exception as e:
                print(f"Virhe tallenna_peli_lkm:ssa: {e}")

            if pelaa != 0:
                while True:
                    syote = input("\nJatketaanko peliä?\n1 Jatka\n0 Lopeta")
                    if syote in ["0", "1"]:
                        pelaa = int(syote)
                        break
                    else:
                        print("Syötteesi ei ollut kelvollinen. Yritä uudestaan.")
                        
                input("Paina enteriä jatkaaksesi")
    
        except ValueError:
            print("Virheellinen syöte! Valitse 1 tai 0.")
        
    
    
    print("Kiitos pelistä!")

def lisaaPelaajat():
    pelaajat = {}
    lisaaUusi = input("Haluatko lisätä uuden pelaajan? (Y/N)").lower()

    while True:
        if lisaaUusi == "y":
            nimi = input("Anna nimesi:").upper()
            # Tarkista, ettei pelaajaa ole jo lisätty
            try:
                if nimi in pelaajat:
                    raise ValueError(f"Pelaaja {nimi} on jo lisätty.")
                elif nimi == "":
                    print("Et voi olla nimetön.")
                    continue
                pelaajat[nimi] = {"kortit": [], "sakot": 0}
                print(f"Pelaaja {nimi} lisätty onnistuneesti.")
                lisaaUusi = input("Haluatko lisätä uuden pelaajan? (Y/N)").lower()
            except ValueError as ve:
                print(ve)
        elif lisaaUusi == "n":
            break
        else:
            print("Y = kyllä, N = ei")
            lisaaUusi = input("Haluatko lisätä uuden pelaajan? (Y/N)").lower()

    return pelaajat
    

def luoKorttipakka():
    korttipakka = []
    numerot = range(1, 14)
    maat = ("pata", "risti", "ruutu", "hertta")

    for maa in maat:
        for numero in numerot:
            kortti = (maa, numero)
            korttipakka.append(kortti)

    # Sekoita korttipakka
    random.shuffle(korttipakka)
    return korttipakka

def pelitilanne(pelaajat):
    print("PELITILANNE\n*****")
    for pelaaja, tiedot in pelaajat.items():
        print(f"{pelaaja}:")
        print(f"  Kortit: {', '.join(map(str, tiedot['kortit']))}")
        if tiedot['sakot'] == 6:
            print("Sakkoa joka kerta, haepa lisää juotavaa.")
        elif tiedot['sakot'] == 0:
            print("Ei yhtään sakkoa, hyvin arvailtu!")
        else:
            print(f"  Sakot: {tiedot['sakot']}")
        print("")
    print("*****")

def vertaa_kortteja(edellinen_kortti, uusi_kortti):
    if edellinen_kortti[1] < uusi_kortti[1]:
        return "1"
    elif edellinen_kortti[1] > uusi_kortti[1]:
        return "2"
    else:
        return "3"
    
def seuraava_kierros():
#käytetään vain siihen että voi hieman vaikuttaa pelin tulosteiden tahtiin. muuten on vaikea pysyä mukana imo.
    while True:
        jatko = input("Paina enteriä jatkaaksesi\n")
        if jatko == "":
            return
        else:
            print("Älä kirjoita mitään")

def ensimmainen_kierros(pelaajat, korttipakka):
    if not pelaajat or not korttipakka:
        return "Ei pelaajia tai korttipakkaa"
    for pelaaja, tiedot in pelaajat.items():
        print(f"{pelaaja}, 1. kierros:")
        while True:
            arvaus = input("Arvaa kortin väri (musta/punainen): ").lower()
            if arvaus in ["musta", "punainen"]:
                break
            else:
                print("Virheellinen syöte, valitse musta tai punainen.")

        oikea_vari = "musta" if korttipakka[0][0] in ["pata", "risti"] else "punainen"
        
        jaettu_kortti = korttipakka.pop(0)
        tiedot["kortit"].append(jaettu_kortti)

        if arvaus == oikea_vari:
            print(f"\nOnneksi olkoon! Arvasit oikein, kortti on: {jaettu_kortti}")
        else:
            print(f"\nArvaus meni väärin! {jaettu_kortti} otas hörppy!")
            tiedot["sakot"] += 1
    return "1. kierros päättynyt\n"
    


def toinen_kierros(pelaajat, korttipakka):
    if not pelaajat or not korttipakka:
        return "Ei pelaajia tai korttipakkaa"
    for pelaaja, tiedot in pelaajat.items():
        print(f"{pelaaja}, toinen kierros ja tuplasakot:")
        # Tarkista, että pelaajalla on vähintään yksi kortti ennen vertailua
        if len(tiedot["kortit"]) < 1:
            print(f"Pelaajalla {pelaaja} ei ole vielä yhtään korttia.")
            return "Seuraava pelaaja"
        
        while True:
            arvaus = input(f"Arvaa onko seuraava kortti:\n1 = suurempi\n2 = pienempi\n3 = samaa numeroa kuin {tiedot['kortit']}: ")
            if arvaus in ["1", "2", "3"]:
                break
            else:
                print("Yritä uudestaan.")

        edellinen_kortti = tiedot["kortit"][-1]
        jaettu_kortti = korttipakka.pop(0)
        tiedot["kortit"].append(jaettu_kortti)
        
        
        uusi_kortti = tiedot["kortit"][-1]
        vertailu = vertaa_kortteja(edellinen_kortti, uusi_kortti)

        if arvaus == vertailu:
            print(f"\nOnneksi olkoon! Arvasit oikein, kortti on: {jaettu_kortti}")
        else:
            print(f"\nArvaus meni väärin! {jaettu_kortti} pari hörppyä!")
            tiedot["sakot"] += 2
    return "2. kierros on päättynyt\n"
    

def kolmas_kierros(pelaajat, korttipakka):
    for pelaaja, tiedot in pelaajat.items():
        print(f"{pelaaja}, kolmas kierros tietää triplasakkoja vääristä arvauksista.")
        while True:
            arvaus = input("Arvaa seuraavan kortin maa:\n1 = pata\n2 = hertta\n3 = ruutu\n4 = risti: ").lower()
            if arvaus in ["1", "2", "3", "4"]:
                break
            else:
                print("Vaihtoehtoina olivat 1, 2, 3 ja 4. Et valinnut niistä.")
                
        jaettu_kortti = korttipakka.pop(0)
        tiedot["kortit"].append(jaettu_kortti)
        maat = ["","pata","hertta","ruutu","risti"]
        

        oikea_maa = jaettu_kortti[0]
        if maat[int(arvaus)] == oikea_maa:
            print(f"\nOnneksi olkoon! Arvasit oikein, kortti on: {jaettu_kortti}")
        else:
            print(f"\nArvaus meni väärin! {jaettu_kortti} kolme kunnon kulausta!")
            tiedot["sakot"] += 3
    return "3. kierros on päättynyt\n"
    

def neljas_kierros(pelaajat, korttipakka):
    print("Pelaaja, jonka korttien summa on suurin, saa 4 bonus-hörppyjä.")
    

    suurin = 0
    for pelaaja, tiedot in pelaajat.items():
        korttien_summa = sum([kortti[1] for kortti in tiedot["kortit"]])
        print(f"Pelaajan {pelaaja} korttien summa: {korttien_summa}")
        if korttien_summa > suurin:
            suurin = korttien_summa
    print(suurin, " oli suurin määrä, kuittaahan bonuksesi")
    return "4. kierros on päättynyt\n"
    
    
def aloitaPeli(pelaajat, korttipakka):
    kierrokset = {0:ensimmainen_kierros,
                    1:toinen_kierros,
                    2:kolmas_kierros,
                    3:neljas_kierros}
    kierros = 0
    if not pelaajat:
        print("Ei ole pelaajia!")
        return
    
    while (kierros < 4):
        seuraava_kierros()
        print(f"KIERROS {kierros + 1}")
        print(kierrokset[kierros](pelaajat, korttipakka))
        kierros += 1
    seuraava_kierros()
    
if __name__ == "__main__":
    main()
