#!/usr/bin/env python
# Copyright (C) 2011-2015 Swift Navigation Inc.
# Contact: Fergus Noble <fergus@swift-nav.com>
#
# This source is subject to the license found in the file 'LICENSE' which must
# be be distributed together with this source. All other rights reserved.
#
# THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
# EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.
"""
The :mod:`piksi_tools.serial_link` module contains functions related to
setting up and running SBP message handling.
"""
from __future__ import print_function

import os
import sys
import time
from monotonic import monotonic

import serial.tools.list_ports
from sbp.client import Forwarder, Framer, Handler
from sbp.client.drivers.cdc_driver import CdcDriver
from sbp.client.drivers.pyftdi_driver import PyFTDIDriver
from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client.drivers.file_driver import FileDriver, PlaybackFileDriver
from sbp.client.loggers.json_logger import JSONLogger, JSONBinLogger, JSONLogIterator
from sbp.client.loggers.null_logger import NullLogger
from sbp.logging import SBP_MSG_LOG, SBP_MSG_PRINT_DEP, MsgLog
from sbp.piksi import MsgReset

from piksi_tools.utils import mkdir_p, get_tcp_driver, call_repeatedly
from piksi_tools import __version__ as VERSION

SERIAL_PORT = "/dev/ttyUSB0"
SERIAL_BAUD = 115200


def logfilename():
    return time.strftime("serial-link-%Y%m%d-%H%M%S.log.json")


def get_ports():
    """
    Get list of serial ports.
    """
    return [
        p for p in serial.tools.list_ports.comports() if p[1][0:4] != "ttyS"
    ]


def base_cl_options(override_arg_parse=None, add_help=True,
                    add_log_args=False, add_reset_arg=False):
    import argparse
    if override_arg_parse:
        parserclass = override_arg_parse
    else:
        parserclass = argparse.ArgumentParser
    parser = parserclass(
        description="Swift Navigation SBP Client version " + VERSION, add_help=add_help)
    parser.add_argument(
        "-p", "--port", default=None, help="specify the serial port to use.")
    parser.add_argument(
        "-b",
        "--baud",
        default=SERIAL_BAUD,
        help="specify the baud rate to use.")
    parser.add_argument(
        "--rtscts",
        default=False,
        action="store_true",
        help="Enable Hardware Flow Control (RTS/CTS).")
    parser.add_argument(
        "-t",
        "--tcp",
        action="store_true",
        default=False,
        help="Use a TCP connection instead of a local serial port. \
                      If TCP is selected, the port is interpreted as host:port"
    )
    parser.add_argument(
        "-f",
        "--ftdi",
        action="store_true",
        help="use pylibftdi instead of pyserial.")
    parser.add_argument(
        "--file",
        help="Read with a filedriver rather than pyserial.",
        action="store_true")
    parser.add_argument(
        '--json',
        action="store_true",
        help="Input is SBP JSON")
    parser.add_argument(
        '--playback',
        action="store_true",
        help="Emulate real input")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print extra debugging information.")
    if add_reset_arg:
        parser.add_argument(
            "-r",
            "--reset",
            action="store_true",
            help="reset device after connection.")
    if add_log_args:
        parser.add_argument(
            "-l",
            "--log",
            action="store_true",
            help="serialize SBP messages to autogenerated log file.")
        parser.add_argument(
            "-o",
            "--log-dirname",
            default='',
            help="directory in which to create logfile.")
        parser.add_argument(
            "--logfilename",
            default='',
            help='filename to use for log. Default filename with date and timestamp is used otherwise.'
        )
        parser.add_argument(
            '--expand-json',
            action="store_true",
            default=False,
            help="Expand fields in JSON logs"
        )
        parser.add_argument(
            "--skip-metadata",
            action="store_true",
            help="Omit metadata from JSON logs.")
        parser.add_argument(
            "--sort-keys",
            action="store_true",
            help="Sort JSON log elements by keys.")
        parser.add_argument(
            "--sender-id-filter",
            default=None,
            help="comma separated List of base10 sender_ids: e.g: 4096,0")
    return parser


def get_args():
    """
    Get and parse arguments.
    """
    parser = base_cl_options(add_log_args=True, add_reset_arg=True)
    parser.add_argument(
        "--timeout",
        default=None,
        help="exit after TIMEOUT seconds have elapsed.")
    parser.add_argument(
        "--status",
        default=False,
        action="store_true",
        help="print periodic data rate to stdout.")
    return parser.parse_args()


def get_driver(use_ftdi=False,
               port=SERIAL_PORT,
               baud=SERIAL_BAUD,
               use_file=False,
               playback=False,
               rtscts=False):
    """
    Get a driver based on configuration options

    Parameters
    ----------
    use_ftdi : bool
      For serial driver, use the pyftdi driver, otherwise use the pyserial driver.
    port : string
      Serial port to read.
    baud : int
      Serial port baud rate to set.
    """
    try:
        if use_ftdi:
            return PyFTDIDriver(baud)
        if use_file:
            if playback:
                return PlaybackFileDriver(open(port, 'rb'))
            return FileDriver(open(port, 'rb'))
    # HACK - if we are on OSX and the device appears to be a CDC device, open as a binary file
        for each in serial.tools.list_ports.comports():
            if port == each[0] and sys.platform == "darwin":
                if each[1].startswith("Gadget Serial") or each[1].startswith("Piksi"):
                    print("Opening a file driver")
                    return CdcDriver(open(port, 'w+b', 0))
        return PySerialDriver(port, baud, rtscts=rtscts)
    # if finding the driver fails we should exit with a return code
    # currently sbp's py serial driver raises SystemExit, so we trap it
    # here
    except SystemExit:
        sys.exit(1)


def get_logger(use_log=False, filename=logfilename(), expand_json=False, sort_keys=False):
    """
    Get a logger based on configuration options.

    Parameters
    ----------
    use_log : bool
      Whether to log or not.
    filename : string
      File to log to.
    """
    if not use_log:
        return NullLogger()
    dirname = os.path.dirname(filename)
    if dirname:
        mkdir_p(dirname)
    print("Starting JSON logging at %s" % filename)
    infile = open(filename, 'w')
    if expand_json:
        logger = JSONLogger
    else:
        logger = JSONBinLogger
    return logger(infile, sort_keys=sort_keys)


def printer(sbp_msg, **metadata):
    """
    Default print callback

    Parameters
    ----------
    sbp_msg: SBP
      SBP Message to print out.
    """
    print(sbp_msg.payload.decode('ascii', 'replace'), end=' ')


def log_printer(sbp_msg, **metadata):
    """
    Default log callback

    Parameters
    ----------
    sbp_msg: SBP
      SBP Message to print out.
    """
    levels = {
        0: 'EMERG',
        1: 'ALERT',
        2: 'CRIT',
        3: 'ERROR',
        4: 'WARN',
        5: 'NOTICE',
        6: 'INFO',
        7: 'DEBUG'
    }
    m = MsgLog(sbp_msg)
    print(levels[m.level], m.text.decode('ascii', 'replace'))


def swriter(link):
    """Callback intended for reading out messages from one stream and into
    a serial link stream.

    Parameters
    ----------
    link : file handle

    Returns
    ----------
    A callback function taking an SBP message.

    """

    def scallback(sbp_msg, **metadata):
        link(sbp_msg)

    return scallback


def run(args, link, stop_function=lambda: None):
    """Spin loop for reading from the serial link.

    Parameters
    ----------
    args : object
      Argparse result.
    link : Handler
      Piksi serial handle

    """
    link.start()
    timeout = args.timeout
    if args.reset:
        link(MsgReset(flags=0))
    try:
        if args.timeout is not None:
            expire = monotonic() + float(args.timeout)
        while True:
            if timeout is None or monotonic() < expire:
                # Wait forever until the user presses Ctrl-C
                time.sleep(1)
            else:
                print("Timer expired!")
                stop_function()
                break

            if link.is_alive():
                continue

            if getattr(args, 'file', None):
                # If reading from a file it is expected to end at some point
                stop_function()
                sys.exit(0)

            if args.verbose:
                sys.stderr.write("ERROR: link is gone!\n")

            stop_function()
            sys.exit(1)
    except KeyboardInterrupt:
        # Callbacks call thread.interrupt_main(), which throw a
        # KeyboardInterrupt exception. To get the proper error
        # condition, return exit code of 1. Note that the finally
        # block does get caught since exit itself throws a
        # SystemExit exception.
        stop_function()
        sys.exit(1)


def get_base_args_driver(args):
    driver = None
    if getattr(args, 'tcp', None):
        driver = get_tcp_driver(getattr(args, 'port', None))
    else:
        driver_kwargs = {}
        # unpack relevant args
        driver_kwargs['use_ftdi'] = getattr(args, 'ftdi', None)
        driver_kwargs['port'] = getattr(args, 'port', None)
        driver_kwargs['baud'] = getattr(args, 'baud', None)
        driver_kwargs['use_file'] = getattr(args, 'file', None)
        driver_kwargs['playback'] = getattr(args, 'playback', None)
        driver_kwargs['rtscts'] = getattr(args, 'rtscts', None)
        # trim none values
        driver_kwargs = {k: v
                         for k, v in driver_kwargs.items()
                         if v is not None}
        driver = get_driver(**driver_kwargs)
    return driver


def main(args):
    """
    Get configuration, get driver, get logger, and build handler and start it.
    """
    log_filename = args.logfilename
    log_dirname = args.log_dirname

    stop_function = lambda: None # noqa

    if not log_filename:
        log_filename = logfilename()
    if log_dirname:
        log_filename = os.path.join(log_dirname, log_filename)
    driver = get_base_args_driver(args)
    sender_id_filter = []
    if args.sender_id_filter is not None:
        sender_id_filter = [int(x) for x in args.sender_id_filter.split(",")]
    if args.json:
        source = JSONLogIterator(driver, conventional=True)
    else:
        source = Framer(driver.read,
                        driver.write,
                        args.verbose,
                        skip_metadata=args.skip_metadata,
                        sender_id_filter_list=sender_id_filter)
    last_bytes_read = [0]
    if args.status:
        def print_io_data(last_bytes_read):
            # bitrate is will be kilobytes per second. 2 second period, 1024 bytes per kilobyte
            kbs_avg = driver.bytes_read_since(last_bytes_read[0]) / (2 * 1024.0)
            print("{0:.2f} KB/s average data rate (2 second period).".format(kbs_avg))
            last_bytes_read[0] = driver.total_bytes_read
        stop_function = call_repeatedly(2, print_io_data, last_bytes_read)
    with Handler(source, autostart=False) as link, get_logger(args.log,
                                                              log_filename,
                                                              args.expand_json,
                                                              args.sort_keys) as logger:
        link.add_callback(printer, SBP_MSG_PRINT_DEP)
        link.add_callback(log_printer, SBP_MSG_LOG)
        Forwarder(link, logger).start()
        run(args, link, stop_function=stop_function)


if __name__ == "__main__":
    main(get_args())
