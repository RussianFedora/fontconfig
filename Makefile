# Makefile for source rpm: fontconfig
# $Id$
NAME := fontconfig
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
