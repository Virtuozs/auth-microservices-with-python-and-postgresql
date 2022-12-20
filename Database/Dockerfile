FROM postgres:13.9-alpine

# ENV POSTGRES_USER=auth1
# ENV POSTGRES_DB=auth
ENV POSTGRES_PASSWORD=password
COPY init.sql /docker-entrypoint-initdb.d/init.sql

# CMD [ "psql", "postgres://auth1:password@localhost:5432/auth"] \
#     && INSERT INTO users (id, email, password) VALUES (DEFAULT, 'test@mail.com', 'password');