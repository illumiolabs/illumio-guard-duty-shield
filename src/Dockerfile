FROM public.ecr.aws/lambda/python:3.8

COPY lambda_function.py ${LAMBDA_TASK_ROOT}

COPY requirements.txt  .

RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD [ "lambda_function.lambda_handler" ]
