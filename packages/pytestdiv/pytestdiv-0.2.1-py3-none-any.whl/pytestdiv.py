"""
A Plugin to split tests into equally sized groups
"""
import pytest


def pytest_addoption(parser, pluginmanager):
    parser.addoption("--divide", type=str, metavar="M/N",
                     default=None,
                     help="Split tests into groups of N tests and execute the Mth group")
    parser.addoption("--divide-files", action="store_true", default=False,
                     help="Split groups by file instead of by test")


def pytest_collection_modifyitems(session: pytest.Session, config, items):
    divide = config.option.divide
    if divide is not None:
        assert "/" in divide, "--divide must be M/N"

        try:
            m, n = divide.split("/", 1)
            m = int(m)
            n = int(n)

            assert n > 0, f"N must be positive"
            assert m > 0, f"M must be positive"
            assert m <= n, f"M must be <= than M for --divide M/N"

            new_items = []
            if config.option.divide_files:
                # share out test files
                files = {}
                for item in items:
                    filename = str(item.fspath)
                    if filename not in files:
                        files[filename] = []
                    files[filename].append(item)
                filenames = sorted(files.keys())
                for i in range(len(filenames)):
                    if (i % n) == (m - 1):
                        filename = filenames[i]
                        new_items.extend(files[filename])
            else:
                # share out test functions
                for i in range(len(items)):
                    if (i % n) == (m - 1):
                        new_items.append(items[i])
            items.clear()
            items.extend(new_items)
        except ValueError:
            assert False, f"{divide} is not valid for --divide"




