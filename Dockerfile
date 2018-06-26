FROM alpine:3.7

RUN apk --no-cache add py2-pip py2-paramiko openssh-client openssl && \
    pip install --no-cache-dir ansible==2.5.5 boto boto3 pywinrm pyopenssl && \
    mkdir ~/.ssh

COPY ./ demokit

WORKDIR /demokit

ENTRYPOINT ["python", "demokit.py"]
