from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
     return {"message": "Label Verifier API is running"}