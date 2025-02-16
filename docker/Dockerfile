FROM condaforge/miniforge3

WORKDIR /app/
COPY . /app/
RUN bash /app/conda_env.sh

EXPOSE 7860
CMD ["bash", "/app/run.sh"]