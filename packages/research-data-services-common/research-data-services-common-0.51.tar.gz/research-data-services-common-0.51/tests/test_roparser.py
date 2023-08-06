from RDS import ROParser
import json
import unittest


class TestROParser(unittest.TestCase):
    def testfiles(self):
        def test(set: int):
            expands = [True, False]
            cleans = [True, False]
            clamps = [None, 1, 2]

            for expand in expands:
                for clean in cleans:
                    for clamp in clamps:
                        doc = ROParser(
                            json.load(open(f"tests/roparser_tests/{set}_test.json")))
                        filename = f"tests/roparser_tests/{set}_{int(expand)}_{int(clean)}_{clamp}.json"
                        result_json = json.load(open(filename))
                        result = doc.getElement(doc.rootIdentifier,
                                                expand=expand, clean=clean, clamps=clamp)
                        try:
                            assert(result == result_json)
                        except:
                            print(filename, result)

        test(1)
