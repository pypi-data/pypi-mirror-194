#  Copyright 2021,2022  Dominik Sekotill <dom.sekotill@kodo.org.uk>
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Extensions for "requests"
"""

from __future__ import annotations

import ipaddress
from typing import Any
from typing import Mapping
from urllib.parse import urlparse

import requests.adapters
from urllib3 import connection
from urllib3 import connectionpool


def redirect(
	session: requests.Session,
	prefix: str,
	address: ipaddress.IPv4Address,
	certificate: str|None = None,
) -> None:
	"""
	Redirect all requests for "prefix" to a given address

	This function allows a user to completely override DNS and local name lookups, allowing
	fixtures to be contacted via any configured URL without having to mess with the system's
	name resolution services.

	"prefix" is formated as either "{hostname}[:{port}]" or "{schema}://{hostname}[:{port}]"
	where "schema" defaults to "http".
	"""
	if not prefix.startswith("http://") or prefix.startswith("https://"):
		prefix = f"http://{prefix}" if certificate is None else f"https://{prefix}"
	session.mount(prefix, _DirectedAdapter(address, certificate))


class _DirectedAdapter(requests.adapters.HTTPAdapter):
	"""
	An alternative HTTP adapter that directs all connections to a configured address

	Instances of this class are mounted on a `requests.Session` as adapters for specific URL
	prefixes.

	Rather than using this class directly the easiest way to use it is with the `redirect`
	function.
	"""

	def __init__(self, destination: ipaddress.IPv4Address, certificate: str|None):
		super().__init__()
		self.destination = destination
		self.certificate = certificate

	def get_connection(self, url: str, proxies: Mapping[str, str]|None = None) -> connectionpool.HTTPConnectionPool:
		parts = urlparse(url)
		if parts.scheme == "https":
			return _HTTPSConnectionPool(parts.hostname, parts.port, address=self.destination)
		else:
			return _HTTPConnectionPool(parts.hostname, parts.port, address=self.destination)

	def cert_verify(
		self,
		conn: connection.HTTPConnection,
		url: str,
		verify: bool|str,
		cert: str|tuple[str, str],
	) -> None:
		if verify is False:
			raise ValueError("Never disable TLS verification")
		if verify is not True:
			u = urlparse(url)
			raise ValueError(
				f"To supply verification certificates please use "
				f"redirect(session, '{u.scheme}://{u.netloc}', '{self.destination}', Path('{verify}'))",
			)
		super().cert_verify(conn, url, True, cert)  # type: ignore
		conn.ca_cert_data = self.certificate  # type: ignore


class _HTTPConnectionPool(connectionpool.HTTPConnectionPool):

	class ConnectionCls(connection.HTTPConnection):

		# Undo the damage done by parent class which makes 'host' a property with magic
		host = ""

		def __init__(self, /, address: ipaddress.IPv4Address, **kwargs: Any):
			super().__init__(**kwargs)
			self._dns_host = str(address)


class _HTTPSConnectionPool(connectionpool.HTTPSConnectionPool):

	class ConnectionCls(connection.HTTPSConnection, _HTTPConnectionPool.ConnectionCls):
		...
