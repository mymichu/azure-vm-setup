#################### Build-System Image ####################
FROM ubuntu:20.04 AS build-system

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG DEBIAN_FRONTEND=noninteractive
#
# Install apt-get basic tooling
RUN apt-get update && apt-get install --no-install-recommends -y \
    apt-utils \
    python3 \
    python3-pip \
    python3.8-venv \
    curl \
    git 
#
#Add Azure Resources
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash
# INSTALL pulumi
ARG PULUMI_VERSION=3.19.0
# Install the Pulumi SDK, including the CLI and language runtimes.
RUN curl -fsSL https://get.pulumi.com/ | bash -s -- --version $PULUMI_VERSION && \
  mv ~/.pulumi/bin/* /usr/bin
#
#Set sym links to tools
RUN ln -s /usr/bin/python3 /usr/bin/python \
    && rm -rf /usr/bin/pip \
    && ln -s /usr/bin/pip3 /usr/bin/pip

#
# Add oh my zsh
RUN apt-get update && apt-get install --no-install-recommends -y \
  zsh \
  wget \
  fonts-powerline \
  curl \
  locales \
  # set up locale
  && locale-gen en_US.UTF-8

# generate locale for agnoster
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && /usr/sbin/locale-gen
# Clean up
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
# Set XTERM
ENV TERM xterm
# Set the default shell to bash rather than sh
ENV SHELL /bin/zsh
 # run the installation script  
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true
RUN git clone git://github.com/zsh-users/zsh-completions.git /root/.oh-my-zsh/custom/plugins/zsh-completions
RUN cd /root && curl -fsSLO https://raw.githubusercontent.com/romkatv/dotfiles-public/master/.purepower
ADD agnoster.zsh-theme /root/.oh-my-zsh/themes
#
# Add pulumi cli 
RUN mkdir -p /root/.oh-my-zsh/custom/plugins/pulumi/\
    && pulumi gen-completion zsh > /root/.oh-my-zsh/custom/plugins/pulumi/pulumi.plugin.zsh 
# zsh configuration
ADD .zshrc /root
#
# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog
