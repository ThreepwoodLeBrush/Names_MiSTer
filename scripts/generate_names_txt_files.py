# Copyright (c) 2021 José Manuel Barroso Galindo <theypsilon@gmail.com>

import csv
from common import options
from typing import Optional

class NamesCSVContent:
    def __init__(self, cores: list[str], names_files: dict[str, dict[str, str]]) -> None:
        self.cores = cores
        self.names_files = names_files

class NamesCSVReader:
    def __init__(self) -> None:
        self.reading = False
        self.names_files: dict[str, dict[str, str]] = {}
        self.cores: list[str] = []
        self.headers: Optional[list[str]] = None

    def read_input_names_csv(self) -> NamesCSVContent:
        if self.reading == True:
            raise ValueError("NamesCSVReader can read only once.")

        self.reading = True

        with open(options.input_names_csv) as csvfile:
            csvrows = list(csv.reader(csvfile, delimiter=options.csv_separator, quotechar=options.csv_quote_char, quoting=csv.QUOTE_MINIMAL))
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

        return NamesCSVContent(self.cores, self.names_files)

    def read_columns(self, row: list[str]) -> None:
        core = None
        for index, column in enumerate(row):
            if core == None:
                core = column
                continue

            assert core is not None
            assert self.headers is not None
            variation = self.headers[index]
            if variation not in self.names_files:
                self.names_files[variation] = {}

            if core in self.names_files[variation]:
                raise ValueError("Core {}, was already in {}.".format(core, variation))

            maybe_reference = "{}{}".format(options.strip_from_reference, column.replace(core + ":", ""))
            if maybe_reference in self.headers:
                column = self.names_files[maybe_reference][core]

            self.names_files[variation][core] = column

        if core is not None:
            self.cores.append(core)

class NamesTXTWriter:
    def __init__(self, content: NamesCSVContent) -> None:
        self.content = content
        self.reading = False

    def write_names_txt(self, variation: str) -> None:
        output_file = "{}.txt".format(variation)
        if self.reading == True:
            raise ValueError("NamesTXTWriter can read only once.")

        self.reading = True

        formatter_line = self.make_formatter_line()

        with open(output_file, 'w+', newline='\n') as namesfile:
            for cnt, core in enumerate(self.content.cores):
                if cnt % options.format_line_every == 0:
                    namesfile.write(formatter_line)

                namesfile.write("{}{}\n".format(self.format_core(core), self.content.names_files[variation][core]))

        print("File '{}' generated.".format(output_file))

    def make_formatter_line(self) -> str:
        return "{}\n".format(options.formatter_line_names_txt)

    def format_core(self, core: str) -> str:
        return (core + ":").ljust(options.cores_column_rightpadding_txt + 1, options.padding_char)

def run() -> None:
    print("Reading {}".format(options.input_names_csv))
    content = NamesCSVReader().read_input_names_csv()
    print("Found {} names variations for {} cores.".format(len(content.names_files), len(content.cores)))
    for variation in content.names_files.keys():
        NamesTXTWriter(content).write_names_txt(variation)
        
    print("DONE.")

if __name__ == "__main__":
    run()
