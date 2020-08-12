ARG version=latest
FROM arcor2/arcor2_base:$version

COPY ./ /root/arcor2_fit_demo/



RUN cd /root \
	&& git clone https://github.com/ZdenekM/pydobot.git \
	&& cd pydobot \
	&& pip3 install -e ./

RUN cd /root/arcor2_fit_demo/ \
	&& pip3 install -e .  


CMD ["python", "/root/arcor2_fit_demo/arcor2_fit_demo/object_types/upload.py", "/bin/sh", "arcor2_upload_builtin_objects"] 

