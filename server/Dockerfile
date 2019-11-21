FROM python:3.6
ENV PYTHONUNBUFFERED=1
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "--worker-tmp-dir", "/dev/shm", "--workers=1", "--threads=4", "--worker-class=gthread", "-b", "0.0.0.0:8000", "app", "--enable-stdio-inheritance" , "--reload"]