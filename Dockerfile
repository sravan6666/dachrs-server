FROM python:3.9

WORKDIR /usr/kanban
RUN mkdir -p data

#RUN apk update
#RUN apk add build-base

#RUN gcc --version

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install azure-identity
#RUN pip install azure-keyvault-secrets
#RUN pip install azure-storage-blob

COPY . .

EXPOSE 5000
CMD [ "flask", "run", "--host=0.0.0.0" ]