from datetime import datetime, timedelta

import pytest
from chaoslib.exceptions import ActivityFailed

from chaosgandi.domains.tolerances import (
    domain_nameservers_should_be_a_subset_of,
    domain_nameservers_should_be_a_superset_of,
    domain_nameservers_should_be_exactly,
    domain_nameservers_should_contain,
    domain_nameservers_should_not_contain,
    domains_should_not_expire_in,
)


def test_domain_nameservers_should_contain():
    assert domain_nameservers_should_contain(["ns1", "ns2"], "ns2") is True


def test_domain_nameservers_should_not_contain():
    assert domain_nameservers_should_not_contain(["ns1", "ns2"], "ns3") is True


def test_domain_nameservers_should_be_a_subset_of():
    assert (
        domain_nameservers_should_be_a_subset_of(["ns1", "ns2"], ["ns2"])
        is True
    )


def test_domain_nameservers_should_be_a_subset_of_fails():
    assert (
        domain_nameservers_should_be_a_subset_of(["ns1", "ns2"], ["ns2", "ns3"])
        is False
    )


def test_domain_nameservers_should_be_a_subset_when_equal():
    assert (
        domain_nameservers_should_be_a_subset_of(["ns1", "ns2"], ["ns2", "ns1"])
        is True
    )


def test_domain_nameservers_should_be_a_superset_of():
    assert (
        domain_nameservers_should_be_a_superset_of(
            ["ns1", "ns2"], ["ns2", "ns1", "ns3"]
        )
        is True
    )


def test_domain_nameservers_should_be_a_superset_of_fails():
    assert (
        domain_nameservers_should_be_a_superset_of(
            ["ns1", "ns2"], ["ns2", "ns5", "ns3"]
        )
        is False
    )


def test_domain_nameservers_should_be_a_superset_of_when_equal():
    assert (
        domain_nameservers_should_be_a_superset_of(
            ["ns1", "ns2"], ["ns2", "ns1"]
        )
        is True
    )


def test_domain_nameservers_should_be_exactly():
    assert (
        domain_nameservers_should_be_exactly(["ns1", "ns2"], ["ns2", "ns1"])
        is True
    )


def test_domains_should_not_expire_in():
    next_week = datetime.today() + timedelta(days=7)
    next_week = next_week.isoformat() + "Z"
    domains = [
        {
            "status": ["clientTransferProhibited"],
            "dates": {
                "created_at": "2019-02-13T11:04:18Z",
                "registry_created_at": "2019-02-13T10:04:18Z",
                "registry_ends_at": next_week,
                "updated_at": "2019-02-25T16:20:49Z",
            },
            "tags": [],
            "fqdn": "example.net",
            "id": "ba1167be-2f76-11e9-9dfb-00163ec4cb00",
            "autorenew": False,
            "tld": "net",
            "owner": "alice_doe",
            "orga_owner": "alice_doe",
            "domain_owner": "Alice Doe",
            "nameserver": {"current": "livedns"},
            "href": "https://api.test/v5/domain/domains/example.net",
            "fqdn_unicode": "example.net",
        }
    ]

    assert domains_should_not_expire_in(domains, "1 day") is True


def test_domains_will_expire_next_week_fails():
    next_week = datetime.today() + timedelta(days=7)
    next_week = next_week.isoformat() + "Z"
    domains = [
        {
            "status": ["clientTransferProhibited"],
            "dates": {
                "created_at": "2019-02-13T11:04:18Z",
                "registry_created_at": "2019-02-13T10:04:18Z",
                "registry_ends_at": next_week,
                "updated_at": "2019-02-25T16:20:49Z",
            },
            "tags": [],
            "fqdn": "example.net",
            "id": "ba1167be-2f76-11e9-9dfb-00163ec4cb00",
            "autorenew": False,
            "tld": "net",
            "owner": "alice_doe",
            "orga_owner": "alice_doe",
            "domain_owner": "Alice Doe",
            "nameserver": {"current": "livedns"},
            "href": "https://api.test/v5/domain/domains/example.net",
            "fqdn_unicode": "example.net",
        }
    ]

    assert domains_should_not_expire_in(domains, "1 month") is False


def test_domains_fails_when_cannot_parse_date():
    with pytest.raises(ActivityFailed) as x:
        domains_should_not_expire_in([], "say months")
