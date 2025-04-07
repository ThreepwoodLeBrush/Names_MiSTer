#!/usr/bin/env python3
# Copyright (c) 2021 José Manuel Barroso Galindo <theypsilon@gmail.com>

import csv
import common

class NamesCSVReader:
    def __init__(self, options):
        self.options = options
        self.reading = False
        self.names_files = {}
        self.cores = []
        self.headers = None

    def read_input_names_csv(self):
        if self.reading == True:
            raise ValueError("NamesCSVReader can read only once.")

        self.reading = True

        with open(self.options["input_names_csv"]) as csvfile:
            csvrows = list(csv.reader(csvfile, delimiter=self.options["csv_separator"], quotechar=self.options["csv_quote_char"], quoting=csv.QUOTE_MINIMAL))
            row_len = None
            for row_count, raw_row in enumerate(csvrows):
                row = list(map(lambda h: h.strip(), raw_row))

                if len(row) <= 1:
                    continue

                if self.headers == None:
                    self.headers = row

                if bool(set(self.headers).intersection(row)):
                    continue

                if row_len == None:
                    row_len = len(row)

                if row_len != len(row):
                    raise ValueError("Wrong len at line {}, should have {} columns, but has {}.".format(row_count, row_len, len(row)))

                self.read_columns(row)

        return {
            "cores": self.cores,
            "names_files": self.names_files
        }

    def read_columns(self, row):
        core = None
        for index, column in enumerate(row):
            if core == None:
                core = column
                continue

            variation = self.headers[index]
            if variation not in self.names_files:
                self.names_files[variation] = {}

            if core in self.names_files[variation]:
                raise ValueError("Core {}, was already in {}.".format(core, variation))

            maybe_reference = "{}{}".format(self.options["strip_from_reference"], column.replace(core + ":", ""))
            if maybe_reference in self.headers:
                column = self.names_files[maybe_reference][core]

            self.names_files[variation][core] = column

        self.cores.append(core)

class NamesTXTWriter:
    def __init__(self, context, options):
        self.context = context
        self.options = options
        self.reading = False

    def write_names_txt(self):
        if self.reading == True:
            raise ValueError("NamesTXTWriter can read only once.")

        self.reading = True

        formatter_line = self.make_formatter_line()

        with open(self.context["output_file"], 'w+') as namesfile:
            for cnt, core in enumerate(self.context["cores"]):
                if cnt % self.options["format_line_every"] == 0:
                    namesfile.write(formatter_line)

                namesfile.write("{}{}\n".format(self.format_core(core), self.context["names_dict"][core]))

        return self.context

    def make_formatter_line(self):
        return "{}\n".format(self.options["formatter_line_names_txt"])

    def format_core(self, core):
        return (core + ":").ljust(self.options["cores_column_rightpadding_txt"] + 1, self.options["padding_char"])

def run(options):
    print("Reading {}".format(options["input_names_csv"]))
    content = NamesCSVReader(options).read_input_names_csv()
    print("Found {} names variations for {} cores.".format(len(content["names_files"]), len(content["cores"])))
    for variation in content["names_files"].keys():
        context = {
            "output_file": "{}.txt".format(variation),
            "names_dict": content["names_files"][variation],
            "cores": content["cores"]
        }
        NamesTXTWriter(context, options).write_names_txt()
        print("File '{}' generated.".format(context["output_file"]))
    print("DONE.")

if __name__ == "__main__":
    run(common.options())
