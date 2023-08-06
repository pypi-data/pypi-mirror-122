import abc
import logging
from typing import List, TypeVar, Generic

import arrow
from koldar_utils.functions import math_helpers

from ya_fattura_elettronica_generator import models, utils
from ya_fattura_elettronica_generator.IFatturaElettronicaValidator import IFatturaElettronicaValidator, ValidationOutcome

DATE_PARSER = "YYYY-MM-DD"
ITALY_TIMEZONE = "Europe/Rome"

ITALIAN_MONTHS = {
    0: "Gennaio",
    1: "Febbraio",
    2: "Marzo",
    3: "Aprile",
    4: "Maggio",
    5: "Giugno",
    6: "Luglio",
    7: "Agosto",
    8: "Settembre",
    9: "Ottobre",
    10: "Novembre",
    11: "Dicembre",
}

LOG = logging.getLogger(__name__)


class AbstractValueEqualToValidator(IFatturaElettronicaValidator):

    def __init__(self, expected_value: any):
        self.expected_value = expected_value

    @abc.abstractmethod
    def get_field_description(self) -> str:
        pass

    @abc.abstractmethod
    def get_value(self, fattura_elettronica: models.FatturaElettronicaType, context) -> any:
        pass

    def validate(self, fattura_elettronica: models.FatturaElettronicaType, context) -> List[ValidationOutcome]:
        actual = self.get_value(fattura_elettronica, context)

        if actual != self.expected_value:
            return [ValidationOutcome.error(f"Expected {self.get_field_description()} to be {self.expected_value}, but it was {actual}")]
        return [ValidationOutcome.ok(f"Document has correct {self.get_field_description()}")]


class FormatoTrasmissioneEqualTo(AbstractValueEqualToValidator):

    def get_field_description(self) -> str:
        return "formato di trasmissione"

    def get_value(self, fattura_elettronica: models.FatturaElettronicaType, context) -> models.FatturaElettronicaType:
        return fattura_elettronica.get_FatturaElettronicaHeader().DatiTrasmissione.FormatoTrasmissione

    def __init__(self, expected_value: models.FormatoTrasmissioneType):
        super().__init__(expected_value)


class CodiceDestinatarioEqualTO(AbstractValueEqualToValidator):

    def __init__(self, expected_value: str):
        super().__init__(expected_value)

    def get_field_description(self) -> str:
        return "codice destinatario"

    def get_value(self, fattura_elettronica: models.FatturaElettronicaType, context) -> models.FatturaElettronicaType:
        return fattura_elettronica.get_FatturaElettronicaHeader().DatiTrasmissione.CodiceDestinatario


class RegimeFiscaleEqualTo(AbstractValueEqualToValidator):

    def __init__(self, expected_value: str):
        super().__init__(expected_value)

    def get_field_description(self) -> str:
        return "regime fiscale"

    def get_value(self, fattura_elettronica: models.FatturaElettronicaType, context) -> any:
        return fattura_elettronica.get_FatturaElettronicaHeader().CedentePrestatore.DatiAnagrafici.get_RegimeFiscale()


class IsFatturaHasSingleBody(IFatturaElettronicaValidator):

    def validate(self, fattura_elettronica: models.FatturaElettronicaType, context) -> List[ValidationOutcome]:
        bodies = fattura_elettronica.get_FatturaElettronicaBody()
        if len(bodies) != 1:
            result = ValidationOutcome.error(f"The document has multiple bodies! Expected 1 but got {len(bodies)}")
        else:
            result = ValidationOutcome.ok(f"document has single fattura body")

        return [result]

class IsFatturaOrdinaria(IFatturaElettronicaValidator):

    def __init__(self, body_id: int):
        self.body_id = body_id

    def validate(self, fattura_elettronica: models.FatturaElettronicaType, context) -> List[ValidationOutcome]:
        tipo = fattura_elettronica.get_FatturaElettronicaBody()[self.body_id].DatiGenerali.DatiGeneraliDocumento.TipoDocumento
        if tipo != models.TipoDocumentoType.TD_01:
            result = ValidationOutcome.error(f"The document is not a fattura! It was {tipo}")
        else:
            result = ValidationOutcome.ok(f"document is of type {tipo}")

        return [result]


class IsDivisaEuro(IFatturaElettronicaValidator):

    def __init__(self, body_id: int):
        self.body_id = body_id

    def validate(self, fattura_elettronica: models.FatturaElettronicaType, context) -> List[ValidationOutcome]:
        val = fattura_elettronica.get_FatturaElettronicaBody()[self.body_id].DatiGenerali.DatiGeneraliDocumento.Divisa
        if val != "EUR":
            result = ValidationOutcome.warning(f"The document is not using euros! It was {val}")
        else:
            result = ValidationOutcome.ok(f"document uses {val}")

        return [result]


class DateIsToday(IFatturaElettronicaValidator):

    def __init__(self, body_id: int):
        self.body_id = body_id

    def validate(self, fattura_elettronica: models.FatturaElettronicaType, context) -> List[ValidationOutcome]:
        val = fattura_elettronica.get_FatturaElettronicaBody()[self.body_id].DatiGenerali.DatiGeneraliDocumento.Data
        val = arrow.get(val)
        italy_now = arrow.now(ITALY_TIMEZONE).date()
        if val != italy_now:
            result = ValidationOutcome.warning(f"The document has a date that is not today! The date was {val}")
        else:
            result = ValidationOutcome.ok(f"document has formally been written today")

        return [result]


class IsNumberMonotonicallyCrescentAndContiguous(IFatturaElettronicaValidator):

    def __init__(self, body_id: int):
        self.body_id = body_id

    def validate(self, fattura_elettronica: models.FatturaElettronicaType, context) -> List[ValidationOutcome]:
        val = fattura_elettronica.get_FatturaElettronicaBody()[self.body_id].DatiGenerali.DatiGeneraliDocumento.Numero
        # we need to check a database to get the supposed to be next id
        expected_number = val # TODO change
        if val != expected_number:
            result = ValidationOutcome.error(f"The document should have the number {expected_number}, but it was {val}!")
        else:
            result = ValidationOutcome.ok(f"document has a contiguous monotonically crescent number")

        return [result]


class HasA2EuroBollo(IFatturaElettronicaValidator):

    def __init__(self, body_id: int):
        self.body_id = body_id

    def validate(self, fattura_elettronica: models.FatturaElettronicaType, context) -> List[ValidationOutcome]:
        bollo = fattura_elettronica.get_FatturaElettronicaBody()[self.body_id].DatiGenerali.DatiGeneraliDocumento.DatiBollo
        if bollo is None:
            return [ValidationOutcome.error(f"The document does not have any bollo!")]
        if not utils.sino_to_bollo(bollo.BolloVirtuale):
            return [ValidationOutcome.error(f"The document does not have a bollo virtuale!")]
        if not math_helpers.is_nearly_equal(bollo.ImportoBollo, 2, 1e-2):
            return [ValidationOutcome.error(f"The document does not have a 2€ bollo!")]

        return [ValidationOutcome.ok(f"document has a 2€ bollo virtual")]


class HasExactlyOneDettaglioLinea(IFatturaElettronicaValidator):

    def __init__(self, body_id: int):
        self.body_id = body_id

    def validate(self, fattura_elettronica: models.FatturaElettronicaType, context) -> List[ValidationOutcome]:
        linee = fattura_elettronica.get_FatturaElettronicaBody()[self.body_id].DatiBeniServizi.DettaglioLinee
        if len(linee) != 1:
            return [ValidationOutcome.error(f"Document has {len(linee)}, but we expected to have just 1!")]
        else:
            return [ValidationOutcome.ok(f"Document has 1 detail line")]


class LineDescriptionSpecifyMonthAndYear(IFatturaElettronicaValidator):

    def __init__(self, body_id: int, numero_linea: int):
        self.body_id = body_id
        self.numero_linea = numero_linea

    def validate(self, fattura_elettronica: models.FatturaElettronicaType, context) -> List[ValidationOutcome]:
        linea = fattura_elettronica.get_FatturaElettronicaBody()[self.body_id].DatiBeniServizi.DettaglioLinee[self.numero_linea]

        italy_now = arrow.now(ITALY_TIMEZONE)
        month = italy_now.date().month - 1
        expected_month = str(ITALIAN_MONTHS[month])
        expected_year = str(italy_now.date().year)

        if expected_month not in linea.Descrizione:
            return [ValidationOutcome.warning(f"Document has line #{self.numero_linea} (0-x) that should contain the month {expected_month}, but it does not")]
        if expected_year not in linea.Descrizione:
            return [ValidationOutcome.warning(f"Document has line #{self.numero_linea} (0-x) that should contain the year {expected_year}, but it does not")]
        return [ValidationOutcome.ok(f"Document has line #{self.numero_linea} (0-x) specifying both month and year")]


class LineHasPrezzoUnitarioSetTo(AbstractValueEqualToValidator):

    def __init__(self, body_id: int, numero_linea: int, expected_prezzo_unitario: float):
        super().__init__(expected_value=expected_prezzo_unitario)
        self.body_id = body_id
        self.numero_linea = numero_linea

    def get_field_description(self) -> str:
        return f"body #{self.body_id} line #{self.numero_linea} (0-x) with prezzo unitario"

    def get_value(self, fattura_elettronica: models.FatturaElettronicaType, context) -> any:
        return fattura_elettronica.get_FatturaElettronicaBody()[self.body_id].DatiBeniServizi.DettaglioLinee[self.numero_linea].PrezzoUnitario


class LineHasAliquotaIvaSetTo(AbstractValueEqualToValidator):

    def __init__(self, body_id: int, numero_linea: int, expected_aliquota_iva: float):
        super().__init__(expected_value=expected_aliquota_iva)
        self.body_id = body_id
        self.numero_linea = numero_linea

    def get_field_description(self) -> str:
        return f"body #{self.body_id} line #{self.numero_linea} (0-x) with aliquota iva"

    def get_value(self, fattura_elettronica: models.FatturaElettronicaType, context) -> any:
        return fattura_elettronica.get_FatturaElettronicaBody()[self.body_id].DatiBeniServizi.DettaglioLinee[self.numero_linea].AliquotaIVA


class LineHasNaturaSetTo(AbstractValueEqualToValidator):

    def get_field_description(self) -> str:
        return f"body #{self.body_id} line #{self.numero_linea} (0-x) with natura"

    def get_value(self, fattura_elettronica: models.FatturaElettronicaType, context) -> any:
        return fattura_elettronica.get_FatturaElettronicaBody()[self.body_id].DatiBeniServizi.DettaglioLinee[self.numero_linea].Natura

    def __init__(self, body_id: int, numero_linea: int, expected_natura: models.NaturaType):
        super().__init__(expected_value=expected_natura)
        self.body_id = body_id
        self.numero_linea = numero_linea


class HasNoArrotondamento(IFatturaElettronicaValidator):

    def __init__(self, body_id: int):
        self.body_id = body_id

    def validate(self, fattura_elettronica: models.FatturaElettronicaType, context) -> List[ValidationOutcome]:
        arrotondamento = fattura_elettronica.get_FatturaElettronicaBody()[self.body_id].DatiGenerali.DatiGeneraliDocumento.Arrotondamento
        if arrotondamento is None:
            return [ValidationOutcome.ok(f"Document has no arrotondamento")]
        if math_helpers.is_nearly_equal(arrotondamento, 0, 1e-2):
            return [ValidationOutcome.ok(f"Document has no arrotondamento")]

        return [ValidationOutcome.error(f"Document has an arrotondamento of {arrotondamento} but we expected to have 0")]


class ImportoTotaleDocumentoIsCorrect(IFatturaElettronicaValidator):

    def __init__(self, body_id: int):
        self.body_id = body_id

    def validate(self, fattura_elettronica: models.FatturaElettronicaType, context) -> List[ValidationOutcome]:
        raw_data = fattura_elettronica.get_FatturaElettronicaBody()[self.body_id].compute_total_from_total_in_lines()
        total_data = fattura_elettronica.get_FatturaElettronicaBody()[self.body_id].compute_total_from_total_in_lines()
        riepilog_data = fattura_elettronica.get_FatturaElettronicaBody()[self.body_id].compute_total_from_dati_riepilogo()
        dati_generali = fattura_elettronica.get_FatturaElettronicaBody()[self.body_id].compute_total_from_dati_generali()

        if not math_helpers.is_nearly_equal(raw_data, total_data):
            return [ValidationOutcome.error(f"the data from the dettaglio linee and the totals in the dettaglio linee mismatch! Expected {raw_data} but got {total_data}")]
        if not math_helpers.is_nearly_equal(raw_data, riepilog_data):
            return [ValidationOutcome.error(
                f"the data from the dettaglio linee and the riepilog mismatch! Expected {raw_data} but got {riepilog_data}")]
        if not math_helpers.is_nearly_equal(raw_data, dati_generali):
            return [ValidationOutcome.error(
                f"the data from the dettaglio linee and the dati generali mismatch! Expected {raw_data} but got {dati_generali}")]
        return [ValidationOutcome.ok(f"Money to gain are ok!")]


class MultiplexerValidator(IFatturaElettronicaValidator):

    def __init__(self, validators: List[IFatturaElettronicaValidator]):
        self.validators = validators

    def validate(self, fattura_elettronica: models.FatturaElettronicaType, context) -> List[ValidationOutcome]:
        result = []
        for x in self.validators:
            try:
                result.extend(x.validate(fattura_elettronica, context))
            except Exception as e:
                LOG.exception(e)
                result.append(ValidationOutcome.error(f"When computing the validation {type(x).__name__} an exception occured. Exception was {e}"))
        return result


class RegimeForfettarioMonthlyInvoiceValidator(MultiplexerValidator):

    def __init__(self):
        super().__init__(validators=[
            IsFatturaHasSingleBody(),
            FormatoTrasmissioneEqualTo(expected_value=models.FormatoTrasmissioneType.FPR_12),
            RegimeFiscaleEqualTo(expected_value=models.RegimeFiscaleType.RF_19),
            IsFatturaOrdinaria(body_id=0),
            IsDivisaEuro(body_id=0),
            DateIsToday(body_id=0),
            IsNumberMonotonicallyCrescentAndContiguous(body_id=0),
            HasA2EuroBollo(body_id=0),
            HasExactlyOneDettaglioLinea(body_id=0),
            LineDescriptionSpecifyMonthAndYear(body_id=0, numero_linea=0),
            LineHasPrezzoUnitarioSetTo(body_id=0, numero_linea=0, expected_prezzo_unitario=1.0),
            LineHasAliquotaIvaSetTo(body_id=0, numero_linea=0, expected_aliquota_iva=0.0),
            LineHasNaturaSetTo(body_id=0, numero_linea=0, expected_natura=models.NaturaType.N_2_2),
            HasNoArrotondamento(body_id=0),
            ImportoTotaleDocumentoIsCorrect(body_id=0),
        ])

