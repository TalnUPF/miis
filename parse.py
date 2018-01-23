#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import logging as log
import argparse

from clients.transition_client import NLTKParserClient
from clients.mate_client import MateClient

log.basicConfig(format='%(levelname)8s: %(message)s', level=log.DEBUG)

def write_output(save_dir, in_filename, text, extension=".conll"):

    basename = os.path.basename(in_filename)
    name, _ = os.path.splitext(basename)

    out_filename = name + extension
    out_filepath = os.path.join(save_dir, out_filename)

    output_dir = os.path.dirname(out_filepath)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with codecs.open(out_filepath, 'w', encoding='utf8') as out_fd:
        out_fd.write(text)

    log.debug("Content wrote to %s" % out_filepath)

def process_text_file(filepath, save_dir, deep_parse=False):

    try:
        with codecs.open(filepath, encoding='utf8') as fd:
            text = fd.read()

        log.info('Processing %s', filepath)

        if text.strip():

            log.debug('Parsing %s', filepath)
            parser = NLTKParserClient("en")
            conll = parser.parse_text(text)

            if save_dir:
                write_output(save_dir, filepath, str(conll), ".surface.conll")
            else:
                print "======================"
                print "       Surface"
                print "======================"
                print conll

            if deep_parse:
                mate = MateClient("en")
                conll = mate.process(conll)

                if save_dir:
                    write_output(save_dir, filepath, str(conll), ".deep.conll")
                else:
                    print "======================"
                    print "        Deep"
                    print "======================"
                    print conll

            log.info("File %s processed successfully.", filepath)

        else:
            log.info("File %s is empty. Skipping...", filepath)

        #"""
    except Exception as exc:
        log.warn("An error occurred while processing file %s.", filepath)
        log.warn("Error: %s: %s", type(exc).__name__, exc)
        log.warn("Skipping %s...", filepath)
        raise
        #"""

    finally:
        pass

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Parses plain text files using TALN web service.")

    parser.add_argument("file_list", metavar="FILE", nargs="+",
                        help="the file[s] to process.")

    parser.add_argument("-s", "--save_dir", default=False,
                        help='Store the parsing result into the supplied directory location.')

    parser.add_argument("-d", "--deep_parse", default=False, action='store_true',
                        help='Do also the deep parsing of the text.')

    args = parser.parse_args()

    save_dir = args.save_dir
    if save_dir:
        if not os.path.exists(save_dir):
            log.warning("The given location '%s' does not exists!", save_dir)
            
        elif not os.path.isdir(save_dir):
            log.warning("The given location '%s' is NOT a directory!", save_dir)

    for filename in args.file_list:
        if os.path.exists(filename):
            if os.path.isdir(filename):
                log.warning("The given location '%s' is a directory!", filename)
            else:
               process_text_file(filename, save_dir, args.deep_parse)

        else:
            log.warning("The given location '%s' does not exists!", filename)
