FROM python:3.8
MAINTAINER MrFlava <thatelitemaili33t@gmail.com>

WORKDIR /FlaskTask
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /FlaskTask/
EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]