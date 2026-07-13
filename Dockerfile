FROM python:3.14

WORKDIR /code

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src/ai_knowledge_assistant /code/ai_knowledge_assistant

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

