import pytest

from pglift import logrotate
from pglift.ctx import Context
from pglift.models import interface
from pglift.models.system import Instance
from pglift.settings import LogRotateSettings, Settings


@pytest.fixture
def logrotate_settings(settings: Settings) -> LogRotateSettings:
    assert settings.logrotate is not None
    return settings.logrotate


def test_site_configure(
    settings: Settings, logrotate_settings: LogRotateSettings
) -> None:
    assert not logrotate_settings.configdir.exists()
    logrotate.site_configure_install(settings)
    assert logrotate_settings.configdir.exists()
    logrotate.site_configure_uninstall(settings)
    assert not logrotate_settings.configdir.exists()


def test_instance_configure(
    ctx: Context, instance: Instance, instance_manifest: interface.Instance
) -> None:
    logrotate.instance_configure(ctx=ctx, manifest=instance_manifest, creating=True)
    assert ctx.settings.logrotate is not None
    config = (
        ctx.settings.logrotate.configdir / f"{instance.version}-{instance.name}.conf"
    )
    assert config.exists()
    assert ctx.settings.pgbackrest is not None
    assert ctx.settings.patroni is not None
    assert config.read_text() == "\n".join(
        [
            f"{ctx.settings.pgbackrest.logpath}/*.log {{",
            "  weekly",
            "  rotate 10",
            "  copytruncate",
            "  delaycompress",
            "  compress",
            "  notifempty",
            "  missingok",
            "}",
            "",
            f"{ctx.settings.patroni.logpath}/*.log {{",
            "  weekly",
            "  rotate 10",
            "  copytruncate",
            "  delaycompress",
            "  compress",
            "  notifempty",
            "  missingok",
            "}",
            "",
            f"{instance.datadir}/log/*.log {{",
            "  weekly",
            "  rotate 10",
            "  copytruncate",
            "  delaycompress",
            "  compress",
            "  notifempty",
            "  missingok",
            "}",
            "",
        ]
    )

    # When not creating the instance, don't touch the file.
    config.unlink()
    logrotate.instance_configure(ctx=ctx, manifest=instance_manifest, creating=False)
    assert not config.exists()
    config.touch()

    logrotate.instance_drop(ctx=ctx, instance=instance)
    assert not config.exists()
