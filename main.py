from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my api!!!"}

@app.get("/feeds")
def feeds():
    return {"Feeds" : "Here is a list of feeds"}