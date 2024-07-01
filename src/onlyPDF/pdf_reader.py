# read PDF File

from .util import FileOperator

class PDFReader():
    """PDF Reader
    """
    def __init__(
            self,
            path: str,
        ):
        """Initialize PDF Reader Object

        Args:
            path (str): PDF File path
        """
        self.content = FileOperator().read_file_lines(path=path)


