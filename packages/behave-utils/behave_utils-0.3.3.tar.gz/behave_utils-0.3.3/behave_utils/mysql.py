#  Copyright 2021, 2022  Dominik Sekotill <dom.sekotill@kodo.org.uk>
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Management and control for MySQL database fixtures
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING
from typing import Iterator
from typing import Sequence

from behave import fixture

from .docker import Cli
from .docker import Container
from .docker import Image
from .docker import Mount
from .docker import Network
from .secret import make_secret
from .utils import wait

if TYPE_CHECKING:
	from behave.runner import FeatureContext


INIT_DIRECTORY = Path("/docker-entrypoint-initdb.d")


class Mysql(Container):
	"""
	Container subclass for a database container
	"""

	def __init__(
		self,
		version: str = "latest",
		init_files: Sequence[Path] = [],
		network: Network|None = None,
		name: str = "test-db",
		user: str = "test-db-user",
		password: str|None = None,
	):
		self.name = name
		self.user = user
		self.password = password or make_secret(20)
		volumes: list[Mount] = [(path, INIT_DIRECTORY / path.name) for path in init_files]
		volumes.append(Path("/var/lib/mysql"))
		env = dict(
			MYSQL_DATABASE=name,
			MYSQL_USER=user,
			MYSQL_PASSWORD=self.password,
		)
		Container.__init__(
			self,
			Image.pull(f"mysql/mysql-server:{version}"),
			volumes=volumes,
			env=env,
			network=network,
		)

	def get_location(self) -> str:
		"""
		Return a "host:port" string for connecting to the database from other containers
		"""
		host = self.inspect().path("$.Config.Hostname", str)
		return f"{host}:3306"

	@property
	def mysql(self) -> Cli:
		"""
		Run "mysql" commands
		"""
		return Cli(self, "mysql")

	@property
	def mysqladmin(self) -> Cli:
		"""
		Run "mysqladmin" commands
		"""
		return Cli(self, "mysqladmin")

	@property
	def mysqldump(self) -> Cli:
		"""
		Run "mysqldump" commands
		"""
		return Cli(self, "mysqldump")

	@contextmanager
	def started(self) -> Iterator[Container]:
		"""
		Return a context manager that only enters once the database is initialised
		"""
		with self:
			self.start()
			sleep(20)
			wait(lambda: self.run(['/healthcheck.sh']).returncode == 0)
			yield self


@fixture
def snapshot_rollback(context: FeatureContext, /, database: Mysql|None = None) -> Iterator[None]:
	"""
	Manage the state of a database as a revertible fixture

	At the end of the fixture's lifetime it's state at the beginning is restored.  This
	allows for faster fixture turn-around than restarting the database.
	"""
	assert database is not None, \
		"'database' is required for snapshot_rollback"
	snapshot = database.mysqldump("--all-databases", deserialiser=bytes)
	yield
	database.mysql(input=snapshot)
