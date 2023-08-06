import pytest
from jsm_user_services.support.string_utils import get_first_value_from_comma_separated_string

@pytest.mark.parametrize("ips_chain, expected_ip", [("1.1.1.1 , 2.2.2.2", "1.1.1.1"), ("1.1.1.1 , 2.2.2.2", "1.1.1.1"), ("7.7.7.7, 8.8.8.8, 1.1.1.1", "7.7.7.7")])
def test_should_take_first_ip_from_chain_of_ips_without_spaces(ips_chain, expected_ip):
    first_ip = get_first_value_from_comma_separated_string(ips_chain)

    assert first_ip == expected_ip
