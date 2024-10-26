FROM python:3.12.6

COPY /requirements.txt requirements.txt 

RUN pip install -r requirements.txt
RUN python3 

COPY /src /src

EXPOSE 7860

CMD ["python", "src/app.py"]