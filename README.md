# Names_MiSTer

The names.txt file provides proper system names in the OSD of MiSTer FPGA. The file needs to go into the root of the main microSD, the same place where MiSTer.ini and the MiSTer binary are located.

When core date codes are disabled then the system names can have a maximum length of 28 characters before extending off screen and scrolling after a short delay. In MiSTer.ini set rbf_hide_datecode=1 to hide these core timestamps. F2 toggles the display of date codes in case they are required to be temporarily visible.

The aim of this names.txt is to keep all system names withing this 28 characters limit and if available preface the system with a manufacturer name or acronym for better sorting.
