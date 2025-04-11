FROM python:3.11-slim 
# base image for new docker image

WORKDIR /apicode
# working directory -- homebase for streamlit application 

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4000

CMD [ "python", "backend_app.py"]

