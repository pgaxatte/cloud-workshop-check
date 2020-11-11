FROM python:3.8-slim as builder

COPY . /app
WORKDIR /app
RUN python setup.py bdist_wheel

FROM python:3.8-slim
COPY --from=builder /app/dist/cloud_workshop_check-0.1.0-py3-none-any.whl /app/cloud_workshop_check-0.1.0-py3-none-any.whl

RUN pip install /app/cloud_workshop_check-0.1.0-py3-none-any.whl
#CMD ["waitress-serve", "--call", "cloud-workshop-check"]
CMD ["python", "-m", "cloud-workshop-check"]
