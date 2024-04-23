from common import *

app = FastAPI()


@app.get('/three')
def run_program():
    Stamp('Request to renew accepted', 'i')
    for name in ('graphs', 'stencil', 'search'):
        if not AddToDatabase(name, PATH_DB + 'active.txt', True):
            Stamp(f'{name} check passed', 's')
            thread = Thread(target=subprocess.run, args=(['python', '-m', f'{name}.main'],), kwargs={'check': False})
            thread.start()
            Stamp(f'Thread was given to {name}', 'b')
            while thread.is_alive():
                time.sleep(1)
            RemoveFromDatabase(name, PATH_DB + 'active.txt')
            Stamp(f'Process  {name} is finished', 'b')
        else:
            Stamp(f'Check {name} failed, program is already running', 'e')
            return {'message': f'Program {name} is already running'}
    return {'message': 'All programs executed successfully'}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
