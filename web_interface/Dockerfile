FROM python:3.10-slim
WORKDIR /db_access
COPY requirements.txt /db_access
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /db_access
EXPOSE 8000
CMD ["python","/db_access/run_webaccess.py"]