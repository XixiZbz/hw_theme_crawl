FROM python:2.7.15



ADD ./myapp /usr/src/app/

WORKDIR /usr/src/app/qc_cmq_python_sdk_V1.0.4/qc_cmq_python_sdk_V1.0.4/qc_cmq_python_sdk/sample/





RUN pip install requests -i https://pypi.mirrors.ustc.edu.cn/simple/

# ENTRYPOINT ["python","cmq_monitor.py"]
CMD ["python",'cmq_monitor.py']


#CMD [python /usr/src/app/qc_cmq_python_sdk_V1.0.4/qc_cmq_python_sdk_V1.0.4/qc_cmq_python_sdk/sample/cmq_monitor.py && /bin/bash ]
