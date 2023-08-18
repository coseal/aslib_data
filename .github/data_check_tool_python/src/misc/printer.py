'''
Created on Nov 5, 2012

@author: Marius Lindauer
'''

import sys

class Printer(object):
    '''
        Printer prints all stdout and stderr messages
    '''
    
    verbose = 1
    disable_printing = False
    disable_warning = False
    _comment = "c "
    _comment = "% "

    def __init__(self):
        '''
        Constructor
        '''
        
    @staticmethod
    def print_c(str_):
        '''
            print comment on stdout
        '''
        if not Printer.disable_printing:
            sys.stdout.write(Printer._comment+("\n"+Printer._comment).join(str_.split("\n"))+"\n")
    
    @staticmethod
    def print_n(str_, line_break=True):
        '''
            print comment on stdout
        '''
        if not Printer.disable_printing:
            sys.stdout.write("\n".join(str_.split("\n")))
            if line_break:
                sys.stdout.write("\n")
    
    @staticmethod
    def print_e(str_,exit_code=-1):
        '''
            print error on stderr
            exit program
        '''
        sys.stderr.write("[ERROR]: "+str_+"\n")
        sys.exit(exit_code)
        
    @staticmethod        
    def print_w(str_):
        '''
            print warning on stderr
        '''
        if not Printer.disable_printing and not Printer.disable_warning:
            sys.stderr.write(Printer._comment+"[WARNING]: "+str_+"\n")
        
    @staticmethod
    def print_nearly_verbose(str_):
        '''
            write comment on stdout if verbose level is at least 1
        '''
        if Printer.verbose >= 1:
            Printer.print_c(str_)
            
    @staticmethod 
    def print_verbose(str_):
        '''
            write comment on stdout if verbose level is at least 2
        '''
        if Printer.verbose >= 2:
            Printer.print_c(str_)
            
    @staticmethod 
    def print_verbose_debug(str_):
        '''
            write comment on stdout if verbose is active
        '''
        if Printer.verbose == -1:
            Printer.print_c(str_)