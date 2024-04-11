from fastapi import FastAPI


def Main() -> None:
    @app.get('/renew')
    def run_program():
        return {"message": "Program started"}


if __name__ == '__main__':
    app = FastAPI()
    Main()
