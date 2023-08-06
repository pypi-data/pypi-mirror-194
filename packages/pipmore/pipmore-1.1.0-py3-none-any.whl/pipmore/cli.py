import argparse

from . import package

base_url = "https://pypi.org"


def cli():
    parser = argparse.ArgumentParser(
        prog="pipmore",
        description="Find the latest package version supported by a specific python version",
        epilog="https://github.com/andregri/pipmore",
    )

    parser.add_argument("package_name")
    parser.add_argument("py_version")

    args = parser.parse_args()

    max_release = None
    releases = package.releases(base_url, args.package_name)

    for release in releases:
        pkg = package.Release(base_url, args.package_name, release)
        requires_python = pkg.requires_python()
        max_release = package.find_max_release(
            release, max_release, args.py_version, requires_python
        )

    print(max_release)


if __name__ == "__main__":
    cli()
