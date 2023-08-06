import pytest
import requests_mock
from chaoslib.exceptions import ActivityFailed

from chaosgandi.domains.probes import list_domains, list_nameservers


def test_list_domains():
    with requests_mock.mock() as m:
        m.get(
            "https://api.gandi.net/v5/domain/domains",
            json=[
                {
                    "status": ["clientTransferProhibited"],
                    "dates": {
                        "created_at": "2019-02-13T11:04:18Z",
                        "registry_created_at": "2019-02-13T10:04:18Z",
                        "registry_ends_at": "2021-02-13T10:04:18Z",
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
                },
                {
                    "status": [],
                    "dates": {
                        "created_at": "2019-01-15T14:19:59Z",
                        "registry_created_at": "2019-01-15T13:19:58Z",
                        "registry_ends_at": "2020-01-15T13:19:58Z",
                        "updated_at": "2019-01-15T13:30:42Z",
                    },
                    "tags": [],
                    "fqdn": "example.com",
                    "id": "42927d64-18c8-11e9-b9b5-00163ec4cb00",
                    "autorenew": False,
                    "tld": "fr",
                    "owner": "alice_doe",
                    "orga_owner": "alice_doe",
                    "domain_owner": "Alice Doe",
                    "nameserver": {"current": "livedns"},
                    "href": "https://api.test/v5/domain/domains/example.com",
                    "fqdn_unicode": "example.com",
                },
            ],
        )

        domains = list_domains(secrets={"apikey": "1234"})
        assert len(domains) == 2


def test_list_domains_filtered_by_tld():
    with requests_mock.mock() as m:
        m.get(
            "https://api.gandi.net/v5/domain/domains",
            json=[
                {
                    "status": ["clientTransferProhibited"],
                    "dates": {
                        "created_at": "2019-02-13T11:04:18Z",
                        "registry_created_at": "2019-02-13T10:04:18Z",
                        "registry_ends_at": "2021-02-13T10:04:18Z",
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
            ],
        )

        domains = list_domains(tld_filter="net", secrets={"apikey": "1234"})
        assert len(domains) == 1


def test_list_domains_filtered_by_fqdn():
    with requests_mock.mock() as m:
        m.get(
            "https://api.gandi.net/v5/domain/domains",
            json=[
                {
                    "status": ["clientTransferProhibited"],
                    "dates": {
                        "created_at": "2019-02-13T11:04:18Z",
                        "registry_created_at": "2019-02-13T10:04:18Z",
                        "registry_ends_at": "2021-02-13T10:04:18Z",
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
                },
                {
                    "status": [],
                    "dates": {
                        "created_at": "2019-01-15T14:19:59Z",
                        "registry_created_at": "2019-01-15T13:19:58Z",
                        "registry_ends_at": "2020-01-15T13:19:58Z",
                        "updated_at": "2019-01-15T13:30:42Z",
                    },
                    "tags": [],
                    "fqdn": "example.com",
                    "id": "42927d64-18c8-11e9-b9b5-00163ec4cb00",
                    "autorenew": False,
                    "tld": "fr",
                    "owner": "alice_doe",
                    "orga_owner": "alice_doe",
                    "domain_owner": "Alice Doe",
                    "nameserver": {"current": "livedns"},
                    "href": "https://api.test/v5/domain/domains/example.com",
                    "fqdn_unicode": "example.com",
                },
            ],
        )

        domains = list_domains(
            fqdn_filter="example.*", secrets={"apikey": "1234"}
        )
        assert len(domains) == 2


def test_list_domains_fails_on_error_4xx_and_5xx():
    with requests_mock.mock() as m:
        m.get("https://api.gandi.net/v5/domain/domains", status_code=404)

        with pytest.raises(ActivityFailed):
            list_domains(secrets={"apikey": "1234"})


def test_list_ns():
    with requests_mock.mock() as m:
        m.get(
            "https://api.gandi.net/v5/domain/domains/example.net/nameservers",
            json=["mydns.net", "myotherdns.net"],
        )

        ns = list_nameservers(domain="example.net", secrets={"apikey": "1234"})
        assert len(ns) == 2


def test_list_ns_fails_on_error_4xx_and_5xx():
    with requests_mock.mock() as m:
        m.get(
            "https://api.gandi.net/v5/domain/domains/example.net/nameservers",
            status_code=404,
        )

        with pytest.raises(ActivityFailed):
            list_nameservers(domain="example.net", secrets={"apikey": "1234"})
