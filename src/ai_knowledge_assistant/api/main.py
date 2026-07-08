from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {'Hello':'World'}


@app.get('/health')
def health():
    return {'status':'ok'}
