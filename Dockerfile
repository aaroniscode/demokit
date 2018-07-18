FROM alpine:3.8

RUN apk --no-cache add py2-pip py2-bcrypt py2-cryptography py-pynacl openssh-client openssl && \
    pip install --no-cache-dir ansible==2.6.0 boto boto3 pyopenssl==17 pywinrm && \
    mkdir ~/.aws && mkdir ~/.ssh

COPY ./ demokit

WORKDIR /demokit

ENTRYPOINT ["python", "demokit.py"]
