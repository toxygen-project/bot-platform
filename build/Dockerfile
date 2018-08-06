FROM ubuntu:16.04

RUN apt-get update && \
apt-get install python3.6 build-essential libtool autotools-dev automake checkinstall cmake check git yasm libsodium-dev libopus-dev libvpx-dev pkg-config -y && \
git clone https://github.com/ingvar1995/toxcore.git --branch=ngc_rebase && \
cd toxcore && mkdir _build && cd _build && \
cmake .. && make && make install && \
cd ~ && \
git clone https://github.com/toxygen-project/bot-platform.git && \
cd bot-platform && python3 setup.py

RUN useradd -ms /bin/bash toxbot
USER toxbot

CMD ["toxbot"]
