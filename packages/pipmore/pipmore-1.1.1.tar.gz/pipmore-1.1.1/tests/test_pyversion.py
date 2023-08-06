import unittest

from pipmore import pyversion


class Test_PyVersionFromClassifier(unittest.TestCase):
    def test_pyversions_from_classifier(self):
        classifiers = ["Programming Language :: Python :: 3.10"]
        expected = ["3.10"]
        actual = pyversion.from_classifiers(classifiers)
        self.assertEqual(actual, expected)

    def test_empty_classifiers(self):
        classifiers = []
        expected = []
        actual = pyversion.from_classifiers(classifiers)
        self.assertEqual(actual, expected)

    def test_minimum_from_classifiers(self):
        classifiers = [
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.10",
        ]
        expected = "3.4"
        actual = pyversion.minimum_from_classifiers(classifiers)
        self.assertEqual(actual, expected)

    def test_minimum_from_requires_ge(self):
        requires = ">=3.8"
        expected = "3.8"
        actual = pyversion.minimum_from_requires(requires)
        self.assertEqual(actual, expected)

    def test_classifier_smaller_than_requires(self):
        classifiers = [
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.10",
        ]
        requires = ">=3.8"
        expected = "3.4"
        actual = pyversion.minimum_from_combined(requires, classifiers)
        self.assertEqual(actual, expected)

    def test_requires_smaller_than_classifier(self):
        classifiers = ["Programming Language :: Python :: 3.10"]
        requires = ">=3.8"
        expected = "3.8"
        actual = pyversion.minimum_from_combined(requires, classifiers)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
