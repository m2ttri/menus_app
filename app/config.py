from pydantic.v1 import BaseSettings, root_validator


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    DB_HOST_TEST: str
    DB_PORT_TEST: int
    DB_USER_TEST: str
    DB_PASS_TEST: str
    DB_NAME_TEST: str

    @root_validator
    def get_database_url(cls, v):
        v['DATABASE_URL'] = (
            f"postgresql+asyncpg://"  # noqa: E231
            f"{v['DB_USER']}:{v['DB_PASS']}@"  # noqa: E231
            f"{v['DB_HOST']}:{v['DB_PORT']}/"  # noqa: E231
            f"{v['DB_NAME']}"  # noqa: E231
        )
        v['TEST_DATABASE_URL'] = (
            f"postgresql+asyncpg://"  # noqa: E231
            f"{v['DB_USER_TEST']}:{v['DB_PASS_TEST']}@"  # noqa: E231
            f"{v['DB_HOST_TEST']}:{v['DB_PORT_TEST']}/"  # noqa: E231
            f"{v['DB_NAME_TEST']}"  # noqa: E231
        )
        return v

    class Config:
        env_file = '.env'


settings = Settings()
