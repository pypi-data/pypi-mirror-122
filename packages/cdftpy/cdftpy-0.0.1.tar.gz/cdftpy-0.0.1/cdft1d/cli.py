#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import pathlib
import re
import sys

import click
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory, AutoSuggest
from prompt_toolkit.history import FileHistory, InMemoryHistory
from prompt_toolkit.shortcuts import radiolist_dialog, confirm
from prompt_toolkit.validation import Validator

from cdft1d.io_utils import read_solute, read_key_value
from cdft1d.rdf import analyze_rdf_peaks_sim, write_rdf_sim, analyze_rdf_peaks, write_rdf
from cdft1d.rism_new import rism_1d
from cdft1d.rsdft import rsdft_1d
from cdft1d.solvent import load_solvent_model
from cdft1d.chemdata import ION_CHARGE
from cdft1d.config import DATA_DIR

from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.completion import WordCompleter


HEADER = """
==================================
1D-CDFT PROGRAM

Marat Valiev and Gennady Chuev
==================================
"""


def cdft_run_interactive():

    def is_float(num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def file_exist(filename):
        filename = filename+".dat"
        filepath = pathlib.Path.cwd() / filename
        new_file = not filepath.exists()
        one_word = (filename.strip().find(' ') == -1)
        not_blank = (filename.strip() != "")
        return one_word and not_blank

    def correct_method(method):
        return method in {'rism','rsdft'}

    def is_word(line):
        return line.strip().find(' ') == -1

    validator_method = Validator.from_callable(
        correct_method,
        error_message='Only rism or rsdft theories are supported',
        move_cursor_to_end=True)

    validator = Validator.from_callable(
        is_float,
        error_message='This input is invalid number',
        move_cursor_to_end=True)
    validator_file = Validator.from_callable(
        file_exist,
        error_message='Bad filename',
        move_cursor_to_end=True)

    validator_word = Validator.from_callable(
        is_word,
        error_message='File exists, add ! to overwrite',
        move_cursor_to_end=True)

    history = InMemoryHistory()
    history.append_string("rism")
    history.append_string("rsdft")
    history.append_string("s2_rsdft")
    history.append_string("s2_rism")

    cdft_completer = WordCompleter(['rism', 'rsdft'])


    def bottom_toolbar(text):
        return (text)

    default_title = 'CDFT Interactive session'
    session = PromptSession()

    while True:
        try:

            prompt("Simulation type: ",  accept_default=True, default=" Single ion solvation")

            method = prompt("Theory (rsdft or rism): ",
                                    default="rsdft", validator = validator_method, completer=cdft_completer)
            solvent = prompt("Solvent model: ", default="s2")
            print("Provide ion parameters")
            name = prompt('  name: ', default="Cl")

            charge = prompt('  charge: ', default=str(ION_CHARGE.get(name.lower(), None)))
            eps = prompt('  \u03B5 (kcal/mol): ', validator=validator, default='0.05349244',)
            sigma = prompt('  \u03C3 (Å): ', validator=validator, default='4.83')

            while 1:
                input_file = prompt("Choose name for the input file: ",  validator=validator_file)
                input_file = input_file.split('!')[0] + ".dat"
                filepath = pathlib.Path.cwd() / input_file
                if filepath.exists():
                    answer = confirm(f"File {input_file} exists. Overwrite? ", suffix='y/N: ')
                    if answer:
                        break
                    continue
                break

            now = datetime.datetime.now()
            with open(input_file, "w") as fp:
                fp.write("# Input file for single ion solvation calculation\n")
                fp.write(f"# generated on {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
                fp.write("<solute>\n")
                fp.write(f"#name  sigma  eps charge \n")
                fp.write(f" {name}  {sigma} {eps} {charge} \n")
                fp.write("<simulation>\n")
                fp.write(f"theory {method}\n")
                fp.write(f"solvent {solvent}\n")
                fp.write(f"<analysis>\n")
                fp.write(f"rdf_peaks\n")
                fp.write(f"<output>\n")
                fp.write(f"rdf\n")

            print(f"Generated input file {input_file}")

            to_run = prompt("Run calculation?: ", default="y")
            if to_run == 'y':
                cdft_run_input(input_file)

        except EOFError:
            quit(1)
        except KeyboardInterrupt:
            quit(0)
        else:
            break

    return input_file


# noinspection PyTypeChecker
@click.command()
@click.argument('input_file', default="")
def cdft(input_file):
    """
    Perform CDFT calculation

    Args:
        input_file


    """

    if input_file == "":
        input_file = cdft_run_interactive()
    else:
        cdft_run_input(input_file)


def cdft_run_input(input_file):

    solute = read_solute(input_file)
    for k, v in solute.items():
        solute[k] = v[0]

    parameters = read_key_value(input_file, section="simulation")

    solvent_name = parameters["solvent"]
    solvent_model = load_solvent_model(solvent_name)

    theory = parameters.pop("theory")
    if theory == "rism":
        sim = rism_1d(solute, solvent_model, params=parameters)
    elif theory == "rsdft":
        sim = rsdft_1d(solute, solvent_model, params=parameters)
    else:
        print(f"Unknown method {theory}")
        sys.exit(1)
    pass

    analysis = read_key_value(input_file, section="analysis")
    if analysis is not None:
        if "rdf_peaks" in analysis:
            analyze_rdf_peaks_sim(sim)

    output = read_key_value(input_file, section="output")
    if output is not None:
        if "rdf" in output:
            write_rdf_sim(sim)


if __name__ == '__main__':

    cdft("")
