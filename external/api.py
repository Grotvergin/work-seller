from common import *

app = FastAPI()


@app.get('/renew')
def run_program():
    if AddToDatabase('external', PATH_DB + 'active.txt', True):
        thread = Thread(target=subprocess.run, args=(['python', '-m', 'external.main'],), kwargs={'check': False})
        thread.start()
        while thread.is_alive():
            time.sleep(1)
        RemoveFromDatabase('external', PATH_DB + 'active.txt')
        return {'message': 'Program executed successfully'}
    return {'message': 'Program is already running'}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
