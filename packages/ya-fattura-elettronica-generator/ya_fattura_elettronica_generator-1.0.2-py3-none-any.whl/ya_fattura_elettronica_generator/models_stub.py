#!/usr/bin/env python

#
# Generated Tue Oct  5 14:06:37 2021 by generateDS.py version 2.40.3.
# Python 3.8.6 (tags/v3.8.6:db45529, Sep 23 2020, 15:52:53) [MSC v.1927 64 bit (AMD64)]
#
# Command line options:
#   ('-o', 'models.py')
#   ('-s', 'models_stub.py')
#
# Command line arguments:
#   ya_fattura_elettronica_generator\package_data\Schema_del_file_xml_FatturaPA_versione_1.2.xsd
#
# Command line:
#   .\venv\Scripts\generateDS.py -o "models.py" -s "models_stub.py" ya_fattura_elettronica_generator\package_data\Schema_del_file_xml_FatturaPA_versione_1.2.xsd
#
# Current working directory (os.getcwd()):
#   pythonProject
#

import os
import sys
from lxml import etree as etree_


from ya_fattura_elettronica_generator import models

def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

def parsexmlstring_(instring, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    element = etree_.fromstring(instring, parser=parser, **kwargs)
    return element

#
# Globals
#

ExternalEncoding = ''
SaveElementTreeNode = True

#
# Data representation classes
#


class FatturaElettronicaTypeSub(models.FatturaElettronicaType):
    def __init__(self, versione=None, FatturaElettronicaHeader=None, FatturaElettronicaBody=None, Signature=None, **kwargs_):
        super(FatturaElettronicaTypeSub, self).__init__(versione, FatturaElettronicaHeader, FatturaElettronicaBody, Signature,  **kwargs_)
models.FatturaElettronicaType.subclass = FatturaElettronicaTypeSub
# end class FatturaElettronicaTypeSub


class FatturaElettronicaHeaderTypeSub(models.FatturaElettronicaHeaderType):
    def __init__(self, DatiTrasmissione=None, CedentePrestatore=None, RappresentanteFiscale=None, CessionarioCommittente=None, TerzoIntermediarioOSoggettoEmittente=None, SoggettoEmittente=None, **kwargs_):
        super(FatturaElettronicaHeaderTypeSub, self).__init__(DatiTrasmissione, CedentePrestatore, RappresentanteFiscale, CessionarioCommittente, TerzoIntermediarioOSoggettoEmittente, SoggettoEmittente,  **kwargs_)
models.FatturaElettronicaHeaderType.subclass = FatturaElettronicaHeaderTypeSub
# end class FatturaElettronicaHeaderTypeSub


class FatturaElettronicaBodyTypeSub(models.FatturaElettronicaBodyType):
    def __init__(self, DatiGenerali=None, DatiBeniServizi=None, DatiVeicoli=None, DatiPagamento=None, Allegati=None, **kwargs_):
        super(FatturaElettronicaBodyTypeSub, self).__init__(DatiGenerali, DatiBeniServizi, DatiVeicoli, DatiPagamento, Allegati,  **kwargs_)
models.FatturaElettronicaBodyType.subclass = FatturaElettronicaBodyTypeSub
# end class FatturaElettronicaBodyTypeSub


class DatiTrasmissioneTypeSub(models.DatiTrasmissioneType):
    def __init__(self, IdTrasmittente=None, ProgressivoInvio=None, FormatoTrasmissione=None, CodiceDestinatario=None, ContattiTrasmittente=None, PECDestinatario=None, **kwargs_):
        super(DatiTrasmissioneTypeSub, self).__init__(IdTrasmittente, ProgressivoInvio, FormatoTrasmissione, CodiceDestinatario, ContattiTrasmittente, PECDestinatario,  **kwargs_)
models.DatiTrasmissioneType.subclass = DatiTrasmissioneTypeSub
# end class DatiTrasmissioneTypeSub


class IdFiscaleTypeSub(models.IdFiscaleType):
    def __init__(self, IdPaese=None, IdCodice=None, **kwargs_):
        super(IdFiscaleTypeSub, self).__init__(IdPaese, IdCodice,  **kwargs_)
models.IdFiscaleType.subclass = IdFiscaleTypeSub
# end class IdFiscaleTypeSub


class ContattiTrasmittenteTypeSub(models.ContattiTrasmittenteType):
    def __init__(self, Telefono=None, Email=None, **kwargs_):
        super(ContattiTrasmittenteTypeSub, self).__init__(Telefono, Email,  **kwargs_)
models.ContattiTrasmittenteType.subclass = ContattiTrasmittenteTypeSub
# end class ContattiTrasmittenteTypeSub


class DatiGeneraliTypeSub(models.DatiGeneraliType):
    def __init__(self, DatiGeneraliDocumento=None, DatiOrdineAcquisto=None, DatiContratto=None, DatiConvenzione=None, DatiRicezione=None, DatiFattureCollegate=None, DatiSAL=None, DatiDDT=None, DatiTrasporto=None, FatturaPrincipale=None, **kwargs_):
        super(DatiGeneraliTypeSub, self).__init__(DatiGeneraliDocumento, DatiOrdineAcquisto, DatiContratto, DatiConvenzione, DatiRicezione, DatiFattureCollegate, DatiSAL, DatiDDT, DatiTrasporto, FatturaPrincipale,  **kwargs_)
models.DatiGeneraliType.subclass = DatiGeneraliTypeSub
# end class DatiGeneraliTypeSub


class DatiGeneraliDocumentoTypeSub(models.DatiGeneraliDocumentoType):
    def __init__(self, TipoDocumento=None, Divisa=None, Data=None, Numero=None, DatiRitenuta=None, DatiBollo=None, DatiCassaPrevidenziale=None, ScontoMaggiorazione=None, ImportoTotaleDocumento=None, Arrotondamento=None, Causale=None, Art73=None, **kwargs_):
        super(DatiGeneraliDocumentoTypeSub, self).__init__(TipoDocumento, Divisa, Data, Numero, DatiRitenuta, DatiBollo, DatiCassaPrevidenziale, ScontoMaggiorazione, ImportoTotaleDocumento, Arrotondamento, Causale, Art73,  **kwargs_)
models.DatiGeneraliDocumentoType.subclass = DatiGeneraliDocumentoTypeSub
# end class DatiGeneraliDocumentoTypeSub


class DatiRitenutaTypeSub(models.DatiRitenutaType):
    def __init__(self, TipoRitenuta=None, ImportoRitenuta=None, AliquotaRitenuta=None, CausalePagamento=None, **kwargs_):
        super(DatiRitenutaTypeSub, self).__init__(TipoRitenuta, ImportoRitenuta, AliquotaRitenuta, CausalePagamento,  **kwargs_)
models.DatiRitenutaType.subclass = DatiRitenutaTypeSub
# end class DatiRitenutaTypeSub


class DatiBolloTypeSub(models.DatiBolloType):
    def __init__(self, BolloVirtuale=None, ImportoBollo=None, **kwargs_):
        super(DatiBolloTypeSub, self).__init__(BolloVirtuale, ImportoBollo,  **kwargs_)
models.DatiBolloType.subclass = DatiBolloTypeSub
# end class DatiBolloTypeSub


class DatiCassaPrevidenzialeTypeSub(models.DatiCassaPrevidenzialeType):
    def __init__(self, TipoCassa=None, AlCassa=None, ImportoContributoCassa=None, ImponibileCassa=None, AliquotaIVA=None, Ritenuta=None, Natura=None, RiferimentoAmministrazione=None, **kwargs_):
        super(DatiCassaPrevidenzialeTypeSub, self).__init__(TipoCassa, AlCassa, ImportoContributoCassa, ImponibileCassa, AliquotaIVA, Ritenuta, Natura, RiferimentoAmministrazione,  **kwargs_)
models.DatiCassaPrevidenzialeType.subclass = DatiCassaPrevidenzialeTypeSub
# end class DatiCassaPrevidenzialeTypeSub


class ScontoMaggiorazioneTypeSub(models.ScontoMaggiorazioneType):
    def __init__(self, Tipo=None, Percentuale=None, Importo=None, **kwargs_):
        super(ScontoMaggiorazioneTypeSub, self).__init__(Tipo, Percentuale, Importo,  **kwargs_)
models.ScontoMaggiorazioneType.subclass = ScontoMaggiorazioneTypeSub
# end class ScontoMaggiorazioneTypeSub


class DatiSALTypeSub(models.DatiSALType):
    def __init__(self, RiferimentoFase=None, **kwargs_):
        super(DatiSALTypeSub, self).__init__(RiferimentoFase,  **kwargs_)
models.DatiSALType.subclass = DatiSALTypeSub
# end class DatiSALTypeSub


class DatiDocumentiCorrelatiTypeSub(models.DatiDocumentiCorrelatiType):
    def __init__(self, RiferimentoNumeroLinea=None, IdDocumento=None, Data=None, NumItem=None, CodiceCommessaConvenzione=None, CodiceCUP=None, CodiceCIG=None, **kwargs_):
        super(DatiDocumentiCorrelatiTypeSub, self).__init__(RiferimentoNumeroLinea, IdDocumento, Data, NumItem, CodiceCommessaConvenzione, CodiceCUP, CodiceCIG,  **kwargs_)
models.DatiDocumentiCorrelatiType.subclass = DatiDocumentiCorrelatiTypeSub
# end class DatiDocumentiCorrelatiTypeSub


class DatiDDTTypeSub(models.DatiDDTType):
    def __init__(self, NumeroDDT=None, DataDDT=None, RiferimentoNumeroLinea=None, **kwargs_):
        super(DatiDDTTypeSub, self).__init__(NumeroDDT, DataDDT, RiferimentoNumeroLinea,  **kwargs_)
models.DatiDDTType.subclass = DatiDDTTypeSub
# end class DatiDDTTypeSub


class DatiTrasportoTypeSub(models.DatiTrasportoType):
    def __init__(self, DatiAnagraficiVettore=None, MezzoTrasporto=None, CausaleTrasporto=None, NumeroColli=None, Descrizione=None, UnitaMisuraPeso=None, PesoLordo=None, PesoNetto=None, DataOraRitiro=None, DataInizioTrasporto=None, TipoResa=None, IndirizzoResa=None, DataOraConsegna=None, **kwargs_):
        super(DatiTrasportoTypeSub, self).__init__(DatiAnagraficiVettore, MezzoTrasporto, CausaleTrasporto, NumeroColli, Descrizione, UnitaMisuraPeso, PesoLordo, PesoNetto, DataOraRitiro, DataInizioTrasporto, TipoResa, IndirizzoResa, DataOraConsegna,  **kwargs_)
models.DatiTrasportoType.subclass = DatiTrasportoTypeSub
# end class DatiTrasportoTypeSub


class IndirizzoTypeSub(models.IndirizzoType):
    def __init__(self, Indirizzo=None, NumeroCivico=None, CAP=None, Comune=None, Provincia=None, Nazione='IT', **kwargs_):
        super(IndirizzoTypeSub, self).__init__(Indirizzo, NumeroCivico, CAP, Comune, Provincia, Nazione,  **kwargs_)
models.IndirizzoType.subclass = IndirizzoTypeSub
# end class IndirizzoTypeSub


class FatturaPrincipaleTypeSub(models.FatturaPrincipaleType):
    def __init__(self, NumeroFatturaPrincipale=None, DataFatturaPrincipale=None, **kwargs_):
        super(FatturaPrincipaleTypeSub, self).__init__(NumeroFatturaPrincipale, DataFatturaPrincipale,  **kwargs_)
models.FatturaPrincipaleType.subclass = FatturaPrincipaleTypeSub
# end class FatturaPrincipaleTypeSub


class CedentePrestatoreTypeSub(models.CedentePrestatoreType):
    def __init__(self, DatiAnagrafici=None, Sede=None, StabileOrganizzazione=None, IscrizioneREA=None, Contatti=None, RiferimentoAmministrazione=None, **kwargs_):
        super(CedentePrestatoreTypeSub, self).__init__(DatiAnagrafici, Sede, StabileOrganizzazione, IscrizioneREA, Contatti, RiferimentoAmministrazione,  **kwargs_)
models.CedentePrestatoreType.subclass = CedentePrestatoreTypeSub
# end class CedentePrestatoreTypeSub


class DatiAnagraficiCedenteTypeSub(models.DatiAnagraficiCedenteType):
    def __init__(self, IdFiscaleIVA=None, CodiceFiscale=None, Anagrafica=None, AlboProfessionale=None, ProvinciaAlbo=None, NumeroIscrizioneAlbo=None, DataIscrizioneAlbo=None, RegimeFiscale=None, **kwargs_):
        super(DatiAnagraficiCedenteTypeSub, self).__init__(IdFiscaleIVA, CodiceFiscale, Anagrafica, AlboProfessionale, ProvinciaAlbo, NumeroIscrizioneAlbo, DataIscrizioneAlbo, RegimeFiscale,  **kwargs_)
models.DatiAnagraficiCedenteType.subclass = DatiAnagraficiCedenteTypeSub
# end class DatiAnagraficiCedenteTypeSub


class AnagraficaTypeSub(models.AnagraficaType):
    def __init__(self, Denominazione=None, Nome=None, Cognome=None, Titolo=None, CodEORI=None, **kwargs_):
        super(AnagraficaTypeSub, self).__init__(Denominazione, Nome, Cognome, Titolo, CodEORI,  **kwargs_)
models.AnagraficaType.subclass = AnagraficaTypeSub
# end class AnagraficaTypeSub


class DatiAnagraficiVettoreTypeSub(models.DatiAnagraficiVettoreType):
    def __init__(self, IdFiscaleIVA=None, CodiceFiscale=None, Anagrafica=None, NumeroLicenzaGuida=None, **kwargs_):
        super(DatiAnagraficiVettoreTypeSub, self).__init__(IdFiscaleIVA, CodiceFiscale, Anagrafica, NumeroLicenzaGuida,  **kwargs_)
models.DatiAnagraficiVettoreType.subclass = DatiAnagraficiVettoreTypeSub
# end class DatiAnagraficiVettoreTypeSub


class IscrizioneREATypeSub(models.IscrizioneREAType):
    def __init__(self, Ufficio=None, NumeroREA=None, CapitaleSociale=None, SocioUnico=None, StatoLiquidazione=None, **kwargs_):
        super(IscrizioneREATypeSub, self).__init__(Ufficio, NumeroREA, CapitaleSociale, SocioUnico, StatoLiquidazione,  **kwargs_)
models.IscrizioneREAType.subclass = IscrizioneREATypeSub
# end class IscrizioneREATypeSub


class ContattiTypeSub(models.ContattiType):
    def __init__(self, Telefono=None, Fax=None, Email=None, **kwargs_):
        super(ContattiTypeSub, self).__init__(Telefono, Fax, Email,  **kwargs_)
models.ContattiType.subclass = ContattiTypeSub
# end class ContattiTypeSub


class RappresentanteFiscaleTypeSub(models.RappresentanteFiscaleType):
    def __init__(self, DatiAnagrafici=None, **kwargs_):
        super(RappresentanteFiscaleTypeSub, self).__init__(DatiAnagrafici,  **kwargs_)
models.RappresentanteFiscaleType.subclass = RappresentanteFiscaleTypeSub
# end class RappresentanteFiscaleTypeSub


class DatiAnagraficiRappresentanteTypeSub(models.DatiAnagraficiRappresentanteType):
    def __init__(self, IdFiscaleIVA=None, CodiceFiscale=None, Anagrafica=None, **kwargs_):
        super(DatiAnagraficiRappresentanteTypeSub, self).__init__(IdFiscaleIVA, CodiceFiscale, Anagrafica,  **kwargs_)
models.DatiAnagraficiRappresentanteType.subclass = DatiAnagraficiRappresentanteTypeSub
# end class DatiAnagraficiRappresentanteTypeSub


class CessionarioCommittenteTypeSub(models.CessionarioCommittenteType):
    def __init__(self, DatiAnagrafici=None, Sede=None, StabileOrganizzazione=None, RappresentanteFiscale=None, **kwargs_):
        super(CessionarioCommittenteTypeSub, self).__init__(DatiAnagrafici, Sede, StabileOrganizzazione, RappresentanteFiscale,  **kwargs_)
models.CessionarioCommittenteType.subclass = CessionarioCommittenteTypeSub
# end class CessionarioCommittenteTypeSub


class RappresentanteFiscaleCessionarioTypeSub(models.RappresentanteFiscaleCessionarioType):
    def __init__(self, IdFiscaleIVA=None, Denominazione=None, Nome=None, Cognome=None, **kwargs_):
        super(RappresentanteFiscaleCessionarioTypeSub, self).__init__(IdFiscaleIVA, Denominazione, Nome, Cognome,  **kwargs_)
models.RappresentanteFiscaleCessionarioType.subclass = RappresentanteFiscaleCessionarioTypeSub
# end class RappresentanteFiscaleCessionarioTypeSub


class DatiAnagraficiCessionarioTypeSub(models.DatiAnagraficiCessionarioType):
    def __init__(self, IdFiscaleIVA=None, CodiceFiscale=None, Anagrafica=None, **kwargs_):
        super(DatiAnagraficiCessionarioTypeSub, self).__init__(IdFiscaleIVA, CodiceFiscale, Anagrafica,  **kwargs_)
models.DatiAnagraficiCessionarioType.subclass = DatiAnagraficiCessionarioTypeSub
# end class DatiAnagraficiCessionarioTypeSub


class DatiBeniServiziTypeSub(models.DatiBeniServiziType):
    def __init__(self, DettaglioLinee=None, DatiRiepilogo=None, **kwargs_):
        super(DatiBeniServiziTypeSub, self).__init__(DettaglioLinee, DatiRiepilogo,  **kwargs_)
models.DatiBeniServiziType.subclass = DatiBeniServiziTypeSub
# end class DatiBeniServiziTypeSub


class DatiVeicoliTypeSub(models.DatiVeicoliType):
    def __init__(self, Data=None, TotalePercorso=None, **kwargs_):
        super(DatiVeicoliTypeSub, self).__init__(Data, TotalePercorso,  **kwargs_)
models.DatiVeicoliType.subclass = DatiVeicoliTypeSub
# end class DatiVeicoliTypeSub


class DatiPagamentoTypeSub(models.DatiPagamentoType):
    def __init__(self, CondizioniPagamento=None, DettaglioPagamento=None, **kwargs_):
        super(DatiPagamentoTypeSub, self).__init__(CondizioniPagamento, DettaglioPagamento,  **kwargs_)
models.DatiPagamentoType.subclass = DatiPagamentoTypeSub
# end class DatiPagamentoTypeSub


class DettaglioPagamentoTypeSub(models.DettaglioPagamentoType):
    def __init__(self, Beneficiario=None, ModalitaPagamento=None, DataRiferimentoTerminiPagamento=None, GiorniTerminiPagamento=None, DataScadenzaPagamento=None, ImportoPagamento=None, CodUfficioPostale=None, CognomeQuietanzante=None, NomeQuietanzante=None, CFQuietanzante=None, TitoloQuietanzante=None, IstitutoFinanziario=None, IBAN=None, ABI=None, CAB=None, BIC=None, ScontoPagamentoAnticipato=None, DataLimitePagamentoAnticipato=None, PenalitaPagamentiRitardati=None, DataDecorrenzaPenale=None, CodicePagamento=None, **kwargs_):
        super(DettaglioPagamentoTypeSub, self).__init__(Beneficiario, ModalitaPagamento, DataRiferimentoTerminiPagamento, GiorniTerminiPagamento, DataScadenzaPagamento, ImportoPagamento, CodUfficioPostale, CognomeQuietanzante, NomeQuietanzante, CFQuietanzante, TitoloQuietanzante, IstitutoFinanziario, IBAN, ABI, CAB, BIC, ScontoPagamentoAnticipato, DataLimitePagamentoAnticipato, PenalitaPagamentiRitardati, DataDecorrenzaPenale, CodicePagamento,  **kwargs_)
models.DettaglioPagamentoType.subclass = DettaglioPagamentoTypeSub
# end class DettaglioPagamentoTypeSub


class TerzoIntermediarioSoggettoEmittenteTypeSub(models.TerzoIntermediarioSoggettoEmittenteType):
    def __init__(self, DatiAnagrafici=None, **kwargs_):
        super(TerzoIntermediarioSoggettoEmittenteTypeSub, self).__init__(DatiAnagrafici,  **kwargs_)
models.TerzoIntermediarioSoggettoEmittenteType.subclass = TerzoIntermediarioSoggettoEmittenteTypeSub
# end class TerzoIntermediarioSoggettoEmittenteTypeSub


class DatiAnagraficiTerzoIntermediarioTypeSub(models.DatiAnagraficiTerzoIntermediarioType):
    def __init__(self, IdFiscaleIVA=None, CodiceFiscale=None, Anagrafica=None, **kwargs_):
        super(DatiAnagraficiTerzoIntermediarioTypeSub, self).__init__(IdFiscaleIVA, CodiceFiscale, Anagrafica,  **kwargs_)
models.DatiAnagraficiTerzoIntermediarioType.subclass = DatiAnagraficiTerzoIntermediarioTypeSub
# end class DatiAnagraficiTerzoIntermediarioTypeSub


class AllegatiTypeSub(models.AllegatiType):
    def __init__(self, NomeAttachment=None, AlgoritmoCompressione=None, FormatoAttachment=None, DescrizioneAttachment=None, Attachment=None, **kwargs_):
        super(AllegatiTypeSub, self).__init__(NomeAttachment, AlgoritmoCompressione, FormatoAttachment, DescrizioneAttachment, Attachment,  **kwargs_)
models.AllegatiType.subclass = AllegatiTypeSub
# end class AllegatiTypeSub


class DettaglioLineeTypeSub(models.DettaglioLineeType):
    def __init__(self, NumeroLinea=None, TipoCessionePrestazione=None, CodiceArticolo=None, Descrizione=None, Quantita=None, UnitaMisura=None, DataInizioPeriodo=None, DataFinePeriodo=None, PrezzoUnitario=None, ScontoMaggiorazione=None, PrezzoTotale=None, AliquotaIVA=None, Ritenuta=None, Natura=None, RiferimentoAmministrazione=None, AltriDatiGestionali=None, **kwargs_):
        super(DettaglioLineeTypeSub, self).__init__(NumeroLinea, TipoCessionePrestazione, CodiceArticolo, Descrizione, Quantita, UnitaMisura, DataInizioPeriodo, DataFinePeriodo, PrezzoUnitario, ScontoMaggiorazione, PrezzoTotale, AliquotaIVA, Ritenuta, Natura, RiferimentoAmministrazione, AltriDatiGestionali,  **kwargs_)
models.DettaglioLineeType.subclass = DettaglioLineeTypeSub
# end class DettaglioLineeTypeSub


class CodiceArticoloTypeSub(models.CodiceArticoloType):
    def __init__(self, CodiceTipo=None, CodiceValore=None, **kwargs_):
        super(CodiceArticoloTypeSub, self).__init__(CodiceTipo, CodiceValore,  **kwargs_)
models.CodiceArticoloType.subclass = CodiceArticoloTypeSub
# end class CodiceArticoloTypeSub


class AltriDatiGestionaliTypeSub(models.AltriDatiGestionaliType):
    def __init__(self, TipoDato=None, RiferimentoTesto=None, RiferimentoNumero=None, RiferimentoData=None, **kwargs_):
        super(AltriDatiGestionaliTypeSub, self).__init__(TipoDato, RiferimentoTesto, RiferimentoNumero, RiferimentoData,  **kwargs_)
models.AltriDatiGestionaliType.subclass = AltriDatiGestionaliTypeSub
# end class AltriDatiGestionaliTypeSub


class DatiRiepilogoTypeSub(models.DatiRiepilogoType):
    def __init__(self, AliquotaIVA=None, Natura=None, SpeseAccessorie=None, Arrotondamento=None, ImponibileImporto=None, Imposta=None, EsigibilitaIVA=None, RiferimentoNormativo=None, **kwargs_):
        super(DatiRiepilogoTypeSub, self).__init__(AliquotaIVA, Natura, SpeseAccessorie, Arrotondamento, ImponibileImporto, Imposta, EsigibilitaIVA, RiferimentoNormativo,  **kwargs_)
models.DatiRiepilogoType.subclass = DatiRiepilogoTypeSub
# end class DatiRiepilogoTypeSub


class SignatureTypeSub(models.SignatureType):
    def __init__(self, Id=None, SignedInfo=None, SignatureValue=None, KeyInfo=None, Object=None, **kwargs_):
        super(SignatureTypeSub, self).__init__(Id, SignedInfo, SignatureValue, KeyInfo, Object,  **kwargs_)
models.SignatureType.subclass = SignatureTypeSub
# end class SignatureTypeSub


class SignatureValueTypeSub(models.SignatureValueType):
    def __init__(self, Id=None, valueOf_=None, **kwargs_):
        super(SignatureValueTypeSub, self).__init__(Id, valueOf_,  **kwargs_)
models.SignatureValueType.subclass = SignatureValueTypeSub
# end class SignatureValueTypeSub


class SignedInfoTypeSub(models.SignedInfoType):
    def __init__(self, Id=None, CanonicalizationMethod=None, SignatureMethod=None, Reference=None, **kwargs_):
        super(SignedInfoTypeSub, self).__init__(Id, CanonicalizationMethod, SignatureMethod, Reference,  **kwargs_)
models.SignedInfoType.subclass = SignedInfoTypeSub
# end class SignedInfoTypeSub


class CanonicalizationMethodTypeSub(models.CanonicalizationMethodType):
    def __init__(self, Algorithm=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(CanonicalizationMethodTypeSub, self).__init__(Algorithm, anytypeobjs_, valueOf_, mixedclass_, content_,  **kwargs_)
models.CanonicalizationMethodType.subclass = CanonicalizationMethodTypeSub
# end class CanonicalizationMethodTypeSub


class SignatureMethodTypeSub(models.SignatureMethodType):
    def __init__(self, Algorithm=None, HMACOutputLength=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(SignatureMethodTypeSub, self).__init__(Algorithm, HMACOutputLength, anytypeobjs_, valueOf_, mixedclass_, content_,  **kwargs_)
models.SignatureMethodType.subclass = SignatureMethodTypeSub
# end class SignatureMethodTypeSub


class ReferenceTypeSub(models.ReferenceType):
    def __init__(self, Id=None, URI=None, Type=None, Transforms=None, DigestMethod=None, DigestValue=None, **kwargs_):
        super(ReferenceTypeSub, self).__init__(Id, URI, Type, Transforms, DigestMethod, DigestValue,  **kwargs_)
models.ReferenceType.subclass = ReferenceTypeSub
# end class ReferenceTypeSub


class TransformsTypeSub(models.TransformsType):
    def __init__(self, Transform=None, **kwargs_):
        super(TransformsTypeSub, self).__init__(Transform,  **kwargs_)
models.TransformsType.subclass = TransformsTypeSub
# end class TransformsTypeSub


class TransformTypeSub(models.TransformType):
    def __init__(self, Algorithm=None, anytypeobjs_=None, XPath=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(TransformTypeSub, self).__init__(Algorithm, anytypeobjs_, XPath, valueOf_, mixedclass_, content_,  **kwargs_)
models.TransformType.subclass = TransformTypeSub
# end class TransformTypeSub


class DigestMethodTypeSub(models.DigestMethodType):
    def __init__(self, Algorithm=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(DigestMethodTypeSub, self).__init__(Algorithm, anytypeobjs_, valueOf_, mixedclass_, content_,  **kwargs_)
models.DigestMethodType.subclass = DigestMethodTypeSub
# end class DigestMethodTypeSub


class KeyInfoTypeSub(models.KeyInfoType):
    def __init__(self, Id=None, KeyName=None, KeyValue=None, RetrievalMethod=None, X509Data=None, PGPData=None, SPKIData=None, MgmtData=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(KeyInfoTypeSub, self).__init__(Id, KeyName, KeyValue, RetrievalMethod, X509Data, PGPData, SPKIData, MgmtData, anytypeobjs_, valueOf_, mixedclass_, content_,  **kwargs_)
models.KeyInfoType.subclass = KeyInfoTypeSub
# end class KeyInfoTypeSub


class KeyValueTypeSub(models.KeyValueType):
    def __init__(self, DSAKeyValue=None, RSAKeyValue=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(KeyValueTypeSub, self).__init__(DSAKeyValue, RSAKeyValue, anytypeobjs_, valueOf_, mixedclass_, content_,  **kwargs_)
models.KeyValueType.subclass = KeyValueTypeSub
# end class KeyValueTypeSub


class RetrievalMethodTypeSub(models.RetrievalMethodType):
    def __init__(self, URI=None, Type=None, Transforms=None, **kwargs_):
        super(RetrievalMethodTypeSub, self).__init__(URI, Type, Transforms,  **kwargs_)
models.RetrievalMethodType.subclass = RetrievalMethodTypeSub
# end class RetrievalMethodTypeSub


class X509DataTypeSub(models.X509DataType):
    def __init__(self, X509IssuerSerial=None, X509SKI=None, X509SubjectName=None, X509Certificate=None, X509CRL=None, anytypeobjs_=None, **kwargs_):
        super(X509DataTypeSub, self).__init__(X509IssuerSerial, X509SKI, X509SubjectName, X509Certificate, X509CRL, anytypeobjs_,  **kwargs_)
models.X509DataType.subclass = X509DataTypeSub
# end class X509DataTypeSub


class X509IssuerSerialTypeSub(models.X509IssuerSerialType):
    def __init__(self, X509IssuerName=None, X509SerialNumber=None, **kwargs_):
        super(X509IssuerSerialTypeSub, self).__init__(X509IssuerName, X509SerialNumber,  **kwargs_)
models.X509IssuerSerialType.subclass = X509IssuerSerialTypeSub
# end class X509IssuerSerialTypeSub


class PGPDataTypeSub(models.PGPDataType):
    def __init__(self, PGPKeyID=None, PGPKeyPacket=None, anytypeobjs_=None, **kwargs_):
        super(PGPDataTypeSub, self).__init__(PGPKeyID, PGPKeyPacket, anytypeobjs_,  **kwargs_)
models.PGPDataType.subclass = PGPDataTypeSub
# end class PGPDataTypeSub


class SPKIDataTypeSub(models.SPKIDataType):
    def __init__(self, SPKISexp=None, anytypeobjs_=None, **kwargs_):
        super(SPKIDataTypeSub, self).__init__(SPKISexp, anytypeobjs_,  **kwargs_)
models.SPKIDataType.subclass = SPKIDataTypeSub
# end class SPKIDataTypeSub


class ObjectTypeSub(models.ObjectType):
    def __init__(self, Id=None, MimeType=None, Encoding=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(ObjectTypeSub, self).__init__(Id, MimeType, Encoding, anytypeobjs_, valueOf_, mixedclass_, content_,  **kwargs_)
models.ObjectType.subclass = ObjectTypeSub
# end class ObjectTypeSub


class ManifestTypeSub(models.ManifestType):
    def __init__(self, Id=None, Reference=None, **kwargs_):
        super(ManifestTypeSub, self).__init__(Id, Reference,  **kwargs_)
models.ManifestType.subclass = ManifestTypeSub
# end class ManifestTypeSub


class SignaturePropertiesTypeSub(models.SignaturePropertiesType):
    def __init__(self, Id=None, SignatureProperty=None, **kwargs_):
        super(SignaturePropertiesTypeSub, self).__init__(Id, SignatureProperty,  **kwargs_)
models.SignaturePropertiesType.subclass = SignaturePropertiesTypeSub
# end class SignaturePropertiesTypeSub


class SignaturePropertyTypeSub(models.SignaturePropertyType):
    def __init__(self, Target=None, Id=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(SignaturePropertyTypeSub, self).__init__(Target, Id, anytypeobjs_, valueOf_, mixedclass_, content_,  **kwargs_)
models.SignaturePropertyType.subclass = SignaturePropertyTypeSub
# end class SignaturePropertyTypeSub


class DSAKeyValueTypeSub(models.DSAKeyValueType):
    def __init__(self, P=None, Q=None, G=None, Y=None, J=None, Seed=None, PgenCounter=None, **kwargs_):
        super(DSAKeyValueTypeSub, self).__init__(P, Q, G, Y, J, Seed, PgenCounter,  **kwargs_)
models.DSAKeyValueType.subclass = DSAKeyValueTypeSub
# end class DSAKeyValueTypeSub


class RSAKeyValueTypeSub(models.RSAKeyValueType):
    def __init__(self, Modulus=None, Exponent=None, **kwargs_):
        super(RSAKeyValueTypeSub, self).__init__(Modulus, Exponent,  **kwargs_)
models.RSAKeyValueType.subclass = RSAKeyValueTypeSub
# end class RSAKeyValueTypeSub


class DigestValueTypeSub(models.DigestValueType):
    def __init__(self, valueOf_=None, **kwargs_):
        super(DigestValueTypeSub, self).__init__(valueOf_,  **kwargs_)
models.DigestValueType.subclass = DigestValueTypeSub
# end class DigestValueTypeSub


def get_root_tag(node):
    tag = models.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = models.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(models, tag):
        rootClass = getattr(models, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'FatturaElettronicaType'
        rootClass = models.FatturaElettronicaType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'FatturaElettronicaType'
        rootClass = models.FatturaElettronicaType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(content)
        sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    from io import BytesIO as StringIO
    parser = None
    rootNode= parsexmlstring_(inString, parser)
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'FatturaElettronicaType'
        rootClass = models.FatturaElettronicaType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'FatturaElettronicaType'
        rootClass = models.FatturaElettronicaType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from ??? import *\n\n')
        sys.stdout.write('import ??? as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
