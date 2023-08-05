import sys

from .. import api

from Bio import bgzf

description = f"""
#################################
# Write a BGZF compressed file. #
#################################

BGZF (Blocked GNU Zip Format) is a modified form of gzip compression which can be applied to any file format to provide compression with efficient random access.

In addition to being required for random access to and writing of BAM files, the BGZF format can also be used for most of the sequence data formats (e.g. FASTA, FASTQ, GenBank, VCF, MAF).

The command will look for stdin if there are no arguments.

Usage examples:
  $ fuc {api.common._script_name()} in.vcf > out.vcf.gz
  $ cat in.vcf | fuc {api.common._script_name()} > out.vcf.gz
"""

def create_parser(subparsers):
    parser = api.common._add_parser(
        subparsers,
        api.common._script_name(),
        help='Write a BGZF compressed file.',
        description=description,
    )
    parser.add_argument(
        'file',
        nargs='*',
        help='File to be compressed (default: stdin).'
    )

def main(args):
    if args.file:
        with open(args.file[0]) as f:
            data = f.read()
    elif not sys.stdin.isatty():
        data = sys.stdin.read()
    else:
        raise ValueError('No input data detected')

    w = bgzf.BgzfWriter(fileobj=sys.stdout.buffer)
    w.write(data)
    w.close()
