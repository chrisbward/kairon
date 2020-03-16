FROM rasa/rasa:1.8.1-full

SHELL ["/bin/bash", "-c"]

ENV RASA_NLU_DOCKER="YES" \
    RASA_NLU_HOME=/app \
    RASA_NLU_PYTHON_PACKAGES=/usr/local/lib/python3.6/dist-packages

WORKDIR ${RASA_NLU_HOME}

USER root
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install pyyaml
RUN python3 -m pip install nest_asyncio
RUN python3 -m pip install gensim
RUN python3 -m pip install sentence_transformers
RUN python3 -m pip install autocorrect
RUN python3 -m pip install Quart
RUN python3 -m pip install Quart-CORS
RUN mkdir ssl
USER 1001

COPY . ${RASA_NLU_HOME}

RUN rasa train

EXPOSE 5005

ENTRYPOINT["hypercorn", "-w", 2", "flaskblog:app"]
