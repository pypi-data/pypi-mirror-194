import os
from unittest import TestCase

from utils import PDFFile

TEST_PDF_FILE = PDFFile('tests/example.pdf')


class TestPDFFile(TestCase):
    def test_n_pages(self):
        self.assertEqual(TEST_PDF_FILE.n_pages, 16)

    def test_tables(self):
        os.system(f'rm -rf {TEST_PDF_FILE.dir_tables}')
        table_files = TEST_PDF_FILE.table_files
        self.assertEqual(len(table_files), 5)

        table_files = TEST_PDF_FILE.table_files
        self.assertEqual(len(table_files), 5)
