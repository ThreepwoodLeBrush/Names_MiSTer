#!/usr/bin/env python3
# Copyright (c) 2021 José Manuel Barroso Galindo <theypsilon@gmail.com>

import re
import csv
import common

class MultipleNamesTXTReader:
    def __init__(self, options):
        self.options = options
        self.names_dicts = {}
        self.sorted_cores = []
        self.sorted_names_files = sorted(self.options["names_files"].keys())
        self.reading = False
        self.error = False

    def read_input_names_txt_files(self):
        if self.reading == True:
            raise ValueError("MultipleNamesTXTReader can read only once.")

        self.reading = True

        for file in self.sorted_names_files:
            try:
                self.__process_file(file)
            except BaseException as e:
                print("ERROR: {} {}".format(file, e))

        lengths = {}
        for file in self.sorted_names_files:
            lengths[len(self.names_dicts[file])] = True
        
        if len(lengths) != 1:
            self.error = True
            print("ERROR: different quantity of cores in some files: {}".format(lengths))

        if self.error == True:
            raise ValueError("Something bad happened. Check previous logs.")

        return {
            "names_dicts": self.names_dicts,
            "sorted_cores": self.sorted_cores,
            "sorted_names_files": self.sorted_names_files
        }

    def __process_file(self, file):
        self.names_dicts[file] = {}

        path = file + ".txt"

        with open(path) as fp:
            for cnt, line in enumerate(fp):

                if re.match(r'^\s*$', line):
                    continue

                if re.match(r'^(\s*\|\s*)*$', line):
                    continue

                splits = re.search(r'^([^\:]+)\:(.+)$', line)
                if splits:
                    groups = splits.groups()
                    core = groups[0].strip()
                    name_term = groups[1].strip()
                    self.names_dicts[file][core] = name_term
                    if file == self.sorted_names_files[0]:
                        self.sorted_cores.append(core)
                else:
                    print("Ignored line {}:{}\n{}".format(path, cnt, line))

class NamesCsvGenerator:
    def __init__(self, context, options):
        self.context = context
        self.options = options
        self.writing = False

    def write_output_names_csv(self):
        if self.writing == True:
            raise ValueError("NamesCsvGenerator can write only once.")

        self.writing = True

        file = self.options["output_names_csv"]
        cores_column_name = self.options["cores_column_name"]
        format_line_every = self.options["format_line_every"]
        straight_line_every = self.options["straight_line_every"]

        first_row = [self.format_core(self.options["cores_column_name"])] + list(map(lambda f: self.format_name(f, f), self.context["sorted_names_files"]))
        formatter_line = self.make_formatter_line()
        straight_line = self.make_straight_line(file, first_row)

        big_space_index = 0

        with open(file, 'w+', newline='\n') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=self.options["csv_separator"], quotechar=self.options["csv_quote_char"], quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            for cnt, core in enumerate(self.context["sorted_cores"]):

                if core == self.options["big_space_before_core"]:
                    big_space_index = cnt
                    for x in range(0, self.options["big_space_line_quantity"]):
                        csvfile.write("\n")

                line_index = cnt - big_space_index

                if line_index % straight_line_every == 0:

                    if line_index != 0:
                        csvfile.write("\n")

                    csvfile.write(straight_line)
                    csvwriter.writerow(first_row)
                    csvfile.write(straight_line)

                if line_index % format_line_every == 0:
                    csvfile.write(formatter_line)

                csvwriter.writerow(self.make_names_row(core))        

    def format_core(self, core):
        return core.ljust(self.options["cores_column_rightpadding_csv"], self.options["padding_char"])

    def format_name(self, name, file):
        charlimit = self.options["names_files"][file]
        return name.ljust(charlimit * 2, self.options["padding_char"])

    def count_firstline(self, file, first_row):
        with open(file, 'w', newline='\n') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=self.options["csv_separator"], quotechar=self.options["csv_quote_char"], quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(first_row)

        with open(file) as fp:
            for cnt, line in enumerate(fp):
                return len(line) - 1
                break
        return 0

    def make_straight_line(self, file, first_row):
        straight_line = self.options["straight_line_char"] * self.count_firstline(file, first_row) + "\n"

        if len(straight_line) < 20:
            raise ValueError("ERROR: straight_line too short... weird: {}".format(straight_line))

        return straight_line

    def make_formatter_line(self):
        padding_char = self.options["padding_char"]
        format_line_separator = self.options["format_line_separator"]

        formatter_line = self.format_core("") + format_line_separator
        for file in self.context["sorted_names_files"]:
            charcode = self.options["names_files"][file]
            formatter_line = formatter_line + padding_char * charcode + format_line_separator + (charcode - 1) * padding_char + format_line_separator
        return formatter_line + "\n"


    def make_names_row(self, core):
        row = [self.format_core(core)]
        temp_terms = {}
        for file in self.context["sorted_names_files"]:
            term = self.context["names_dicts"][file][core]
            if term in temp_terms:
                term = temp_terms[term]
            else:
                temp_terms[term] = "{}:{}".format(core, file.replace(self.options["stip_from_reference"], ""))
            row.append(self.format_name(term, file))
        return row

def run(options):
    files = list(map(lambda a: "'{}.txt'".format(a), options["names_files"].keys()))
    print("Reading core names from files: {}".format(", ".join(files)))
    context = MultipleNamesTXTReader(options).read_input_names_txt_files()
    print("Found {} names for cores in {} different versions.".format(len(context["sorted_cores"]), len(files)))
    print("Generating {} file...".format(options["output_names_csv"]))
    NamesCsvGenerator(context, options).write_output_names_csv()
    print("DONE.")

if __name__ == "__main__":
    run(common.options())
