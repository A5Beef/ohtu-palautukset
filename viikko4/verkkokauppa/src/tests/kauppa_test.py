import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from kirjanpito import Kirjanpito
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.varasto_mock = Mock()
        self.kirjanpito_mock = Mock()

        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42


        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 5
            if tuote_id == 3:
                return 0

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "juusto", 3)
            if tuote_id == 3:
                return Tuote(3, "kanamuna", 4)
            
        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)


    def test_valmiinatullu(self):
        # pohjatesti
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    # tehtävä 3 testi
    def test_ostotesti(self):
        
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("perttu", "1337")

        self.pankki_mock.tilisiirto.assert_called_with("perttu", ANY, "1337", ANY, 5)

    def test_kaksi_eri_tuotetta(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("Karvinen", "1454603")

        self.pankki_mock.tilisiirto.assert_called_with("Karvinen", ANY, "1454603", ANY, 8)

    def test_kaksi_samaa_tuotetta(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("Matti", "99999")

        self.pankki_mock.tilisiirto.assert_called_with("Matti", ANY, "99999", ANY, 6)

    def test_toinen_tuote_loppu(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3)

        self.kauppa.tilimaksu("Teppo", "88888")
        self.pankki_mock.tilisiirto.assert_called_with("Teppo", ANY, "88888", ANY, 5)


    # Tehtävä 4 testi
    def test_aloita_asiointi_nollaa_edellisen(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("Aku", "77777")

        self.pankki_mock.tilisiirto.assert_called_with("Aku", ANY, "77777", ANY, 3)

    def test_kauppa_pyytaa_uuden_viitenumeron(self):
        self.viitegeneraattori_mock.uusi.side_effect = [42, 43]

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("Iines", "66666")

        self.pankki_mock.tilisiirto.assert_called_with("Iines", 42, "66666", ANY, 5)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("Kalle", "55555")
        self.pankki_mock.tilisiirto.assert_called_with("Kalle", 43, "55555", ANY, 3)


    def test_coverage_sataan(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.poista_korista(1)

        self.kauppa.tilimaksu("Iines", "66666")

        self.pankki_mock.tilisiirto.assert_called_with("Iines", ANY, "66666", ANY, 3)
    
    def test_kirjanpito_tapahtumat_kun_ostetaan(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("Mauri", "44444")

        self.varasto_mock.ota_varastosta.assert_any_call(Tuote(1, "maito", 5))
        self.varasto_mock.ota_varastosta.assert_any_call(Tuote(2, "juusto", 3)) 