FROM python:3.10-slim
WORKDIR /scorexpert
COPY requirements.txt /scorexpert/
RUN pip install -r requirements.txt
COPY . /scorexpert/
EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
