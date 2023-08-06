import abc
from typing import List

from ya_fattura_elettronica_generator.models import FatturaElettronicaType


class IFatturaElettronicaGenerator(abc.ABC):

    @abc.abstractmethod
    def generate(self, context) -> FatturaElettronicaType:
        """
        Generate a new fattura elettronica
        :param context: additional dcontext to create the fattura
        :return: a mdoel repersenting the fattura elettronica you want to have
        """
        pass

    @abc.abstractmethod
    def validate(self, context) -> List[str]:
        """
        Perform a sequence of checks to ensure that the fattura elettronica is for sure compliant
        :param context:
        :return:
        """
        pass

    def serialize_to_xml_file(self, fattura_elettronica: FatturaElettronicaType, output_file: str) -> str:
        """
        Serialize the model into a xml file
        :param fattura_elettronica: fattura eletronica to output
        :param output_file:
        :return:
        """
        fattura_elettronica.export(
            output_file,
            level=4,
            pretty_print=True
        )
        return output_file