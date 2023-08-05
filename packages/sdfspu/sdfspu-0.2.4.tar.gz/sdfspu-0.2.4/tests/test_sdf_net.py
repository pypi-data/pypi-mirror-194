from sdfspu.sdf_net import get_ip


def test_get_ip():
    assert isinstance(get_ip(), str)
