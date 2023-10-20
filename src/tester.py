from jose import JWTError, jwt


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

token = 'eJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyNzc3QGV4YW1wbGUuY29tIiwiZXhwIjoxNjk3ODE1MzkzfQ.h_g1JN2C7hqK6WqnXbMxdCssuEPkY2mkX3hkWf1kCfc'

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

except JWTError:
    print("hllo world")