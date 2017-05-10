#!/usr/bin/python

#randomly mix two fastq files
import docopt, sys
import os
import subprocess


USAGE = """
    Usage:
    	ransomly_mix_fastq.py --file1_pair1 <file1_pair1> --file1_pair2 <file1_pair2> --file2_pair1 <file2_pair1> --file2_pair2 <file2_pair2> --out <out> --fraction <fraction>

    Description:
        Tool accepts the two paired-end inputs (file1 and file2) and a 0-1 number for the fraction of reads to sample from file2 and merge into file1.
        the output is a fastq files (out_1.fastq and out_2.fastq) containing the reads of file1 with a proportion of reads downsampled from file2

    Options:

        --help                              Show help dialog
        --version                           Tool version.
        --file1_pair1 <file1_pair1>   the input file1 - first pair
        --file1_pair2 <file1_pair2>   the input file1 - second pair
        --file2_pair1 <file2_pair1>   the input file2 - first pair
        --file2_pair2 <file2_pair2>   the input file2 - second pair
        --fraction <fraction>	a floating point number from 0 to 1 indicating the fraction of reads to downsample from file2.  
        --out <out> the prefix of the output file name. Name will be out_1.fastq and out_2.fastq

"""


def main():

	#parse arguments
    args = docopt.docopt(USAGE, version = 1.0)
    print args
    file2_pair1 = args["--file2_pair1"]
    file2_pair2 = args["--file2_pair2"]
    file1_pair1 = args["--file1_pair1"]
    file1_pair2 = args["--file1_pair2"]
    fraction = args["--fraction"]
    out = args["--out"]

    if file1_pair1.endswith(".gz"):
        out_1 = out+"_1.fastq.gz"
        out_2 = out+"_2.fastq.gz"
    else:
        out_1 = out+"_1.fastq"
        out_2 = out+"_2.fastq"
    


    file2_temp_pair1 = file2_pair1+".tmp"
    file2_temp_pair2 = file2_pair2+".tmp"

    #downsample reads
    command1 = "seqtk sample -s100 %s %s > %s" %(file2_pair1, fraction, file2_temp_pair1)
    sys.stderr.write(command1 + "\n")
    subprocess.check_call(command1, shell=True)
    
    command2 = "seqtk sample -s100 %s %s > %s" %(file2_pair2, fraction, file2_temp_pair2)
    sys.stderr.write(command2 + "\n")
    subprocess.check_call(command2, shell=True)

    #merge fastq files
    command1 = "cat %s %s > %s" %(file1_pair1, file2_temp_pair1, out_1)
    sys.stderr.write(command1 + "\n")
    subprocess.check_call(command1, shell=True)

    command2 = "cat %s %s > %s" %(file1_pair2, file2_temp_pair2, out_2)
    sys.stderr.write(command2 + "\n")
    subprocess.check_call(command2, shell=True)

    #delete temp file
    command1 = "rm %s" %file2_temp_pair1
    subprocess.check_call(command1, shell=True)
    command2 = "rm %s" %file2_temp_pair2
    subprocess.check_call(command2, shell=True)


if __name__ == '__main__':
    main()


#EXAMPLE
#python randomly_mix_fastq.py --file1_pair1 bulk_RNA1.fastq --file1_pair2 bulk_RNA2.fastq --file2_pair1 scRNA_1.fastq --scRNA_2 ERR1146421_2.fastq --fraction 0.15 --out examplerun





