#!/usr/bin/python3
""" ! Coding Style Checker ! """

import glob
import re
import os.path
import color
# import fnmatch


class File:
    """  File class """

    def __init__(self, name):
        self._name = name
        with open(name) as file_fd:
            self._content = file_fd.readlines()
        self._full_content = "".join(self._content)
        self._ext = os.path.splitext(name)[1]
        self._type = "SOURCE" if self._ext in [".c", ".cpp"] else "HEADER"
        self._err = 0

    def get_name(self):
        """ @returns: name """
        return self._name

    def get_content(self):
        """ @returns: content """
        return self._content

    def get_full_content(self):
        """ @returns: full content """
        return self._full_content

    def get_ext(self):
        """ @returns: extension of file """
        return self._ext

    def get_type(self):
        """ @returns: type of file """
        return self._type

    def get_nb_err(self):
        """ @returns: number of error """
        return self._err


def get_files(ext):
    """
    Gets all *.ext files in current dir/subdir.

    @returns: list of files
    """

    return [filename for filename in glob.iglob("./**/*.{}".format(ext),
                                                recursive=True)]


def check_columns(_file):
    """ Checks lenght of a line """

    nb_line = 1
    for line in _file.get_content():
        nb_tab = line.count("\t")
        lenght = len(line) - nb_tab + nb_tab * 8
        tmp = line.lstrip()
        if lenght > 80 and not re.search(r"^\*\*|\/\*|\*\/|\/\/.*$", tmp):
            _file._err += 1
            display_err("More than 80 characters", nb_line, _file.get_name())
        nb_line += 1
    return


def check_nb_functions(_file):
    """ Checks number of functions in a file """

    nb_fc = 0
    for line in _file.get_content():
        if re.match("^{", line):
            nb_fc += 1
    if nb_fc > 5:
        _file._err += 1
        print(color.RED, " - More than 5 functions in the file {}{}\n"
              .format(color.BLUE, _file.get_name()))
    return


def check_epitech_header(_file):
    """ Checks epitech header """

    if not re.search("..\n.. EPITECH PROJECT, [0-9]{4}\n...*\n.. File description:\n...*\n..",
                     _file.get_full_content()):
        _file._err += 1
        print(color.RED, " - Bad Epitech's header in the file {}{}\n"
              .format(color.BLUE, _file.get_name()))
    return


def check_pointers(_file):
    """ Checks pointers location """

    nb_line = 1
    for line in _file.get_content():
        match = re.search(r"(int|signed|unsigned|char|long|short|float|double|void|const|struct)\*.*", line)
        if match:
            _file._err += 1
            display_err("Missplaced pointer *", nb_line, _file.get_name(), match.group())
        nb_line += 1
    return


def check_keyword_space(_file):
    """ Checks space after keyword """

    nb_line = 1
    for line in _file.get_content():
        match = re.search(r"(if|else if|else|for|while|switch|return)\(.*", line)
        if match:
            _file._err += 1
            display_err("Missing space after keyword",
                        nb_line, _file.get_name(), match.group())
        nb_line += 1


def display_err(msg, nb_line, filename, err=None):
    """ Display error coding style """

    if err:
        print(color.RED, " - {}\
        {}\n\t- Line : {}\
        \n\t- Error : {}\
        \n\t- File : {}\n".format(msg, color.BLUE, nb_line, err, filename))
    else:
        print(color.RED, " - {}\
        {}\n\t- Line : {}\
        \n\t- File : {}\n".format(msg, color.BLUE, nb_line, filename))


def check_if_else(_file):
    """ Checks if's forest """

    count = 0
    nb_line = 1
    for line in _file.get_content():
        line = line.lstrip()
        if line.startswith("if"):
            count = 1
        elif "else if" in line or "else" in line:
            count += 1
            if count > 3:
                _file._err += 1
                display_err("Too many if/else", nb_line, _file.get_name())
        nb_line += 1
    return


def check_coma_spaces(_file):
    """ Checks spaces around comas. """

    nb_line = 1
    for line in _file.get_content():
        match = re.search(r",\S", line)
        if match:
            _file._err += 1
            display_err("Missing space around ','", nb_line, _file.get_name(), match.group())
        nb_line += 1
    return


def check_op_space(_file):
    """ Checks spaces around operator. """

    operators = ['==', '!=', '\<=', '\>=', '&&', '\|\|', '\+=', '-=', '\*=', '/=', '=', '\+', '-', '%', '\<', '\>']
    nb_line = 1
    re_str = "|".join(["([^ ]{}[^ ])|([^ ]{} )|( {}[^ ])".format(ope, ope, ope) for ope in operators])

    for line in _file.get_content():
        res = re.compile(re_str)
        match = res.search(line)
        if match and match.group().lstrip() not in operators:
            _file._err += 1
            display_err("Missing spaces around operator", nb_line, _file.get_name(), match.group())
        nb_line += 1
    return


def check_trailing_spaces(_file):
    """ Checks trailing spaces """

    nb_line = 1
    for line in _file.get_content():
        line = line.lstrip()
        if not is_comment(line):
            match = re.search("(.*[ ]{1,}$)|(.*[\t]{1,}$)", line)
            if match:
                _file._err += 1
                display_err("Trailing space at end of line", nb_line, _file.get_name(), match.group())
        nb_line += 1
    return


def is_comment(line):
    """ Checks if line is a comment """
    return line.startswith("//") or line.startswith("/*") or line.startswith("*/") or line.startswith("**")


def check_useless_files():
    """ Checks useless files in dir/subdir """
    useless = [".c", ".h", ".hpp", ".cpp", "Makefile"]
    files = glob.glob("./**/*", recursive=True)

    to_del = []
    for _file in files:
        if os.path.isdir(_file) or os.path.splitext(_file)[1] in useless:
            to_del.append(_file)
    files = set(files) - set(to_del)
    nb = len(files)
    if nb > 0:
        print(color.RED, " - Files that shouldn't be commited :", color.RESET)
        for _file in files:
            print("\t{} - {}".format(color.BLUE, _file))
    return nb


def check_funcion_lines(_file):
    """ Checks number of line in function """

    nb_line = 1
    count = 0
    search = False
    for line in _file.get_content():
        if re.search(r"^{.*$", line):
            search = True
            count = 1
        if re.search(r"^}.*", line):
            search = False
        if search:
            count += 1
        nb_line += 1
        if count > 20:
            search = False
            count = 1
            _file._err += 1
            display_err("More than 20 lines in a function", nb_line, _file.get_name())


def moulilol():
    """ Moulilol """

    files = get_files("c") + get_files("h") + get_files("hpp") + get_files("cpp")
    final = 0

    print("{}\n! Coding Style Checker !\n{}".format(color.CYAN, color.RESET))

    for element in files:
        _file = File(element)
        check_columns(_file)
        if _file.get_type() == "SOURCE":
            check_nb_functions(_file)
            check_pointers(_file)
            check_keyword_space(_file)
            check_if_else(_file)
            check_op_space(_file)
            check_funcion_lines(_file)
        check_epitech_header(_file)
        check_coma_spaces(_file)
        check_trailing_spaces(_file)
        final += _file.get_nb_err()
    final += check_useless_files()
    if final:
        print(color.RED, """
---------------------------------------
        Coding Style Error : {}
---------------------------------------{}""".format(final, color.RESET))
    else:
        print(color.GREEN, "Norme OK", color.RESET)

if __name__ == "__main__":
    moulilol()
