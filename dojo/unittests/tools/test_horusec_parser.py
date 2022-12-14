import datetime
from os import path

from django.test import TestCase
from dojo.models import Test
from dojo.tools.horusec.parser import HorusecParser


class TestHorusecParser(TestCase):
    def test_get_findings(self):
        """Version 2.6.3 with big project in Python"""
        with open(path.join(path.dirname(__file__), "../scans/horusec/version_2.6.3.json")) as testfile:
            parser = HorusecParser()
            findings = parser.get_findings(testfile, Test())
            self.assertEqual(267, len(findings))

    def test_get_tests(self):
        """Version 2.6.3 with big project in Python"""
        with open(path.join(path.dirname(__file__), "../scans/horusec/version_2.6.3.json")) as testfile:
            parser = HorusecParser()
            tests = parser.get_tests("Horusec Scan", testfile)
            self.assertEqual(1, len(tests))
            test = tests[0]
            self.assertEqual('2.6.3', test.version)
            self.assertEqual(267, len(test.findings))
            findings = test.findings
            with self.subTest(i=0):
                finding = findings[0]
                self.assertEqual("Hard-coded password", finding.title)
                self.assertEqual("Critical", finding.severity)
                self.assertEqual("docker/entrypoint.sh", finding.file_path)
                self.assertEqual(20, finding.line)
                self.assertEqual(datetime.datetime(2021, 10, 1), finding.date)
            with self.subTest(i=50):
                finding = findings[50]
                self.assertEqual("Detected MD5 hash algorithm which is considered insecure. MD5 is not collision resistant and is therefore not suitable as a cryptographic signature. Use SHA256 or SHA3 instead.", finding.title)
                self.assertEqual("Medium", finding.severity)
                self.assertEqual("dojo/tools/huskyci/parser.py", finding.file_path)
                self.assertEqual(55, finding.line)
                self.assertEqual(datetime.datetime(2021, 10, 1), finding.date)
            with self.subTest(i=266):
                finding = findings[266]
                self.assertEqual("Try, Except, Pass detected.", finding.title)
                self.assertEqual("Low", finding.severity)
                self.assertEqual("tests/base_test_class.py", finding.file_path)
                self.assertEqual(191, finding.line)
                self.assertEqual(datetime.datetime(2021, 10, 1), finding.date)

    def test_get_tests_ok(self):
        """Version 2.6.3 with big project in Python"""
        with open(path.join(path.dirname(__file__), "../scans/horusec/horres3.json")) as testfile:
            parser = HorusecParser()
            tests = parser.get_tests("Horusec Scan", testfile)
            self.assertEqual(1, len(tests))
            test = tests[0]
            self.assertEqual(266, len(test.findings))
            findings = test.findings
            with self.subTest(i=0):
                finding = findings[0]
                self.assertEqual("Hard-coded password", finding.title)
                self.assertEqual("Critical", finding.severity)
                self.assertEqual("Dockerfile.nginx", finding.file_path)
                self.assertEqual(83, finding.line)
                self.assertGreaterEqual(finding.scanner_confidence, 3)  # "Firm"
                self.assertLessEqual(finding.scanner_confidence, 5)  # "Firm"
            with self.subTest(i=50):
                finding = findings[50]
                self.assertEqual("Detected MD5 hash algorithm which is considered insecure. MD5 is not collision resistant and is therefore not suitable as a cryptographic signature. Use SHA256 or SHA3 instead.", finding.title)
                self.assertEqual("Medium", finding.severity)
                self.assertEqual("dojo/tools/trufflehog3/parser.py", finding.file_path)
                self.assertEqual(50, finding.line)
                self.assertGreaterEqual(finding.scanner_confidence, 6)  # "Tentative"
            with self.subTest(i=265):
                finding = findings[265]
                self.assertEqual("Try, Except, Pass detected.", finding.title)
                self.assertEqual("Low", finding.severity)
                self.assertEqual("tests/base_test_class.py", finding.file_path)
                self.assertEqual(191, finding.line)
                self.assertLessEqual(finding.scanner_confidence, 2)  # "Certain"
