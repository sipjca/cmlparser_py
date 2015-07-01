# cmlparser_py
Parses avogadro created .cml files

Uses a command line argument specifying the location of the file to parse.
It doesn't check the filename for the extention cml, so be sure it is a cml
file otherwise there may be issues.

There are a few command line flags to be aware of:

python Main.py <cml-filename> <output-filename> %<aa>

<cml-filename> - The name and location of the cml file you would like to parse

OPTIONAL - <output-filename> - If you want to output the debugging output/lammps to a file

OPTIONAL - <aa> - Specifiy "aa" if you want to use an opls-aa(all atom) forcefield rather than a opls-ua(united atom) forcefield
