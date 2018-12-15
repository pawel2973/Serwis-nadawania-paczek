# docker image
FROM python:3.6.6

# Umożliwia natychmiastowe zgłaszanie komunikatów do strumienia zamiast buforowania.
# Jest to przydatne do unikania sytuacji, w których aplikacja ulega awarii bez emitowania odpowiedniego komunikatu z powodu "zablokowania" komunikatu w buforze.
ENV PYTHONUNBUFFERED 1 

# Ustaw katalog roboczy
WORKDIR .

# Ma na celu dodanie katalogów i plików do systemu plików kontenera
COPY requirements.txt .

# Wykonuje polecenia 
RUN pip3 install -r requirements.txt
