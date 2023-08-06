from chttp import Fetcher


def test_downlotad():
    test_packages = ["flask", "fastapi"]
    test_urls = [f"https://pypi.org/pypi/{package}/json" for package in test_packages]
    packages = Fetcher(test_urls)
    for p in packages.get_all():
        print(p, p.url)
