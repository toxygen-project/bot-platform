FROM ubuntu:16.04

RUN apt-get update && \
apt-get install build-essential libtool autotools-dev automake checkinstall cmake check git yasm libsodium-dev libopus-dev libvpx-dev pkg-config -y && \
git clone https://github.com/ingvar1995/toxcore.git --branch=ngc_rebase && \
cd toxcore && mkdir _build && cd _build && \
cmake .. && make && make install

RUN cd ~ && apt-get install python3 python3-setuptools -y && \
git clone https://github.com/toxygen-project/bot-platform.git && \
cd bot-platform && python3 setup.py install

EXPOSE 443/tcp 443/udp 3389/tcp 3389/udp 33445/tcp 33445/udp 33446/tcp 33446/udp

CMD ["toxbot"]
