
# libraries

FROM python:3.11-slim

#ENV_Variables

ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app



COPY model_requirements.txt .
RUN pip install --no-cache-dir --default-timeout=5000 -r model_requirements.txt

# get acess to API codes

COPY Data-API/ $APP_HOME/
WORKDIR $APP_HOME

# download MNIST only in build time. Not In every Run
RUN python -c "from torchvision import datasets, transforms; \
    datasets.MNIST(root='./data', train=True, download=True); \
    datasets.MNIST(root='./data', train=False, download=True)"

# make ready start.sh file for to be runned
RUN chmod +x start.sh

# define posrts for container
EXPOSE 8000
EXPOSE 8001

# run APIs together

CMD ["./start.sh"]
