from pathlib import Path
from typing import Iterator

from pglift import postgresql, roles
from pglift.ctx import Context
from pglift.models import interface, system

from . import reconfigure_instance, role_in_pgpass


def test_instance_port_changed(
    ctx: Context,
    passfile: Path,
    instance_manifest: interface.Instance,
    instance: system.Instance,
    tmp_port_factory: Iterator[int],
) -> None:
    """Check that change of instance port is reflected in password file
    entries.
    """
    role1, role2, role3 = (
        interface.Role(name="r1", password="1", pgpass=True),
        interface.Role(name="r2", password="2", pgpass=True),
        interface.Role(name="r3", pgpass=False),
    )
    surole = instance_manifest.surole(ctx.settings)
    assert ctx.settings.postgresql.surole.pgpass
    assert postgresql.is_running(ctx, instance)
    roles.apply(ctx, instance, role1)
    roles.apply(ctx, instance, role2)
    roles.apply(ctx, instance, role3)
    port = instance.port
    assert role_in_pgpass(passfile, role1, port=port)
    assert role_in_pgpass(passfile, role2, port=port)
    assert not role_in_pgpass(passfile, role3)
    assert role_in_pgpass(passfile, surole, port=port)
    newport = next(tmp_port_factory)
    with reconfigure_instance(ctx, instance_manifest, port=newport):
        assert not role_in_pgpass(passfile, role1, port=port)
        assert role_in_pgpass(passfile, role1, port=newport)
        assert not role_in_pgpass(passfile, role2, port=port)
        assert role_in_pgpass(passfile, role2, port=newport)
        assert not role_in_pgpass(passfile, role3)
        assert not role_in_pgpass(passfile, surole, port=port)
        assert role_in_pgpass(passfile, surole, port=newport)
