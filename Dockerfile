FROM ghcr.io/raw-labs/mxcp:0.10.0-rc12

COPY --chown=mxcp:mxcp . /mxcp-site/

WORKDIR /mxcp-site

# Excel ingestion dependency for dbt Python models
RUN python -m pip install --no-cache-dir openpyxl

ENV MXCP_CONFIG=/mxcp-site/mxcp-config.yml
