FROM apache/airflow:2.10.2
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
         android-tools-adb \
         android-tools-fastboot \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /

EXPOSE 5037

USER airflow
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
