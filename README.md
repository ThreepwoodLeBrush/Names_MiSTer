# Names_MiSTer

The names.txt-files provide proper system names in the OSD (main menu) of MiSTer FPGA. The aim is to build name-files for different regions, with different system name lengths and ways of sorting. The files can be pulled via updater scripts, or used as a base for a custom names.txt.

By default MiSTer displays the filenames of the individual core files (*.rbf). If a names.txt is present in the root of the microSD and only if a core name is matched, then the name is substituted in the way of '[rbf-filename]: [substitute name]', e.g. 'Minimig: Commodore Amiga'.

If a new core is installed via updater, that does not have a substitute name in the names.txt yet, then it will appear in the list of systems with its rbf-filename. The other cores that have a match in names.txt will still be represented by their substitute names.

## Quickstart
1. Download the file with the desired region, sorting and maximum name length (18, 28 or full)
2. Rename the file to "names.txt"
3. Copy the names.txt to the root of the MiSTer micro SD (same location as MiSTer.ini)
4. [Optional] In MiSTer.ini set 'rbf_hide_datecode=1' to disable Date codes of cores in the MiSTer main menu (F2 toggles the display of Date Codes). This allows up to 28 characters to be displayed without scrolling.

## Syntax
The filenames are made up from "names_[CHAR18 or CHAR28 or FULL]_[sorting]_[country/continent].txt" and must be renamed to "names.txt" to be used.

### Char Code
* CHAR18: Maximum system name length is 18 characters to fit without scrolling when Date Codes are ON.
* CHAR28: Maximum system name length is 28 characters to fit without scrolling when Date Codes are OFF.
* CHAR54: Maximum system name length is 54 characters to fit two lines without scrolling when Date Codes are OFF.

### Sort Code
* Manufacturer: Will prepend the system name with a manufacturer name to group them by manufacturer where available.
* Common: This variant uses commonly used names for systems, like only "Amiga" for the Commodore Amiga, but "Commodore 64" for said system. These variants are often shorter while still being instantly recognizable.

### Country / Continent
ISO 3166-1 alpha-2 Codes and Country Codes, like JP, US, EU, are used to append a region code to files that contain region specific naming of systems.

## How to contribute
Pull requests are welcome. When making a pull request, please try to provide a source for the validity of the change or addition.