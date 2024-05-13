import abc


class InterfaceOCR(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'extract_text') and
                callable(subclass.extract_text) or
                NotImplemented)

    @abc.abstractmethod
    def extract_text(self, pdf_file: str, output_file: str, data: bool):
        raise NotImplementedError
