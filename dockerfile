FROM python:3.6.9-slim-buster

ENV ENV=production

WORKDIR /src
COPY . .
COPY ./requirements.txt .

RUN apt-get update \
 && apt-get install -y \
 --no-install-recommends \
 --no-install-suggests \
 curl gcc g++ gnupg unixodbc-dev \
 unixodbc-dev \
 libgssapi-krb5-2 && \
 apt-get autoclean && \
 apt-get autoremove && \
 curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
 curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
 apt-get update && \
 ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
 ACCEPT_EULA=Y apt-get install -y mssql-tools && \
 echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile && \
 echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc && \
 pip install --upgrade pip
 
RUN pip install -r requirements.txt && rm requirements.txt

CMD ["python", "main.py"]
