FROM python:3.8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./main.py /code/main.py

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code/app
#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

#
CMD ["pip list"]
CMD ["pytest", "--html", "report.html"]
ENTRYPOINT ["sh", "/tmp/entrypoint.sh" ]