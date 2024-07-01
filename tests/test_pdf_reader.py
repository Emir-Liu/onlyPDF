from onlyPDF.pdf_reader import PDFReader

class TestPDFReader():

    def test_init(self):
        file_path= './others/pdf_files/sample.pdf'
        pdf_reader = PDFReader(path=file_path)

        # check content
        for line_content in pdf_reader.content:
            assert type(line_content) == bytes

