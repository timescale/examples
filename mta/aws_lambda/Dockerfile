FROM amazonlinux
RUN yum -y install git \
    python37 \
    python37-devel \
    python37-pip \
    zip \
    postgresql \
    gcc \
    && yum clean all
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install boto3
