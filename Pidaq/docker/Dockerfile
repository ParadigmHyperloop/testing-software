FROM raspbian/stretch:latest

LABEL build-date="2020-03-01" \
      name="Raspi + Clang for xcompiling" 

RUN sudo apt update -y && \
    sudo apt upgrade -y

RUN sudo apt-get install -y \
    git \
    make \
    curl \
    xz-utils \
    libstdc++6-4.6-dev

RUN cd ~ && \ 
    wget http://releases.llvm.org/9.0.0/clang+llvm-9.0.0-armv7a-linux-gnueabihf.tar.xz && \
    tar -xvf clang+llvm-9.0.0-armv7a-linux-gnueabihf.tar.xz && \
    rm clang+llvm-9.0.0-armv7a-linux-gnueabihf.tar.xz && \
    mv clang+llvm-9.0.0-armv7a-linux-gnueabihf clang_9.0.0 && \
    sudo mv clang_9.0.0 /usr/local && \
    echo 'export PATH=/usr/local/clang_9.0.0/bin:$PATH' >> ~/.bashrc && \
    echo 'export LD_LIBRARY_PATH=/usr/local/clang_9.0.0/lib:$LD_LIBRARY_PATH' >> ~/.bashrc && \
    . ~/.bashrc && \
    clang++ --version

COPY helloTest.sh /usr/local/bin

RUN sed -i.bak 's/\r$//' /usr/local/bin/helloTest.sh && \
    chmod +x /usr/local/bin/helloTest.sh

CMD /bin/bash