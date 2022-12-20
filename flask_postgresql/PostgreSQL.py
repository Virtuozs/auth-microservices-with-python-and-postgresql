from sqlalchemy import create_engine

class PostgreSQL:
    def __init__(self, server):
        self.host = server.config["POSTGRESQL_HOST"] 
        self.user = server.config["POSTGRESQL_USERNAME"] 
        self.password = server.config["POSTGRESQL_PASSWORD"] 
        self.database = server.config["POSTGRESQL_DATABASE"] 
        self.port = server.config["POSTGRESQL_PORT"]
        self.string_conn = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.conn = create_engine(self.string_conn)

            