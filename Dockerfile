FROM python:3
RUN pip install boto3 aiohttp asyncio
WORKDIR /app
ADD src /app/src
CMD [ "python", "/app/src/main.py" ]