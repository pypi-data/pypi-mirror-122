from ya_fattura_elettronica_generator import models
from ya_fattura_elettronica_generator.IFatturaElettronicaGenerator import IFatturaElettronicaGenerator
from ya_fattura_elettronica_generator.models import FatturaElettronicaType, FatturaElettronicaHeaderType




class DatiTrasmissioneGeneratorMixIn:

    def __init__(self, trasmittente_codice_fiscale: str, codice_destinatario: str, progressivo_invio:int = None, formato_trasmissione: models.FormatoTrasmissioneType = None):
        self.trasmittente_id_paese = "IT"
        self.trasmittente_codice_fiscale = trasmittente_codice_fiscale
        self.progressivo_invio = progressivo_invio or 1
        self.formato_trasmissione = formato_trasmissione or models.FormatoTrasmissioneType.FPR_12
        self.codice_destinatario = codice_destinatario


class CedentePrestatoreGeneratorMixIn:

    def __init__(self, cedente_id_paese: str, cedente_piva: str, cedente_codice_fiscale: str, cedente_nome: str, cedente_cognome: str, cedente_regime_fiscale: models.RegimeFiscaleType, cedente_indirizzo_sede: str, cedente_indirizzo_numero_civico: str, cedente_indirizzo_cap: str, cedente_indirizzo_comune: str, cedente_indirizzo_provincia: str, cedente_indirizzo_nazione: str):
        self.cedente_id_paese = cedente_id_paese
        self.cedente_piva = cedente_piva
        self.cedente_codice_fiscale = cedente_codice_fiscale
        self.cedente_nome = cedente_nome
        self.cedente_cognome = cedente_cognome
        self.cedente_regime_fiscale = cedente_regime_fiscale
        self.cedente_indirizzo_sede = cedente_indirizzo_sede
        self.cedente_indirizzo_numero_civico = cedente_indirizzo_numero_civico
        self.cedente_indirizzo_cap = cedente_indirizzo_cap
        self.cedente_indirizzo_comune = cedente_indirizzo_comune
        self.cedente_indirizzo_provincia = cedente_indirizzo_provincia
        self.cedente_indirizzo_nazione = cedente_indirizzo_nazione


class CessionarioCommittenteGeneratorMixIn:

    def __init__(self, committente_id_paese: str, committente_piva: str, committente_codice_fiscale: str, committente_nome: str, committente_cognome: str, committente_regime_fiscale: models.RegimeFiscaleType, committente_indirizzo_sede: str, committente_indirizzo_numero_civico: str, committente_indirizzo_cap: str, committente_indirizzo_comune: str, committente_indirizzo_provincia: str, committente_indirizzo_nazione: str):
        self.committente_id_paese = committente_id_paese
        self.committente_piva = committente_piva
        self.committente_codice_fiscale = committente_codice_fiscale
        self.committente_nome = committente_nome
        self.committente_cognome = committente_cognome
        self.committente_regime_fiscale = committente_regime_fiscale
        self.committente_indirizzo_sede = committente_indirizzo_sede
        self.committente_indirizzo_numero_civico = committente_indirizzo_numero_civico
        self.committente_indirizzo_cap = committente_indirizzo_cap
        self.committente_indirizzo_comune = committente_indirizzo_comune
        self.committente_indirizzo_provincia = committente_indirizzo_provincia
        self.committente_indirizzo_nazione = committente_indirizzo_nazione



