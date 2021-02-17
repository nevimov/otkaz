# REF: https://docs.docker.com/engine/reference/builder/
# BP: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

# The "Node" image includes both Node.js and Python (v3.7.3)
FROM node:12.18.2-buster

# The Node image has a non-root user 'node'. However, for Linux, this user's
# GID/UID must match your local user UID/GID to avoid permission issues with
# bind mounts. Update USER_UID / USER_GID if yours is not 1000.
# See https://aka.ms/vscode-remote/containers/non-root-user.
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV PROJECT_ROOT_DIR=/workspace

# Fix "Warning: Unable to set locale. Expect encoding problems."
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8


# Install Debian packages.

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    && apt-get install --assume-yes \
        #
        # Install packages important for CLI installs
        procps \
        sudo \
        #
        # python3-dev is required to build Psycopg from source
        python3-dev \
        python3-pip \
        #
        # gettext is required to compile translation message files
        gettext \
    #
    # Install Dart Sass's stand-alone executable (faster than the JS version)
    && export SASS_VERSION=1.26.10 \
    && export SASS_ARCHIVE=dart-sass-${SASS_VERSION}-linux-x64.tar.gz \
    && cd /usr/local/bin \
    && wget --progress=dot --quiet \
    "https://github.com/sass/dart-sass/releases/download/$SASS_VERSION/$SASS_ARCHIVE" \
    # Extract the archive without the root folder
    && tar -xf  "$SASS_ARCHIVE" --strip-components=1 \
    && rm "$SASS_ARCHIVE" \
    #
    # Remove APT cache and package lists to reduce disk space occupied by the container
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=


# Set up a non-root user
RUN if [ "$USER_GID" != "1000" ]; then groupmod node --gid $USER_GID; fi \
    && if [ "$USER_UID" != "1000" ]; then usermod --uid $USER_UID node; fi \
    # [Optional] Don't ask the non-root user for password when using sudo
    && echo node ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/node \
    && chmod 0440 /etc/sudoers.d/node


RUN mkdir -p "$PROJECT_ROOT_DIR" \
    && chown $USER_UID:$USER_GID "$PROJECT_ROOT_DIR"
WORKDIR $PROJECT_ROOT_DIR


# Install Pip packages
COPY pip-common.txt pip-dev.txt ./
RUN  pip3 install --no-cache-dir --upgrade pip \
     && python3 -m pip install --no-cache-dir --requirement pip-dev.txt


# Install Node packages
USER $USER_UID:$USER_GID
COPY package*.json ./
RUN npm install && npm cache clean --force --loglevel=error


# Expose a port for Django development server
EXPOSE 80 8001 8002

CMD ["sleep", "infinity"]
