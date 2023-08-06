# Example:
# python -m b2bTools -dynamics -agmata -file ./b2bTools/test/input/example_toy.fasta

import json
import sys
import os
from .wrapper_source.wrapper_utils import *

def print_help_section():
    print("Help section:")
    print("Show help section: --help or -h")
    print("An input file in FASTA format is required: -file /path/to/file.fasta")
    print("An output file path is required: -output /path/to/output_file.json")
    print("An output index file path is required: -index /path/to/output_file.csv")
    print("At least one predictor should be present:")
    print("AgMata: -agmata or -aggregation")
    print("Dynamine: -dynamine or -dynamics")
    print("Disomine: -disomine or -disorder")
    print("EFoldMine: -efoldmine or -early_folding_events")
    print("PSPer: -psp or -psper")
    print("An identifier is required: -identifier name")
    print("Full documentation available on https://pypi.org/project/b2bTools/")
    exit(0)

if __name__ == '__main__':
    _command, *parameters = sys.argv
    print("Bio2Byte Tools - Command Line Interface")

    tools = []
    fileName = None
    outputFileName = None
    outputIndexFileName = None
    identifier = None
    short_id = False

    for index, param in enumerate(parameters):
        if param == "--help" or param == "-h":
          print_help_section()
        if param == "-short-id":
            short_id = True
        if param == "-file":
          fileName = parameters[index + 1]
        if param == "-output":
          outputFileName = parameters[index + 1]
        if param == "-identifier":
          identifier = parameters[index + 1]
        if param == "-dynamics" or param == "-{0}".format(constants.TOOL_DYNAMINE):
            tools.append(constants.TOOL_DYNAMINE)
        if param == "-aggregation" or param == "-{0}".format(constants.TOOL_AGMATA):
            tools.append(constants.TOOL_AGMATA)
        if param == "-early_folding_events" or param == "-{0}".format(constants.TOOL_EFOLDMINE):
            tools.append(constants.TOOL_EFOLDMINE)
        if param == "-disorder" or param == "-{0}".format(constants.TOOL_DISOMINE):
            tools.append(constants.TOOL_DISOMINE)
        if param == "-psp" or param == "-{0}".format(constants.TOOL_PSP):
            tools.append(constants.TOOL_PSP)
        if param == "-index":
            outputIndexFileName = parameters[index + 1]

    if len(tools) == 0:
        exit("At least one predictor should be present: -agmata, -dynamine, -disomine, -efoldmine")
    if not fileName:
        exit("An input file is required: -file /path/to/file")
    if not outputFileName:
        exit("An output file path is required: -output /path/to/output_file.json")

    output_filepath = os.path.realpath(outputFileName)
    outputIndex_filepath = os.path.realpath(outputIndexFileName)

    single_seq = SingleSeq(fileName, short_id).predict(tools)

    print("All predictions have been executed. Next step: exporting the results")
    all_predictions = single_seq.get_all_predictions()
    with open(output_filepath, 'w') as json_file_handler:
        json.dump(all_predictions, json_file_handler, indent=2)

    if outputIndexFileName is not None:
        print("All predictions have been executed. Next step: exporting the index")
        single_seq.index(outputIndex_filepath, os.path.basename(output_filepath))

    exit(0)
