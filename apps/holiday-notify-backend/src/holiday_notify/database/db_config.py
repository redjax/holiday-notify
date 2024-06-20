from typing import Union
from dynaconf import Dynaconf
from pydantic import Field, field_validator, ValidationError
from pydantic_settings import BaseSettings

import sqlalchemy as sa
import sqlalchemy.orm as so

valid_db_types: list[str] = ["sqlite", "postgres", "mssql"]

DYNACONF_DB_SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="DB",
    settings_files=["db/settings.toml", "db/.secrets.toml"],
)


class DBSettings(BaseSettings):
    type: str = Field(default=DYNACONF_DB_SETTINGS.DB_TYPE, env="DB_TYPE")
    drivername: str = Field(
        default=DYNACONF_DB_SETTINGS.DB_DRIVERNAME, env="DB_DRIVERNAME"
    )
    username: str | None = Field(
        default=DYNACONF_DB_SETTINGS.DB_USERNAME, env="DB_USERNAME"
    )
    password: str | None = Field(
        default=DYNACONF_DB_SETTINGS.DB_PASSWORD, env="DB_PASSWORD", repr=False
    )
    host: str | None = Field(default=DYNACONF_DB_SETTINGS.DB_HOST, env="DB_HOST")
    port: Union[str, int, None] = Field(
        default=DYNACONF_DB_SETTINGS.DB_PORT, env="DB_PORT"
    )
    database: str = Field(default=DYNACONF_DB_SETTINGS.DB_DATABASE, env="DB_DATABASE")
    echo: bool = Field(default=DYNACONF_DB_SETTINGS.DB_ECHO, env="DB_ECHO")

    @field_validator("port")
    def validate_db_port(cls, v) -> int:
        if v is None or v == "":
            return None
        elif isinstance(v, int):
            return v
        elif isinstance(v, str):
            return int(v)
        else:
            raise ValidationError

    def get_db_uri(self) -> sa.URL:
        try:
            _uri: sa.URL = sa.URL.create(
                drivername=self.drivername,
                username=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
            )

            return _uri

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting SQLAlchemy database URL. Details: {exc}"
            )
            raise msg

    def get_engine(self) -> sa.Engine:
        assert self.get_db_uri() is not None, ValueError("db_uri is not None")
        assert isinstance(self.get_db_uri(), sa.URL), TypeError(
            f"db_uri must be of type sqlalchemy.URL. Got type: ({type(self.db_uri)})"
        )

        try:
            engine: sa.Engine = sa.create_engine(
                url=self.get_db_uri().render_as_string(hide_password=False),
                echo=self.echo,
            )

            return engine
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting database engine. Details: {exc}"
            )

            raise msg

    def get_session_pool(self) -> so.sessionmaker[so.Session]:
        engine: sa.Engine = self.get_engine()
        assert engine is not None, ValueError("engine cannot be None")
        assert isinstance(engine, sa.Engine), TypeError(
            f"engine must be of type sqlalchemy.Engine. Got type: ({type(engine)})"
        )

        session_pool: so.sessionmaker[so.Session] = so.sessionmaker(bind=engine)

        return session_pool


db_settings: DBSettings = DBSettings()
