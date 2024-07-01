import pytest

from onlyPDF.pdf_reader import PDFReader
from onlyPDF.pdf_parser import PDFParser



class TestPDFParser():


    def test_parser(self):
        file_path= './others/pdf_files/sample.pdf'
        pdf_reader = PDFReader(path=file_path)

        pdf_parser = PDFParser(content=pdf_reader.content)

        pdf_parser.parser()

        print(f'header:{pdf_parser.header}')
        print(f'body:{pdf_parser.body}')
        print(f'crt:{pdf_parser.crt}')
        print(f'trailer:{pdf_parser.trailer}')
        print(f'obj_list:{pdf_parser.obj_list}')

        assert pdf_parser.pdf_version != ''
        assert isinstance(pdf_parser.header,list)
        assert isinstance(pdf_parser.body, list)
        assert isinstance(pdf_parser.crt, list)
        assert isinstance(pdf_parser.trailer, list)
        assert isinstance(pdf_parser.obj_list, dict)
