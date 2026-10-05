def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        f = open(file_path, 'r')   #Apro e leggo il file
        f.readline()    #leggo la prima riga per saltarla
        album = {}

        for riga in f:
            riga = riga.strip()  # Rimuovo \n e spazi a inizio - fine
            dati = riga.split(',')

            codice = dati[0]
            titolo = dati[1]
            autore = dati[2]
            mese = int(dati[3])
            anno = int(dati[4])

            foto = {
                'codice': codice,
                'titolo': titolo,
                'autore': autore,
                'mese': mese,
                'anno': anno
            }

            # Se l'anno non esiste ancora nell'album, creo la lista vuota
            if anno not in album:
                album[anno] = []

            # Aggiungo SEMPRE la foto alla lista dell'anno
            album[anno].append(foto)

        f.close()    #chiudo il file
        return album

    except FileNotFoundError:
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # Controllo mese valido
    if mese < 1 or mese > 12:
        return None

    # Controllo se il codice esiste già nell'album
    for a in album:
        for foto in album[a]:
            if foto['codice'] == codice:
                return None  # Codice già presente!

    # Creo l'anno se non esiste e lo aggiungo all'album
    if anno not in album:
        album[anno] = []

    nuova_foto = {
        'codice': codice,
        'titolo': titolo,
        'autore': autore,
        'mese': mese,
        'anno': anno
    }

    # Scrittura sul file in modalità append ('a')
    try:
        f = open(file_path, 'a')
        riga = f"{codice},{titolo},{autore},{mese},{anno}\n"
        f.write(riga)
        f.close()

    except FileNotFoundError:
        return None

    # Aggiornamento in memoria e return
    album[anno].append(nuova_foto)
    return nuova_foto


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for anno in album:
        for foto in album[anno]:
            if foto['codice'] == codice:
                # Ottengo la stringa con le informazioni della foto
                return f"{foto['codice']}, {foto['titolo']}, {foto['autore']}, {foto['mese']}, {foto['anno']}"

        # Se il codice non viene trovato
    return None

def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # Se l'anno non è mai comparso nell'album, restituisce None
    if anno not in album:
        return None

    # Raccolgo tutti i titoli delle foto di quell'anno
    titoli = []
    for foto in album[anno]:
        titoli.append(foto['titolo'])

    # Ordino i titoli in ordine alfabetico
    titoli_ordinati = sorted(titoli)
    return titoli_ordinati

def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
