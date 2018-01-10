FROM ubuntu:17.04

MAINTAINER TimVideos <robot@timvideos.us>

RUN \
	echo 'APT::Get::Assume-Yes "true";' > /etc/apt/apt.conf.d/yes \
	&& apt-get update \
	&& apt-get install -y git sudo \
	&& echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

ENV LITEX_BUILDENV_USER		timvideos
ENV LITEX_BUILDENV_REPO		litex-buildenv
ENV LITEX_BUILDENV_BRANCH       master
ENV LITEX_BUILDENV_REVISION	""
ENV LANG 			C.UTF-8

ENV TARGETS			base

RUN adduser --disabled-password --gecos '' litex-buildenv && adduser litex-buildenv sudo

USER litex-buildenv
WORKDIR /home/litex-buildenv

RUN git clone \
		https://github.com/$LITEX_BUILDENV_USER/$LITEX_BUILDENV_REPO \
		-b  $LITEX_BUILDENV_BRANCH \
		--single-branch \
		--no-shallow-submodules


RUN cd $LITEX_BUILDENV_REPO; sudo ./scripts/download-env-root.sh
RUN cd $LITEX_BUILDENV_REPO; ./.travis/setup.sh

