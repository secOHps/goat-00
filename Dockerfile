FROM artifactory.dso.mtsi-va.com/shared-docker/dso/containers/python-3.11:3.11.2

WORKDIR /home

COPY ./src .

RUN pip3 install --no-cache-dir pip==24.0
