FROM python:3.8.12-slim

COPY requirements_prod.txt requirements.txt
RUN pip install -r requirements.txt

COPY cardano_crystal_ball cardano_crystal_ball
COPY setup.py setup.py
RUN pip install .

COPY Makefile Makefile

CMD uvicorn cardano_crystal_ball.api.fast:app --host 0.0.0.0 --port $PORT
