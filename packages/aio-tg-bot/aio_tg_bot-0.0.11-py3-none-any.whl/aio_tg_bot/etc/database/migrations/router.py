"""Migration router."""
import os
import re
import sys
import typing
import peewee
import pkgutil
import pathlib
import logging
import datetime
from unittest import mock
from types import ModuleType
from importlib import import_module

try:
    from functools import cached_property
except ImportError:
    from cached_property import cached_property

from .logger import LOGGER
from .migrator import Migrator
from aio_tg_bot.etc.conf import settings
from .auto import diff_many, NEWLINE
from aio_tg_bot.version import __version__
from .compat import string_types, exec_in
from aio_tg_bot.etc.database.models import MigrateHistory


CLEAN_RE = re.compile(r'\s+$', re.M)
CURDIR = os.getcwd()
UNDEFINED = object()
VOID = lambda m, d: None  # noqa
template_path = os.path.join(pathlib.Path(__file__).parent, "template.txt")


class BaseRouter(object):
    """Abstract base class for router."""

    def __init__(self, database, ignore=None, schema=None, logger=LOGGER, models="models"):
        """Initialize the router."""
        self.database = database
        self.schema = schema
        self.ignore = ignore
        self.logger = logger
        self.models = models
        if not isinstance(self.database, (peewee.Database, peewee.Proxy)):
            raise RuntimeError('Invalid database: %s' % database)

    @cached_property
    def model(self) -> typing.Type[MigrateHistory]:
        """Initialize and cache MigrationHistory model."""
        MigrateHistory._meta.database = self.database
        MigrateHistory._meta.schema = self.schema
        MigrateHistory.create_table(True)
        return MigrateHistory

    @property
    def todo(self):
        """Get migrations to run."""
        raise NotImplementedError

    @property
    def done(self):
        """Scan migrations in database."""
        if self.model.table_exists():
            query = self.model.select().where(self.model.module == self.module_name).order_by(self.model.id)
            dones =  [migration.name for migration in query]
        else:
            dones = []

        return dones

    @property
    def diff(self):
        """Calculate difference between fs and db."""
        done = set(self.done)
        return [name for name in self.todo if name not in done]

    @cached_property
    def migrator(self):
        """Create migrator and setup it with fake migrations."""
        migrator = Migrator(self.database)
        for name in self.done:
            self.run_one(name, migrator)
        return migrator

    def create(self, name='auto', auto=False):
        """Create a migration.
        :param auto: Python module path to scan for models.
        """
        migrate = rollback = ''
        if auto:
            # Need to append the CURDIR to the path for import to work.
            sys.path.append(CURDIR)
            try:
                modules = [auto]
                if isinstance(auto, bool):
                    modules = [m for _, m, ispkg in pkgutil.iter_modules([CURDIR]) if ispkg]

                models = [m for module in modules for m in get_models([import_module(self.models)])]

            except ImportError:
                return self.logger.error("Can't import models module: %s", auto)

            if self.ignore:
                models = [m for m in models if m._meta.name not in self.ignore]

            for migration in self.diff:
                self.run_one(migration, self.migrator, fake=True)

            migrate = compile_migrations(self.migrator, models)
            if not migrate:
                return self.logger.warn('No changes found.')

            rollback = compile_migrations(self.migrator, models, reverse=True)

        if "tg_bot" == self.module_name:
            name = "{}_tg_bot".format(name)

        self.logger.info('Creating migration "%s"', name)
        name = self.compile(name, migrate, rollback)
        self.logger.info('Migration has been created as "%s"', name)
        return name

    def merge(self, name='initial'):
        """Merge migrations into one."""
        migrator = Migrator(self.database)
        migrate = compile_migrations(migrator, self.migrator.orm.values())
        if not migrate:
            return self.logger.error("Can't merge migrations")

        self.clear()

        self.logger.info('Merge migrations into "%s"', name)
        rollback = compile_migrations(self.migrator, [])
        name = self.compile(name, migrate, rollback, 0)

        migrator = Migrator(self.database)
        self.run_one(name, migrator, fake=True, force=True)
        self.logger.info('Migrations has been merged into "%s"', name)

    def clear(self):
        """Clear migrations."""
        self.model.delete().execute()

    def compile(self, name, migrate='', rollback='', num=None):
        raise NotImplementedError

    def read(self, name):
        raise NotImplementedError

    def run_one(self, name, migrator, fake=True, downgrade=False, force=False):
        """Run/emulate a migration with given name."""
        try:
            migrate, rollback = self.read(name)
            if fake:
                cursor_mock = mock.Mock()
                cursor_mock.fetch_one.return_value = None
                with mock.patch('peewee.Model.select'):
                    with mock.patch('peewee.Database.execute_sql',
                                    return_value=cursor_mock):
                        migrate(migrator, self.database, fake=fake)

                if force:
                    self.model.create(name=name, module=self.module_name)
                    self.logger.info('Done %s', name)

                migrator.clean()
                return migrator

            with self.database.transaction():
                if not downgrade:
                    self.logger.info('Migrate "%s"', name)
                    migrate(migrator, self.database, fake=fake)
                    migrator.run()
                    self.model.create(name=name, module=self.module_name)
                else:
                    self.logger.info('Rolling back %s', name)
                    rollback(migrator, self.database, fake=fake)
                    migrator.run()
                    self.model.delete().where(self.model.name == name).execute()

                self.logger.info('Done %s', name)

        except Exception:
            self.database.rollback()
            operation = 'Migration' if not downgrade else 'Rollback'
            self.logger.exception('%s failed: %s', operation, name)
            raise

    def run(self, name=None, fake=False):
        """Run migrations."""
        self.logger.info('Starting migrations')

        done = []
        diff = self.diff
        if not diff:
            self.logger.info('There is nothing to migrate')
            return done

        migrator = self.migrator
        for mname in diff:
            self.run_one(mname, migrator, fake=fake, force=fake)
            done.append(mname)
            if name and name == mname:
                break

        return done

    def rollback(self, name):
        name = name.strip()
        done = self.done
        if not done:
            raise RuntimeError('No migrations are found.')
        if name != done[-1]:
            raise RuntimeError('Only last migration can be canceled.')

        migrator = self.migrator
        self.run_one(name, migrator, False, True)
        self.logger.warning('Downgraded migration: %s', name)


class Router(BaseRouter):
    filemask = re.compile(r"[\d]{3}_[^\.]+\.py$")

    def __init__(self, database, migrate_dir, module_name=None, **kwargs):
        super(Router, self).__init__(database, **kwargs)
        self.migrate_dir = migrate_dir
        self.module_name = module_name

    @property
    def todo(self):
        """Scan migrations in file system."""
        if not os.path.exists(self.migrate_dir):
            self.logger.warn('Migration directory: %s does not exist.', self.migrate_dir)
            os.makedirs(self.migrate_dir)
        return sorted(f[:-3] for f in os.listdir(self.migrate_dir) if self.filemask.match(f))

    def compile(self, name, migrate='', rollback='', num=None):
        """Create a migration."""
        if num is None:
            num = len(self.todo)

        name = '{:03}_'.format(num + 1) + name
        filename = name + '.py'
        path = os.path.join(self.migrate_dir, filename)

        need_modules = []
        for _migrate in [migrate, rollback]:
            for line in _migrate.split("\n"):
                if ".add_fields" in line:
                    function_params = line[line.index(".add_fields") + len(".add_fields") + 1:-1]
                    fields = function_params[function_params[1:].index("'") + 4:].split("), ")
                    for field in fields:
                        module = ".".join(field.split("(")[0].split("=")[1].split(".")[:-1])


                        if module not in need_modules:
                            need_modules.append(module)
                elif " = " in line and '"' not in line:
                    module = ".".join(line.split(" = ")[1][:line.index("(")].split(".")[:-1])
                    if module not in need_modules and "" != module:
                        need_modules.append(module)

        imports_in_str = "\n".join(["import {}".format(module) for module in need_modules])
        date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

        with open(template_path) as t:
            MIGRATE_TEMPLATE = t.read()

        text = MIGRATE_TEMPLATE.format(migrate=migrate, rollback=rollback,
                                       imports=imports_in_str, version=__version__, date=date)

        with open(path, 'w') as f:
            f.write(text)

        return name

    def read(self, name):
        """Read migration from file."""
        call_params = dict()
        if os.name == 'nt' and sys.version_info >= (3, 0):
            # if system is windows - force utf-8 encoding
            call_params['encoding'] = 'utf-8'

        migration_file = "{}.py".format(name)

        if name.endswith("tg_bot"):
            # Если миграция для библиотеки
            migration_path = os.path.join(pathlib.Path(__file__).parent.parent.parent, "migrations", migration_file)
        else:
            migration_path = os.path.join(self.migrate_dir, migration_file)

        with open(migration_path, **call_params) as f:
            code = f.read()
            scope = {}
            exec_in(code, scope)
            return scope.get('migrate', VOID), scope.get('rollback', VOID)

    def clear(self):
        """Remove migrations from fs."""
        super(Router, self).clear()
        for name in self.todo:
            filename = os.path.join(self.migrate_dir, name + '.py')
            os.remove(filename)


class ModuleRouter(BaseRouter):

    def __init__(self, database, migrate_module='migrations', **kwargs):
        """Initialize the router."""
        super(ModuleRouter, self).__init__(database, **kwargs)

        if isinstance(migrate_module, str):
            migrate_module = import_module(migrate_module)

        self.migrate_module = migrate_module

    def read(self, name):
        """Read migrations from a module."""
        mod = getattr(self.migrate_module, name)
        return getattr(mod, 'migrate', VOID), getattr(mod, 'rollback', VOID)


def load_models(module):
    """Load models from given module."""
    modules = _import_submodules(module)
    return get_models(modules)


def get_models(modules):
    return {m for module in modules for m in filter(
        _check_model, (getattr(module, name) for name in dir(module))
    )}

def _import_submodules(package, passed=UNDEFINED):
    if passed is UNDEFINED:
        passed = set()

    if isinstance(package, str):
        package = import_module(package)

    modules = []

    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
        if name in passed:
            continue
        passed.add(name)

        module = sys.modules.get(name)
        if module is None:
            module = loader.find_module(name).load_module(name)

        modules.append(module)
        if is_pkg:
            modules += _import_submodules(module, passed=passed)

    return modules


def _check_model(obj, models=None):
    """Checks object if it's a peewee model and unique."""
    return isinstance(obj, type) and issubclass(obj, peewee.Model) and hasattr(obj, '_meta')


def compile_migrations(migrator, models, reverse=False):
    """Compile migrations for given models."""
    source = migrator.orm.values()
    if reverse:
        source, models = models, source

    migrations = diff_many(models, source, migrator, reverse=reverse)
    if not migrations:
        return False

    migrations = NEWLINE + NEWLINE.join('\n\n'.join(migrations).split('\n'))
    return CLEAN_RE.sub('\n', migrations)
