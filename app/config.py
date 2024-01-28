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
            f'postgresql+asyncpg://'
            f'{v["DB_USER"]}:{v["DB_PASS"]}@'
            f'{v["DB_HOST"]}:{v["DB_PORT"]}/'
            f'{v["DB_NAME"]}'
        )
        v['TEST_DATABASE_URL'] = (
            f'postgresql+asyncpg://'
            f'{v["DB_USER_TEST"]}:{v["DB_PASS_TEST"]}@'
            f'{v["DB_HOST_TEST"]}:{v["DB_PORT_TEST"]}/'
            f'{v["DB_NAME_TEST"]}'
        )
        return v

    class Config:
        env_file = ".env"


settings = Settings()
