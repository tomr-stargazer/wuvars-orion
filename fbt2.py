''' 
This is a procedure to find bad timestamps. 
It is different from "find_bad_timestamps" 
and is therefore named fbt2.

The principle is to take "constant" stars, compute the offsets 
of each from their mean magnitude, and STACK THEM ALL TOGETHER. 
Nights that are offset from zero will stand out like a 
sore thumb, hopefully.

Of course, the definition of "constant" stars may already be 
prey to these bad nights, so one can never really know. But whatevs.
'''

def stacker(data, lookup):
    ''' Stacks lightcurves for constant stars and outputs the stacked LC.

    Inputs:
      - data: an ATpy table with lightcurve data
      - lookup: a variability stats table (spreadsheet) with only data 
                on "constant" stars.

    Outputs:
      - out_table: an ATpy table with columns corresponding to 
                   MEANMJDOBS, JAPERMAG3, HAPERMAG3, and KAPERMAG3
                   showing the stacked offset for each night.
                   Then we can clip them!
                   '''

#def remover(
