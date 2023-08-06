def from_classifiers(classifiers):
    """
    Return a list of python versions extracted from classifiers.
    Return an empty list if classifiers are not defined.
    """

    py_versions = []
    for cl in classifiers:
        version = cl.split(" :: ")[-1]
        if version in ["3.4", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10", "3.11"]:
            py_versions.append(version)

    return py_versions


def minimum_from_pyversions(py_versions):
    """
    Return the minimum python version from a list of versions
    """
    minors = [int(v.split(".")[-1]) for v in py_versions]
    index = minors.index(min(minors))

    return py_versions[index]


def minimum_from_classifiers(classifiers):
    """
    Returns the minimum python version listed in package classifiers
    """
    py_versions = from_classifiers(classifiers)
    return minimum_from_pyversions(py_versions)


def minimum_from_requires(requires_python):
    """
    Parse the minimum python version from requires_python info
    """
    if requires_python[:2] == ">=":
        return requires_python[2:]


def minimum_from_combined(requires_python, classifiers):
    """
    Returns the minimum python version combining the classifiers
    and the requires_python field
    """

    min_requires = minimum_from_requires(requires_python)
    min_classifier = minimum_from_classifiers(classifiers)

    return minimum_from_pyversions([min_requires, min_classifier])
