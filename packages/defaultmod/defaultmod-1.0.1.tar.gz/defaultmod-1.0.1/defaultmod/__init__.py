PY_VERSION=0

import __future__
import _thread
import abc
import aifc
import argparse
import array
import ast
import asynchat
import asyncio
import asyncore
import atexit
import audioop
import base64
import bdb
import binascii
import binhex
import bisect
import builtins
import bz2
import calendar
import cgi
import cgitb
import chunk
import cmath
import cmd
import code
import codecs
import codeop
import collections
import colorsys
import compileall
import concurrent
import configparser
import contextlib
import contextvars
import copy
import copyreg
import cProfile
try:
  import crypt
except:
  #print("Error importing 'crypt'. It is unix-only")
  pass
import csv
import ctypes
try:
  import curses
except:
  #print("Error importing 'curses'. It is unix-only")
  pass
import dataclasses
import datetime
import dbm
import decimal
import difflib
import dis
import distutils
import doctest
import email
import encodings
import ensurepip
import enum
import errno
import faulthandler
try:
  import fcntl
except:
  #print("Error importing 'fcntl'. It is unix-only")
  pass
import filecmp
import fileinput
import fnmatch
import fractions
import ftplib
import functools
import gc
import getopt
import getpass
import gettext
import glob
import graphlib
try:
  import grp
except:
  #print("Error importing 'grp'. It is unix-only")
  pass
import gzip
import hashlib
import heapq
import hmac
import html
import http
import imaplib
import imghdr
#deprecated: import imp 
import importlib
import inspect
import io
import ipaddress
import itertools
import json
import keyword
import lib2to3
import linecache
import locale
import logging
import lzma
import mailbox
import mailcap
import marshal
import math
import mimetypes
import mmap
import modulefinder
try:
  import msilib
except:
  #print("Error importing 'msilib'. It is win-only")
  pass
try:
  import msvcrt
except:
  #print("Error importing 'msvcrt'. It is win-only")
  pass
import multiprocessing
import netrc
try:
  import nis
except:
  #print("Error importing 'nis'. It is unix-only")
  pass
import nntplib
import numbers
import operator
#deprecated: import optparse
import os
try:
  import ossaudiodev
except:
  #print("Error importing 'ossa.'. linux+bsd only")
  pass
import pathlib
import pdb
import pickle
import pickletools
try:
  import pipes
except:
  #print("Error importing 'pipes'. It is unix-only")
  pass
import pkgutil
import platform
import plistlib
import poplib
try:
  import posix
except:
  #print("Error importing 'posix'. It is unix-only")
  pass
import pprint
import profile
import pstats
try:
  import pty
except:
  #print("Error importing 'pty'. It is unix-only")
  pass
try:
  import pwd
except:
  #print("Error importing 'pwd'. It is unix-only")
  pass
import py_compile
import pyclbr
import pydoc
import queue
import quopri
import random
import re
try:
  import readline
except:
  #print("Error importing 'readl.'. It is unix-only")
  pass
import reprlib
try:
  import resource
except:
  #print("Error importing 'resour.' It is unix-only")
  pass
import rlcompleter
import runpy
import sched
import secrets
import select
import selectors
import shelve
import shlex
import shutil
import signal
import site
import smtpd
import smtplib
import sndhdr
import socket
import socketserver
try:
  import spwd
except:
  #print("Error importing 'spwd'. It is unix-only")
  pass
import sqlite3
import ssl
import stat
import statistics
import string
import stringprep
import struct
import subprocess
import sunau
import symtable
import sys
import sysconfig
try:
  import syslog
except:
  #print("Error importing 'syslog'. It is unix-only")
  pass
import tabnanny
import tarfile
import telnetlib
import tempfile
try:
  import termios
except:
  #print("Error importing 'termi.'. It is unix-only")
  pass
import test
import textwrap
import threading
import time
import timeit
try:
  import tkinter
  PY_VERSION=3
except:
  import Tkinter
  PY_VERSION=2
import token
import tokenize
import trace
import traceback
import tracemalloc
try:
  import tty
except:
  #print("Error importing 'tty'. It is unix-only")
  pass
import turtle
try:
  import turtledemo
except:
  pass
import types
import typing
import unicodedata
import unittest
import urllib
import uu
import uuid
import venv
import warnings
import wave
import weakref
import webbrowser
try:
  import winreg
except:
  #print("Error importing 'winreg'. It is win-only")
  pass
try:
  import winsound
except:
  #print("Error importing 'winsou.'. It is win-only")
  pass
import wsgiref
import xdrlib
import xml
import xmlrpc
import zipapp
import zipfile
import zipimport
import zlib
try:
  import zoneinfo
except:
  #print("Unknown Error Importing ZoneInfo.")
  pass
def add(module):
  return __import__(module,fromlist=[""])
def get_sys():
  try:
    import curses
    return "unix-based"
  except:
    return "win"
def install(module):
  os.system("pip install " + module)
