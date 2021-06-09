# Container Image
FROM python:3.8

# Install additional utils
RUN apt update && apt install -y sudo \
                                 rpm \
                                 vim \
                                 git \
                                 zip \
                                 cloc \
                                 dnsutils \
                                 zsh \
                                 zsh-syntax-highlighting \
                                 zsh-doc \
                                 less \
                                 liquidprompt \
                                 software-properties-common

RUN apt -y dist-upgrade

ARG USERNAME=builder
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    # && apt-get update \ # redundant
    # && apt-get install -y sudo \ # redundant
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

RUN echo "builder ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo "# macros"                      >  /home/builder/.rpmmacros && \
    echo "%_topdir    /workspaces/pbrmon/rpmbuild" >> /home/builder/.rpmmacros && \
    echo "%_sourcedir %{_topdir}/SOURCES"        >> /home/builder/.rpmmacros && \
    echo "%_builddir  %{_topdir}/BUILD"        >> /home/builder/.rpmmacros && \
    echo "%_specdir   %{_topdir}/SPECS"        >> /home/builder/.rpmmacros && \
    echo "%_rpmdir    %{_topdir}/RPM"        >> /home/builder/.rpmmacros && \
    echo "%_srcrpmdir %{_topdir}/SRPMS"        >> /home/builder/.rpmmacros && \
    mkdir /home/builder/rpmbuild && \
    chown -R builder /home/builder

# Install Python Packages
RUN pip install --upgrade pip
RUN pip install Pyyaml jsonrpclib pyeapi jsonschema treelib

USER builder

ENV name='PbrMon'