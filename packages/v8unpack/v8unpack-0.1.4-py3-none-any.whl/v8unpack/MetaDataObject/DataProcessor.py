from ..MetaDataObject.core.Container import Container


class DataProcessor(Container):
    version = '83'

    def __init__(self):
        super(DataProcessor, self).__init__()

    @classmethod
    def get_decode_header(cls, header_data):
        return header_data[0][1][3][1]
