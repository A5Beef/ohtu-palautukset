from enum import Enum
from tkinter import ttk, constants, StringVar


class Komento(Enum):
    SUMMA = 1
    EROTUS = 2
    NOLLAUS = 3
    KUMOA = 4


class Komentotehdas:
    def __init__(self, sovelluslogiikka, kayttoliittyma):
        self._sovelluslogiikka = sovelluslogiikka
        self._kayttoliittyma = kayttoliittyma
        self._komennot = {}
        self._alusta_komennot()
    
    def _alusta_komennot(self):
        self._komennot[Komento.SUMMA] = Summa(
            self._sovelluslogiikka, 
            lambda: self._lue_syote()
        )
        self._komennot[Komento.EROTUS] = Erotus(
            self._sovelluslogiikka, 
            lambda: self._lue_syote()
        )
        self._komennot[Komento.NOLLAUS] = Nollaus(self._sovelluslogiikka)
    
    def _lue_syote(self):
        try:
            return int(self._kayttoliittyma._syote_kentta.get())
        except Exception:
            return 0
    
    def hae(self, komento):
        return self._komennot.get(komento)


class Summa:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._edellinen_arvo = 0
    
    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        syote = self._lue_syote()
        self._sovelluslogiikka.plus(syote)
        return self._edellinen_arvo
    
    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)


class Erotus:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._edellinen_arvo = 0
    
    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        syote = self._lue_syote()
        self._sovelluslogiikka.miinus(syote)
        return self._edellinen_arvo
    
    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)


class Nollaus:
    def __init__(self, sovelluslogiikka):
        self._sovelluslogiikka = sovelluslogiikka
        self._edellinen_arvo = 0
    
    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        self._sovelluslogiikka.nollaa()
        return self._edellinen_arvo
    
    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)


class Kayttoliittyma:
    def __init__(self, sovelluslogiikka, root):
        self._sovelluslogiikka = sovelluslogiikka
        self._root = root
        self._komentotehdas = Komentotehdas(sovelluslogiikka, self)
        self._historia = []

    def kaynnista(self):
        self._arvo_var = StringVar()
        self._arvo_var.set(self._sovelluslogiikka.arvo())
        self._syote_kentta = ttk.Entry(master=self._root)

        tulos_teksti = ttk.Label(textvariable=self._arvo_var)

        summa_painike = ttk.Button(
            master=self._root,
            text="Summa",
            command=lambda: self._suorita_komento(Komento.SUMMA)
        )

        erotus_painike = ttk.Button(
            master=self._root,
            text="Erotus",
            command=lambda: self._suorita_komento(Komento.EROTUS)
        )

        self._nollaus_painike = ttk.Button(
            master=self._root,
            text="Nollaus",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.NOLLAUS)
        )

        self._kumoa_painike = ttk.Button(
            master=self._root,
            text="Kumoa",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.KUMOA)
        )

        tulos_teksti.grid(columnspan=4)
        self._syote_kentta.grid(columnspan=4, sticky=(constants.E, constants.W))
        summa_painike.grid(row=2, column=0)
        erotus_painike.grid(row=2, column=1)
        self._nollaus_painike.grid(row=2, column=2)
        self._kumoa_painike.grid(row=2, column=3)

    def _suorita_komento(self, komento):
        if komento == Komento.KUMOA:
            self._kumoa()
        else:
            komento_olio = self._komentotehdas.hae(komento)
            if komento_olio:
                self._historia.append(komento_olio)
                komento_olio.suorita()
        
        self._paivita_napit()
        self._syote_kentta.delete(0, constants.END)
        self._arvo_var.set(self._sovelluslogiikka.arvo())
    
    def _kumoa(self):
        if self._historia:
            viimeisin_komento = self._historia.pop()
            viimeisin_komento.kumoa()
    
    def _paivita_napit(self):
        # Kumoa-painikkeen tila
        if self._historia:
            self._kumoa_painike["state"] = constants.NORMAL
        else:
            self._kumoa_painike["state"] = constants.DISABLED
        
        # Nollaus-painikkeen tila
        if self._sovelluslogiikka.arvo() == 0:
            self._nollaus_painike["state"] = constants.DISABLED
        else:
            self._nollaus_painike["state"] = constants.NORMAL