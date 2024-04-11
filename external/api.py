from common import *

app = FastAPI()


@app.get('/renew')
def run_program():
    Stamp('Request to renew accepted', 'i')
    if AddToDatabase('external', PATH_DB + 'active.txt', True):
        Stamp('Check passed, starting renew', 's')
        thread = Thread(target=subprocess.run, args=(['python', '-m', 'external.main'],), kwargs={'check': False})
        thread.start()
        Stamp('Thread was given', 'b')
        while thread.is_alive():
            Stamp('Process is alive', 'i')
            time.sleep(1)
        Stamp('Process is finished', 'b')
        RemoveFromDatabase('external', PATH_DB + 'active.txt')
        return {'message': 'Program executed successfully'}
    return {'message': 'Program is already running'}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
