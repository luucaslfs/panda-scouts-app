from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/confrontos")
async def root():
    league_ids = [39, 10]
    return {"ligas": "premier, bundesliga, laliga, seriea, ligue1"}
