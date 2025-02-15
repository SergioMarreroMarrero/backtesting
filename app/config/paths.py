from pathlib import Path


class ProjectPaths:
    BASE = Path(__file__).resolve().parent.parent.parent
    APP = BASE / "app"
    DATA = BASE / "data"
    LOGS = BASE / "logs"
    CONFIG = APP / "config"
    CONFIG_YAML = CONFIG / "yaml"

    @classmethod
    def ensure_dirs(cls):
        for path in [cls.DATA, cls.LOGS]:
            path.mkdir(parents=True, exist_ok=True)


ProjectPaths.ensure_dirs()


class ProjectFiles:

    @classmethod
    def h5(cls, exchange='binance'):
        return ProjectPaths.DATA / f"{exchange}.h5"

    @classmethod
    def app_log(cls):
        return ProjectPaths.LOGS / "app.log"

    @classmethod
    def config_yaml(clsc, file_name):
        return ProjectPaths.CONFIG_YAML / f"{file_name}.yaml"
