from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/renew')
def run_program():
    return {"message": "Program started"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
