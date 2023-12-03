FROM python:3.11.0
WORKDIR /admin-api
COPY requirements.txt .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt
COPY . .
CMD ["python", "admin-service.py"]
EXPOSE 3000