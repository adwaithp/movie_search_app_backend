FROM python:3.9
#environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#the working directory
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
