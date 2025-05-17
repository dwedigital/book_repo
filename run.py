
from app.config import SECRET_KEY, HOST, PORT

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
