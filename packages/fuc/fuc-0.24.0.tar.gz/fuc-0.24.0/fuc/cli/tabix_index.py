import sys

from .. import api

import pysam

description = f"""
############################################
# Index a GFF/BED/SAM/VCF file with Tabix. #
############################################

The Tabix program is used to index a TAB-delimited genome position file (GFF/BED/SAM/VCF) and create an index file (.tbi). The input data file must be position sorted and compressed by bgzip.

Usage examples:
  $ fuc {api.common._script_name()} in.gff.gz
  $ fuc {api.common._script_name()} in.bed.gz
  $ fuc {api.common._script_name()} in.sam.gz
  $ fuc {api.common._script_name()} in.vcf.gz
"""

def create_parser(subparsers):
    parser = api.common._add_parser(
        subparsers,
        api.common._script_name(),
        help='Index a GFF/BED/SAM/VCF file with Tabix.',
        description=description,
    )
    parser.add_argument(
        'file',
        help='File to be indexed.'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force to overwrite the index file if it is present.'
    )

def main(args):
    if '.vcf' in args.file:
        preset = 'vcf'
    elif '.sam' in args.file:
        preset = 'sam'
    elif '.gff' in args.file:
        preset = 'gff'
    elif '.bed' in args.file:
        preset = 'bed'
    else:
        raise ValueError('Unsupported file format')

    pysam.tabix_index(args.file, preset=preset, force=args.force)
