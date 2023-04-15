
# taery/oleg-base
#!/bin/bash
FROM python:3.8

WORKDIR /hyper_hackaton

# Copy project files
COPY /bot_core/ /hyper_hackaton/bot_core/
#COPY /data/ /hyper_hackaton/data/
COPY main.py /hyper_hackaton/main.py

# Install python requirements
COPY requirements.txt /hyper_hackaton/requirements.txt
RUN pip install -r /hyper_hackaton/requirements.txt

CMD ["python", "./main.py"]