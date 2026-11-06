from cyberfusion.Nodechup.utilities import _parse_semver


def test_semver_27_release() -> None:
    ver = "v27.0.0-alpha.0.0.0"
    parsed = _parse_semver(ver)
    assert parsed[0] == 27
    assert parsed[1] == 0
    assert parsed[2] == 0
    assert parsed[3] is False


def test_existing_semver() -> None:
    vers = [
        ("v26.13.0", (26, 13, 0, True)),
        ("v21.2.0", (21, 2, 0, True)),
        ("v21.7.0", (21, 7, 0, True)),
        ("v23.3.0", (23, 3, 0, True)),
    ]
    for v, res in vers:
        parsed = _parse_semver(v)
        assert parsed == res
