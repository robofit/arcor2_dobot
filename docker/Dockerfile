ARG version=latest
FROM arcor2/arcor2_base:$version

COPY ./arcor2_dobot /root/arcor2_fit_demo/arcor2_dobot
COPY ./docker /root/arcor2_fit_demo/docker

RUN cd /root \
	&& git clone https://github.com/ZdenekM/pydobot.git \
	&& cd pydobot \
	&& pip3 install -e ./


EXPOSE 6789
