from fastapi import Body, FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my api!!!"}

@app.get("/feeds")
def feeds():
    return {"Feeds" : "Here is a list of feeds"}

@app.post("/createfeed")
def create_feed(payload: dict = Body(...)):
    print(payload)
    return{"new feed": f"feed title: {payload['title']}, content: {payload['content']}"}