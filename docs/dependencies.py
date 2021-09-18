from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException

async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


# @app.get("/items/")
# async def read_items(commons=Depends(CommonQueryParams)):
#     response = {}
#     if commons.q:
#         response.update({"q": commons.q})
#     items = fake_items_db[commons.skip : commons.skip + commons.limit]
#     response.update({"items": items})
#     return response

# @app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
@app.get("/items/")
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

    
@app.get("/users/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

if __name__ == "__main__":
    import uvicorn
    import os
    file_name = os.path.basename(__file__)[:-3]
    uvicorn.run(file_name + ":app", host="0.0.0.0", port=8000, reload=True)