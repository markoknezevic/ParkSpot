FROM postgres:17-alpine AS vector-build

ARG PGVECTOR_VERSION=0.8.2
RUN apk add --no-cache build-base git \
    && git clone --depth 1 --branch "v${PGVECTOR_VERSION}" https://github.com/pgvector/pgvector.git /tmp/pgvector \
    && make -C /tmp/pgvector OPTFLAGS="" with_llvm=no \
    && make -C /tmp/pgvector install with_llvm=no

FROM postgres:17-alpine

COPY --from=vector-build /usr/local/lib/postgresql/vector.so /usr/local/lib/postgresql/
COPY --from=vector-build /usr/local/share/postgresql/extension/vector* /usr/local/share/postgresql/extension/
