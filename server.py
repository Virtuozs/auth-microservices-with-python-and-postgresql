import jwt, datetime, os
from flask import Flask, request
from flask_postgresql.PostgreSQL import PostgreSQL

server = Flask(__name__)

server.config["POSTGRESQL_HOST"] = os.environ.get("POSTGRES_HOST")
server.config["POSTGRESQL_DATABASE"] = os.environ.get("POSTGRES_DATABASE")
server.config["POSTGRESQL_USERNAME"] = os.environ.get("POSTGRES_USERNAME")
server.config["POSTGRESQL_PASSWORD"] = os.environ.get("POSTGRES_PASSWORD")
server.config["POSTGRESQL_PORT"] = os.environ.get("POSTGRES_PORT")

db = PostgreSQL(server).conn

@server.route('/login', methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401
    
    with db.connect() as conn:    
        result = conn.execute("SELECT email, password FROM users WHERE email=%s", (auth.username, ))
        res = [i for i in result]
        # return res[0]["email"], 200
        if (len(res) > 0):
            user_row = res[0]
            email = user_row["email"]
            password = user_row["password"]

            if auth.username != email or auth.password != password:
                return "invalid credentials", 401
            else:
                return createJWT(auth.username, os.environ.get("JWT_SECRET"))
        else:
            return "invalid credentials", 401
        
@server.route('/validate', methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
    except Exception as e:
        return str(e), 403
    
    return decoded, 200

def time_to_int(dateobj):
    total = int(dateobj.strftime('%S'))
    total += int(dateobj.strftime('%M')) * 60
    total += int(dateobj.strftime('%H')) * 60 * 60
    total += (int(dateobj.strftime('%j')) - 1) * 60 * 60 * 24
    total += (int(dateobj.strftime('%Y')) - 1970) * 60 * 60 * 24 * 365
    return total

def createJWT(username, secret):
    exp = datetime.datetime.now() + datetime.timedelta(days=1)
    # return str(exp.timestamp()), 200
    return jwt.encode(
        {
            "username": username,
            "exp": int(exp.timestamp()),
            "iat": int(datetime.datetime.utcnow().timestamp())
        },
        key=secret,
        algorithm="HS256",
    )

if __name__ == "__main__":
    print(server.config["POSTGRESQL_PASSWORD"])
    server.run(host="0.0.0.0", port=5000)