FROM python:3.11
USER root

RUN pip install --upgrade pip
RUN pip install pipenv

WORKDIR /app

# Copy source code to working directory
COPY . .

RUN pipenv update && \
    pipenv run pip freeze > requirements.txt && \
    pip install -r requirements.txt && \
    rm requirements.txt

ENTRYPOINT ["python"]
CMD ["__main__.py"]