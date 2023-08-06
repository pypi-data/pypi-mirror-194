# Copyright (c) 2021, Google Inc.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# 3. Neither the name of Google Inc. nor the names of its contributors
#    may be used to endorse or promote products derived from this software without
#    specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""Tests for deepconsensus.preprocess.preprocess_utils."""

import collections
import textwrap
from typing import List

from absl.testing import absltest
from absl.testing import parameterized
import numpy as np
import pysam

from deepconsensus.models import data_providers
from deepconsensus.preprocess import pre_lib
from deepconsensus.utils import dc_constants
from deepconsensus.utils import test_utils
from deepconsensus.utils.test_utils import deepconsensus_testdata

Strand = dc_constants.Strand
Issue = dc_constants.Issue

# pyformat: disable pylint: disable=bad-continuation
TEST_HEADER = pysam.AlignmentHeader.from_dict(
    collections.OrderedDict({
        'HD': {'VN': '1.5', 'SO': 'unknown', 'pb': '3.0.7'},
        'SQ': [
            {'SN': 'm64138_200228_003250/18/ccs', 'LN': 100},
            {'SN': 'm64138_200228_003250/23/ccs', 'LN': 100},
        ],
        'RG': [{
            'ID': 'rg1',
            'PL': 'PACBIO',
            'DS': 'READTYPE=SUBREAD',
            'PU': 'm64138_200228_003250',
            'PM': 'SEQUELII',
        }],
    })
)
# pyformat: enable pylint: enable=bad-continuation


def create_segment(
    bases: str,
    cigar: str,
    ip: List[int] = None,
    pw: List[int] = None,
    sn: List[int] = None,
    is_reverse: bool = False,
    reference_name: str = TEST_HEADER.references[0],
    reference_start: int = 0,
    name: str = None,
) -> pysam.AlignedSegment:
  """Generates a pysam AlignedSegment."""
  segment = pysam.AlignedSegment(header=TEST_HEADER)
  segment.qname = name
  segment.seq = bases
  segment.qual = pysam.qualities_to_qualitystring(np.repeat(1, len(bases)))
  segment.set_tag('ip', ip or [1] * len(bases))
  segment.set_tag('pw', pw or [2] * len(bases))
  segment.set_tag('sn', sn or [0.5] * 4)
  segment.cigarstring = cigar
  segment.is_reverse = is_reverse
  segment.reference_name = reference_name
  segment.reference_start = reference_start
  return segment


class TestSubreadGrouper(absltest.TestCase):

  def test_read_bam(self):
    subread_to_ccs = test_utils.deepconsensus_testdata(
        'human_1m/subreads_to_ccs.bam'
    )
    zmw_subread_sets = pre_lib.SubreadGrouper(subread_to_ccs, 1)
    subread_count = 0
    zmw_count = 0
    for zmw_subreads in zmw_subread_sets:
      subread_count += len(zmw_subreads)
      zmw_count += 1
    self.assertEqual(subread_count, 93)
    self.assertEqual(zmw_count, 10)


class TestProcFeeder(absltest.TestCase):

  def test_proc_feeder_inference(self):
    subread_to_ccs = test_utils.deepconsensus_testdata(
        'human_1m/subreads_to_ccs.bam'
    )
    ccs_bam = test_utils.deepconsensus_testdata('human_1m/ccs.bam')
    dc_config = pre_lib.DcConfig(max_passes=20, max_length=100)
    proc_feeder, main_counter = pre_lib.create_proc_feeder(
        subreads_to_ccs=subread_to_ccs, ccs_bam=ccs_bam, dc_config=dc_config
    )
    ccs_seqnames = []
    n_subreads = 0
    for read_set, ccs_seqname, _, mode, _ in proc_feeder():
      ccs_seqnames.append(ccs_seqname)
      # Subtract 1 for CCS sequence
      n_subreads += len(read_set) - 1
      self.assertEqual(mode, 'inference')
    self.assertEqual(main_counter['n_zmw_processed'], 10)
    self.assertLen(set(ccs_seqnames), 10)
    self.assertEqual(n_subreads, 93)

  def test_proc_feeder_training(self):
    subreads_to_ccs = test_utils.deepconsensus_testdata(
        'human_1m/subreads_to_ccs.bam'
    )
    ccs_bam = test_utils.deepconsensus_testdata('human_1m/ccs.bam')

    # Training data
    truth_to_ccs = test_utils.deepconsensus_testdata(
        'human_1m/truth_to_ccs.bam'
    )
    truth_bed = test_utils.deepconsensus_testdata('human_1m/truth.bed')
    truth_split = test_utils.deepconsensus_testdata('human_1m/truth_split.tsv')

    dc_config = pre_lib.DcConfig(max_passes=20, max_length=100)
    proc_feeder, main_counter = pre_lib.create_proc_feeder(
        subreads_to_ccs=subreads_to_ccs,
        ccs_bam=ccs_bam,
        dc_config=dc_config,
        truth_to_ccs=truth_to_ccs,
        truth_bed=truth_bed,
        truth_split=truth_split,
    )
    ccs_seqnames = []
    n_subreads = 0
    for read_set, ccs_seqname, _, mode, _ in proc_feeder():
      ccs_seqnames.append(ccs_seqname)
      # Subtract 2: 1 for CCS, 1 for label
      n_subreads += len(read_set) - 2
      self.assertIn(mode, ['train', 'eval', 'test'])
    self.assertEqual(main_counter['n_zmw_processed'], 10)
    self.assertLen(set(ccs_seqnames), main_counter['n_zmw_pass'])
    self.assertEqual(n_subreads, 92)


class TestRightPad(parameterized.TestCase):

  def test_right_pad(self):
    x = np.repeat(1, 10)
    padded = pre_lib.right_pad(x, 20, 0)
    expected = np.concatenate([np.repeat(1, 10), np.repeat(0, 10)])
    self.assertTrue(np.array_equal(padded, expected))


class TestExpandClipIndent(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='alignment match',
          segment_args={'bases': 'ATCG', 'cigar': '4M'},
          expected_bases='ATCG',
          expected_cigar=[pysam.CMATCH] * 4,
      ),
      dict(
          testcase_name='insertion',
          segment_args={
              'bases': 'AAAATTTTAAAA',
              'cigar': '4M4I4M',
              'ip': [1] * 12,
              'pw': [2] * 12,
          },
          expected_bases='AAAATTTTAAAA',
          expected_cigar=[pysam.CMATCH] * 4
          + [pysam.CINS] * 4
          + [pysam.CMATCH] * 4,
          expected_ip=[1] * 12,
          expected_pw=[2] * 12,
      ),
      dict(
          testcase_name='deletion',
          segment_args={
              'bases': 'AAAAAAAA',
              'cigar': '4M4D4M',
              'ip': [1] * 4 + [1] * 4,
              'pw': [2] * 4 + [0] * 4,
          },
          expected_bases='AAAA    AAAA',
          expected_cigar=[pysam.CMATCH] * 4
          + [pysam.CDEL] * 4
          + [pysam.CMATCH] * 4,
          expected_ip=[1] * 4 + [0] * 4 + [1] * 4,
          expected_pw=[2] * 4 + [0] * 4 + [0] * 4,
      ),
      dict(
          testcase_name='skip region',
          segment_args={
              'bases': 'AAAAAAAA',
              'cigar': '4N8M',
              'ip': [1] * 8,
              'pw': [2] * 8,
          },
          expected_bases='    AAAAAAAA',
          expected_cigar=[pysam.CREF_SKIP] * 4 + [pysam.CMATCH] * 8,
          expected_ip=[0] * 4 + [1] * 8,
          expected_pw=[0] * 4 + [2] * 8,
      ),
      dict(
          testcase_name='subread with match insert match',
          segment_args={
              'bases': 'TTTTCGGAAC',
              'cigar': '5M5D5M',
              'ip': [1] * 10,
              'pw': [2] * 10,
          },
          expected_bases='TTTTC     GGAAC',
          expected_cigar=[pysam.CMATCH] * 5
          + [pysam.CDEL] * 5
          + [pysam.CMATCH] * 5,
          expected_ip=[1] * 5 + [0] * 5 + [1] * 5,
          expected_pw=[2] * 5 + [0] * 5 + [2] * 5,
      ),
      dict(
          testcase_name='subread with complex cigar',
          segment_args={
              'bases': 'TTTTCGGAACTTGGGAAGGG',
              'cigar': '5M5D5M5I5M',
              'ip': [1] * 20,
              'pw': [2] * 20,
          },
          expected_bases='TTTTC     GGAACTTGGGAAGGG',
          expected_cigar=[pysam.CMATCH] * 5
          + [pysam.CDEL] * 5
          + [pysam.CMATCH] * 5
          + [pysam.CINS] * 5
          + [pysam.CMATCH] * 5,
          expected_ip=[1] * 5 + [0] * 5 + [1] * 15,
          expected_pw=[2] * 5 + [0] * 5 + [2] * 15,
      ),
      dict(
          testcase_name='soft clip',
          segment_args={
              'bases': 'AAAATTTTAAAA',
              'cigar': '4S4M4S',
              'ip': [0] * 4 + [1] * 4 + [0] * 4,
              'pw': [0] * 4 + [2] * 4 + [0] * 4,
          },
          expected_bases='TTTT',
          expected_cigar=[pysam.CMATCH] * 4,
          expected_ip=[1] * 4,
          expected_pw=[2] * 4,
      ),
      dict(
          testcase_name='hard clip',
          segment_args={
              'bases': 'TTTT',
              'cigar': '4H4M4H',
              'ip': [1] * 4,
              'pw': [2] * 4,
          },
          expected_bases='TTTT',
          expected_cigar=[pysam.CMATCH] * 4,
          expected_ip=[1] * 4,
          expected_pw=[2] * 4,
      ),
      dict(
          testcase_name='bases match and mismatch',
          segment_args={
              'bases': 'AAAATTTTAAAA',
              'cigar': '4=4X4=',
              'ip': [1] * 12,
              'pw': [2] * 12,
          },
          expected_bases='AAAATTTTAAAA',
          expected_cigar=[pysam.CEQUAL] * 4
          + [pysam.CDIFF] * 4
          + [pysam.CEQUAL] * 4,
          expected_ip=[1] * 12,
          expected_pw=[2] * 12,
      ),
      dict(
          testcase_name='indent',
          segment_args={
              'bases': 'TTTT',
              'cigar': '4M',
              'reference_start': 4,
              'ip': [1] * 4,
              'pw': [2] * 4,
          },
          expected_bases='    TTTT',
          expected_cigar=[pysam.CREF_SKIP] * 4 + [pysam.CMATCH] * 4,
          expected_ip=[0] * 4 + [1] * 4,
          expected_pw=[0] * 4 + [2] * 4,
      ),
      dict(
          testcase_name='indent and soft',
          segment_args={
              'bases': 'AAAATTTT',
              'cigar': '4S4M',
              'reference_start': 4,
              'ip': [1] * 8,
              'pw': [2] * 8,
          },
          expected_bases='    TTTT',
          expected_cigar=[pysam.CREF_SKIP] * 4 + [pysam.CMATCH] * 4,
          expected_ip=[0] * 4 + [1] * 4,
          expected_pw=[0] * 4 + [2] * 4,
      ),
      dict(
          testcase_name='strand forward',
          segment_args={
              'bases': 'AAAA',
              'cigar': '4M',
              'is_reverse': False,
          },
          expected_bases='AAAA',
          expected_cigar=[pysam.CMATCH] * 4,
          expected_strand=Strand.FORWARD,
      ),
      dict(
          testcase_name='strand reverse',
          segment_args={
              'bases': 'AAAA',
              'cigar': '4M',
              'is_reverse': True,
          },
          expected_bases='AAAA',
          expected_cigar=[pysam.CMATCH] * 4,
          expected_strand=Strand.REVERSE,
      ),
      dict(
          testcase_name='strand reverse ip/pw values',
          segment_args={
              'bases': 'AAAA',
              'cigar': '4M',
              'ip': [1, 2, 3, 4],
              'pw': [1, 2, 3, 4],
              'is_reverse': True,
          },
          expected_bases='AAAA',
          expected_ip=[1, 2, 3, 4][::-1],
          expected_pw=[1, 2, 3, 4][::-1],
          expected_cigar=[pysam.CMATCH] * 4,
          expected_strand=Strand.REVERSE,
      ),
      dict(
          testcase_name='strand forward ip/pw values',
          segment_args={
              'bases': 'AAAA',
              'cigar': '4M',
              'ip': [1, 2, 3, 4],
              'pw': [1, 2, 3, 4],
              'is_reverse': False,
          },
          expected_bases='AAAA',
          expected_ip=[1, 2, 3, 4],
          expected_pw=[1, 2, 3, 4],
          expected_cigar=[pysam.CMATCH] * 4,
          expected_strand=Strand.FORWARD,
      ),
      dict(
          testcase_name='strand reverse with indent',
          segment_args={
              'bases': 'AAAA',
              'cigar': '4M',
              'ip': [1, 2, 3, 4],
              'pw': [1, 2, 3, 4],
              'is_reverse': True,
              'reference_start': 2,
          },
          expected_bases='  AAAA',
          expected_ip=[0, 0, 4, 3, 2, 1],
          expected_pw=[0, 0, 4, 3, 2, 1],
          expected_cigar=[pysam.CREF_SKIP] * 2 + [pysam.CMATCH] * 4,
          expected_strand=Strand.REVERSE,
      ),
      dict(
          testcase_name='strand forward with indent',
          segment_args={
              'bases': 'AAAA',
              'cigar': '4M',
              'ip': [1, 2, 3, 4],
              'pw': [1, 2, 3, 4],
              'is_reverse': False,
              'reference_start': 2,
          },
          expected_bases='  AAAA',
          expected_ip=[0, 0, 1, 2, 3, 4],
          expected_pw=[0, 0, 1, 2, 3, 4],
          expected_cigar=[pysam.CREF_SKIP] * 2 + [pysam.CMATCH] * 4,
          expected_strand=Strand.FORWARD,
      ),
  )
  def test_expand_clip_indent(
      self,
      segment_args,
      expected_bases,
      expected_cigar,
      expected_ip=None,
      expected_pw=None,
      expected_strand=None,
  ):
    segment = create_segment(**segment_args)
    subread = pre_lib.expand_clip_indent(segment)
    self.assertEqual(''.join(subread.bases[subread.cigar != 5]), expected_bases)
    # Compare cigars, removing hard-clipped ops.
    self.assertTrue((subread.cigar == expected_cigar).all())
    if expected_ip:
      self.assertEqual(list(subread.ip[subread.cigar != 5]), expected_ip)
      self.assertEqual(len(subread.bases), len(subread.ip))
    if expected_pw:
      self.assertEqual(list(subread.pw[subread.cigar != 5]), expected_pw)
      self.assertEqual(len(subread.bases), len(subread.pw))
    if expected_strand:
      self.assertEqual(expected_strand, subread.strand)


class TestTrimInsertions(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='insertion',
          segment_args={
              'bases': 'AAAATTTTTTAAAA',
              'cigar': '4M6I4M',
              'ip': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
              'pw': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
              'is_reverse': False,
          },
          expected_bases='AAAAAAAA',
          expected_cigar=[
              (dc_constants.PYSAM_CMATCH, 4),
              (dc_constants.PYSAM_CMATCH, 4),
          ],
          exptected_idx=[0, 1, 2, 3, 4, 5, 6, 7],
          # ip=10 is trimmed
          expected_ip=[1, 2, 3, 4, 11, 12, 13, 14],
          # pw=10 is trimmed
          expected_pw=[1, 2, 3, 4, 11, 12, 13, 14],
          expected_strand=False,  # is_reversed
          expected_zmw_trimmed_insertions=1,
          expected_zmw_trimmed_insertions_bp=6,
      ),
      dict(
          testcase_name='insertion_reversed',
          segment_args={
              'bases': 'ATTTTTTAAAA',
              'cigar': '1M6I4M',
              'ip': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
              'pw': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
              'is_reverse': True,
          },
          expected_bases='AAAAA',
          expected_cigar=[
              (dc_constants.PYSAM_CMATCH, 1),
              (dc_constants.PYSAM_CMATCH, 4),
          ],
          exptected_idx=[0, 1, 2, 3, 4],
          # ip=5 is trimmed
          expected_ip=[1, 2, 3, 4, 11],
          # pw=5 is trimmed
          expected_pw=[1, 2, 3, 4, 11],
          expected_strand=True,  # is_reversed
          expected_zmw_trimmed_insertions=1,
          expected_zmw_trimmed_insertions_bp=6,
      ),
      dict(
          testcase_name='insertion_no_trim',
          segment_args={
              'bases': 'AAAATTTTTTAAAA',
              'cigar': '4M6I4M',
              'ip': [1] * 14,
              'pw': [2] * 14,
              'is_reverse': False,
          },
          expected_bases='AAAATTTTTTAAAA',
          expected_cigar=[
              (dc_constants.PYSAM_CMATCH, 4),
              (dc_constants.PYSAM_CINS, 6),
              (dc_constants.PYSAM_CMATCH, 4),
          ],
          exptected_idx=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
          expected_ip=[1] * 14,
          expected_pw=[2] * 14,
          expected_strand=False,  # is_reversed
          ins_trim=0,
          expected_zmw_trimmed_insertions=0,
          expected_zmw_trimmed_insertions_bp=0,
      ),
      dict(
          testcase_name='deletion',
          segment_args={
              'bases': 'AAAAAAAA',
              'cigar': '4M6D4M',
              'ip': [1] * 8,
              'pw': [2] * 8,
              'is_reverse': False,
          },
          expected_bases='AAAAAAAA',
          expected_cigar=[
              (dc_constants.PYSAM_CMATCH, 4),
              (dc_constants.PYSAM_CDEL, 6),
              (dc_constants.PYSAM_CMATCH, 4),
          ],
          exptected_idx=[
              0,
              1,
              2,
              3,
              None,
              None,
              None,
              None,
              None,
              None,
              4,
              5,
              6,
              7,
          ],
          expected_ip=[1] * 8,
          expected_pw=[2] * 8,
          expected_strand=False,  # is_reversed
          expected_zmw_trimmed_insertions=0,
          expected_zmw_trimmed_insertions_bp=0,
      ),
  )
  def test_trim_insertions(
      self,
      segment_args,
      expected_bases,
      expected_cigar,
      exptected_idx=None,
      expected_ip=None,
      expected_pw=None,
      expected_strand=None,
      expected_zmw_trimmed_insertions=None,
      expected_zmw_trimmed_insertions_bp=None,
      ins_trim=5,
  ):
    segment = create_segment(**segment_args)
    counter = collections.Counter()
    trimmed_segment = pre_lib.trim_insertions(
        read=segment, ins_trim=ins_trim, counter=counter
    )
    self.assertEqual(trimmed_segment.query_sequence, expected_bases)
    aligned_pairs = trimmed_segment.get_aligned_pairs()
    self.assertListEqual(trimmed_segment.cigartuples, expected_cigar)
    if exptected_idx:
      read_idx = [x[0] for x in aligned_pairs]
      self.assertListEqual(read_idx, exptected_idx)
    if expected_ip:
      self.assertEqual(list(trimmed_segment.get_tag('ip')), expected_ip)
    if expected_pw:
      self.assertListEqual(list(trimmed_segment.get_tag('pw')), expected_pw)
    if expected_strand:
      self.assertEqual(expected_strand, trimmed_segment.is_reverse)
    if expected_zmw_trimmed_insertions:
      self.assertEqual(
          counter['zmw_trimmed_insertions'], expected_zmw_trimmed_insertions
      )
    if expected_zmw_trimmed_insertions_bp:
      self.assertEqual(
          counter['zmw_trimmed_insertions_bp'],
          expected_zmw_trimmed_insertions_bp,
      )


class TestCcsRead(absltest.TestCase):

  def test_fetch_ccs_read(self):
    # Test that we can construct a ccs read object with quality scores.
    test_bam = deepconsensus_testdata('human_1m/ccs.bam')
    ccs_bam_h = pysam.AlignmentFile(test_bam, check_sq=False)
    ccs_bam_read = next(ccs_bam_h)
    seq_name = 'm54238_180901_011437/4194375/ccs'
    read = pre_lib.construct_ccs_read(ccs_bam_read)
    self.assertEqual(seq_name, read.name)
    self.assertGreater(read.avg_base_quality_score, 0)
    self.assertTrue((read.base_quality_scores > 0).any())
    self.assertIsNotNone(read.ec)
    self.assertIsNotNone(read.np_num_passes)
    self.assertIsNotNone(read.rq)


class TestFetchLabelBases(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='known label bases',
          ccs_name='m64014_181210_152538/29/ccs',
          expected_label_name='m64014_181210_152538/29/truth',
      ),
      dict(
          testcase_name='unknown label',
          ccs_name='m64014_181210_152538/-1/ccs',
          expected_label_name=Issue.TRUTH_ALIGNMENT_NOT_FOUND.name,
      ),
  )
  def test_fetch_bases(self, ccs_name, expected_label_name):
    test_truth_to_ccs = deepconsensus_testdata('preprocess/truth_to_ccs.bam')
    tests_bam = pysam.AlignmentFile(test_truth_to_ccs)
    label = pre_lib.fetch_label_alignment(
        ccs_name, tests_bam, {'contig': 'fake_chr', 'begin': 0, 'end': 0}
    )
    label_name = label.name
    self.assertEqual(label_name, expected_label_name)
    if isinstance(label, pre_lib.Read):
      self.assertEqual(label.zmw, int(label.name.split('/')[1]))
      self.assertTrue(label.is_label)


def split_alignment(text):
  # Transforms simple representations of bases, cigars, and expected alignments
  return [x.rstrip() for x in textwrap.dedent(text).splitlines() if x.strip()]


class TestSpaceOutSubreads(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='two subreads with same sequence',
          bases="""
            AAAA
            AAAA
          """,
          cigars="""
            MMMM
            MMMM
          """,
          expected="""
            AAAA
            AAAA
          """,
      ),
      dict(
          testcase_name='two subreads with different lengths',
          bases="""
            ACTA
            ACTAG
          """,
          cigars="""
            MMMM
            MMMMM
          """,
          expected="""
            ACTA
            ACTAG
          """,
      ),
      dict(
          testcase_name='two subreads with one I',
          bases="""
            ACTG
            ACTAG
          """,
          cigars="""
            MMMM
            MMMIM
          """,
          expected="""
            ACT G
            ACTAG
          """,
      ),
      dict(
          testcase_name='two subreads with one D',
          bases="""
            ACTGG
            ACT G
          """,
          cigars="""
            MMMMM
            MMMDM
          """,
          expected="""
            ACTGG
            ACT G
          """,
      ),
      dict(
          testcase_name='complex alignment case',
          bases="""
           TTTTT
           TTTTT
           TTTTT
          """,
          cigars="""
           MIMIM
           MMMMM
           MIMIM
          """,
          expected="""
           TTTTT
           T T TTT
           TTTTT
          """,
      ),
      dict(
          testcase_name='adjacent insertions',
          bases="""
           TTTTT
           TTTTT
           TTTTT
          """,
          cigars="""
           MIIIM
           MMMMM
           MIIIM
          """,
          expected="""
           TTTTT
           T   TTTT
           TTTTT
          """,
      ),
      dict(
          testcase_name='ignore label insertion',
          bases="""
           TTTTT
           TTTTT
           TTTTT
           TTGGGTTT
          """,
          cigars="""
           MMMMM
           MMMMM
           MMMMM
           MMIIIMMM
          """,
          expected="""
           TTTTT
           TTTTT
           TTTTT
           TTGGGTTT
          """,
          ccs_idx=[
              [0, 1, 2, 3, 4],
              [0, 1, 2, 3, 4],
              [0, 1, 2, 3, 4],
              [0, 1, 2, -1, -1, -1, 3, 4],
          ],
          truth_range={'contig': 'chr1', 'begin': 0, 'end': 8},
      ),
      dict(
          testcase_name='insertion at end of label',
          bases="""
           TTTTT
           TTTTT
           TTTTT
           TTTTTGG
          """,
          cigars="""
           MMMMM
           MMMMM
           MMMMM
           MMMMMII
          """,
          expected="""
           TTTTT
           TTTTT
           TTTTT
           TTTTTGG
          """,
          ccs_idx=[
              [0, 1, 2, 3, 4],
              [0, 1, 2, 3, 4],
              [0, 1, 2, 3, 4],
              [0, 1, 2, 3, 4, -1, -1],
          ],
          truth_range={'contig': 'chr1', 'begin': 0, 'end': 7},
      ),
  )
  def test_space_out_subreads(
      self, bases, cigars, expected, ccs_idx=None, truth_range=None
  ):
    # Construct reads
    subreads = []
    read_set = list(zip(split_alignment(bases), split_alignment(cigars)))
    for i, (bases, cigar) in enumerate(read_set):
      cigar = np.array([dc_constants.CIGAR_OPS[x] for x in list(cigar)])
      if ccs_idx:
        read_ccs_idx = ccs_idx[i]
      else:
        read_ccs_idx = np.arange(len(bases))
      # The truth range is only passed in for the label read
      # (which should always be the last read)
      read = pre_lib.Read(
          name='',
          bases=np.array(list(bases)),
          cigar=cigar,
          ip=[0] * len(bases),
          pw=[0] * len(bases),
          sn=[0.0] * 4,
          strand=dc_constants.Strand.UNKNOWN,
          ccs_idx=read_ccs_idx,
          # The truth range is only specified for the label read.
          truth_range=truth_range if i == len(read_set) - 1 else None,
      )
      subreads.append(read)
    # Run space out subreads
    spaced_subreads = pre_lib.space_out_subreads(subreads)
    spaced_subreads = list(
        map(lambda x: ''.join(x.bases).rstrip(), spaced_subreads)
    )
    self.assertEqual(spaced_subreads, split_alignment(expected))


class TestBounds(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='simple match',
          bases='AAAAATTTTT',
          cigar='10M',
          reference_start=0,
          expected_ccs_bounds=(0, 9),
          slice_bounds=(5, 8),
          expected_ccs_slice_bounds=(5, 8),
      ),
      dict(
          testcase_name='shifted start pos match',
          bases='AAAAATTTTT',
          cigar='10M',
          reference_start=1,
          expected_ccs_bounds=(1, 10),
          slice_bounds=(5, 8),
          expected_ccs_slice_bounds=(5, 8),
      ),
      dict(
          testcase_name='right side of slice beyond bound',
          bases='AAAAATTTTT',
          cigar='10M',
          reference_start=0,
          expected_ccs_bounds=(0, 9),
          slice_bounds=(5, 200),
          expected_ccs_slice_bounds=(5, 9),
      ),
      dict(
          testcase_name='left side of slice beyond bound',
          bases='AAAAATTTTT',
          cigar='10M',
          reference_start=10,
          expected_ccs_bounds=(10, 19),
          slice_bounds=(5, 15),
          expected_ccs_slice_bounds=(10, 15),
      ),
      dict(
          testcase_name='bounds extend beyond ccs',
          bases='AAAAATTTTT',
          cigar='10M',
          reference_start=10,
          expected_ccs_bounds=(10, 19),
          slice_bounds=(5, 25),
          expected_ccs_slice_bounds=(10, 19),
      ),
      dict(
          testcase_name='no overlap slice',
          bases='AAAAATTTTT',
          cigar='10M',
          reference_start=10,
          expected_ccs_bounds=(10, 19),
          slice_bounds=(100, 200),
          expected_ccs_slice_bounds=(0, 0),
      ),
      dict(
          testcase_name='label alignment with softmatch ends',
          bases='GGAAAAATTTTTGG',
          cigar='2S10M2S',
          reference_start=0,
          expected_ccs_bounds=(0, 9),
          slice_bounds=(5, 8),
          expected_ccs_slice_bounds=(5, 8),
          truth_range={'contig': 'chr1', 'begin': 0, 'end': 14},
          expected_label_bounds=slice(2, 11),
          expected_label_slice_bounds=slice(7, 10),
      ),
      dict(
          testcase_name='label alignment with insertions and softmatch ends',
          bases='GGAAAAATTTAAGG',
          cigar='2S5M3I2M2S',
          reference_start=0,
          expected_ccs_bounds=(0, 6),
          slice_bounds=(4, 8),
          expected_ccs_slice_bounds=(4, 6),
          truth_range={'contig': 'chr1', 'begin': 0, 'end': 14},
          expected_label_bounds=slice(2, 11),
          expected_label_slice_bounds=slice(6, 11),
      ),
      dict(
          testcase_name='label alignment with deletions and softmatch ends',
          bases='GGAAAAAAAGG',
          cigar='2S5M3D2M2S',
          reference_start=0,
          expected_ccs_bounds=(0, 9),
          slice_bounds=(2, 6),
          expected_ccs_slice_bounds=(2, 6),
          truth_range={'contig': 'chr1', 'begin': 0, 'end': 11},
          expected_label_bounds=slice(2, 8),
          expected_label_slice_bounds=slice(4, 6),
      ),
  )
  def test_ccs_bounds(
      self,
      bases,
      cigar,
      reference_start,
      slice_bounds,
      expected_ccs_bounds,
      expected_ccs_slice_bounds,
      truth_range=None,
      expected_label_bounds=None,
      expected_label_slice_bounds=None,
  ):
    segment = create_segment(
        bases=bases, cigar=cigar, reference_start=reference_start
    )
    read = pre_lib.expand_clip_indent(segment, truth_range)
    # run space_out_subreads to generate truth_idx
    read = pre_lib.space_out_subreads([read])[0]
    # Bound test
    self.assertEqual(read.ccs_bounds, slice(*expected_ccs_bounds))
    # Slice test
    sliced_read = read.ccs_slice(*slice_bounds)
    self.assertEqual(sliced_read.ccs_bounds, slice(*expected_ccs_slice_bounds))
    if truth_range:
      self.assertNotEmpty(read.label_coords)
      self.assertEqual(read.label_bounds, expected_label_bounds)
      self.assertEqual(sliced_read.label_bounds, expected_label_slice_bounds)
    else:
      self.assertEmpty(read.label_coords)
      self.assertEqual(read.label_bounds, slice(0, 0))


class TestEncodeDecodeBases(absltest.TestCase):

  def test_encode_decode_bases(self):
    bases = 'TTGTGGAGAT'
    cigar = '5M1D5M'
    segment = create_segment(bases=bases, cigar=cigar, reference_start=0)
    read = pre_lib.expand_clip_indent(segment)
    encoded_bases = np.array([2, 2, 4, 2, 4, 0, 4, 1, 4, 1, 2])
    self.assertTrue((read.bases_encoded == encoded_bases).all())
    decoded_bases = pre_lib.decode_bases(np.expand_dims(encoded_bases, 0))
    decoded_bases = ''.join(decoded_bases[0]).replace(' ', '')
    self.assertTrue(bases, decoded_bases)


class TestDcConfig(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='max_passes=5',
          max_passes=5,
          max_length=5,
          expected_ip_slice=slice(10, 13),
          expected_total_rows=25,
      ),
      dict(
          testcase_name='max_passes=20',
          max_passes=20,
          max_length=5,
          expected_ip_slice=slice(40, 43),
          expected_total_rows=85,
      ),
  )
  def test_dc_config(
      self, max_passes, max_length, expected_ip_slice, expected_total_rows
  ):
    dc_config = pre_lib.DcConfig(max_passes=max_passes, max_length=max_length)
    ip_start = dc_config.indices('ip', 3).start
    self.assertEqual(dc_config.indices('ip', 3), expected_ip_slice)
    self.assertEqual(
        dc_config.indices('ip', 100), slice(ip_start, ip_start + max_passes)
    )
    self.assertEqual(dc_config.tensor_height, expected_total_rows)
    self.assertEqual(dc_config.max_length, max_length)


class TestDcConfigFromShape(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='standard shape use_ccs_bq=True',
          shape=(86, 120, -1),
          use_ccs_bq=True,
          expected_max_passes=20,
          expected_sn_rows=slice(82, 86),
      ),
      dict(
          testcase_name='expanded shape use_ccs_bq=True',
          shape=(106, 120, -1),
          use_ccs_bq=True,
          expected_max_passes=25,
          expected_sn_rows=slice(102, 106),
      ),
      dict(
          testcase_name='standard shape use_ccs_bq=False',
          shape=(85, 120, -1),
          use_ccs_bq=False,
          expected_max_passes=20,
          expected_sn_rows=slice(81, 85),
      ),
      dict(
          testcase_name='expanded shape use_ccs_bq=False',
          shape=(105, 120, -1),
          use_ccs_bq=False,
          expected_max_passes=25,
          expected_sn_rows=slice(101, 105),
      ),
  )
  def test_dc_config_from_shape(
      self,
      shape,
      use_ccs_bq,
      expected_max_passes,
      expected_sn_rows,
  ):
    dc_config = pre_lib.dc_config_from_shape(shape, use_ccs_bq)
    self.assertEqual(dc_config.max_passes, expected_max_passes)
    self.assertEqual(dc_config.indices('sn'), expected_sn_rows)

  def test_incompatible_shape(self):
    with self.assertRaisesRegex(ValueError, 'Invalid subreads shape'):
      pre_lib.dc_config_from_shape((7, 7, -1), use_ccs_bq=True)


class TestDcExampleFunctionality(parameterized.TestCase):

  def test_dc_example_functions(self):
    max_length = 9
    dc_config = pre_lib.DcConfig(
        max_passes=20,
        max_length=max_length,
        use_ccs_bq=True,
    )
    # First, generate a bunch of reads
    read_set = []
    num_of_subreads = 10
    for i in range(num_of_subreads):
      segment = create_segment(
          name=f'm0/1/{i}', bases='A' * 10, cigar='10M', reference_start=0
      )
      read = pre_lib.expand_clip_indent(segment)
      read_set.append(read)
    label_segment = create_segment(
        name='m0/1/truth', bases='A' * 10, cigar='10M', reference_start=0
    )
    truth_range = {'contig': 'chr1', 'begin': 0, 'end': 10}
    label = pre_lib.expand_clip_indent(label_segment, truth_range)
    read_set += [label]
    dc_example = pre_lib.subreads_to_dc_example(
        read_set, 'm0/1/ccs', dc_config, None
    )

    # Set CCS Base qualities
    dc_example.ccs.base_quality_scores = np.repeat(1, 10)

    # contig
    self.assertEqual(
        dc_example.contig,
        truth_range['contig'],
        msg='test dc_example.contig name matches truth_range.',
    )

    # subreads
    self.assertEqual(dc_example.n_subreads, 9)
    self.assertLen(dc_example.subreads, 9)

    # ccs
    self.assertEqual(
        repr(dc_example.ccs).strip(), 'Read(m0/1/9) : CCS(0-9) L=10'
    )

    # label
    self.assertEqual(
        repr(dc_example.label).strip(),
        'Read(m0/1/truth) : CCS(0-9) L=10 chr1:0-9',
    )

    # dc_example repr
    self.assertEqual(
        repr(dc_example).splitlines()[2].split(), ['0', '1', '>AAAAAAAAAA']
    )

    # dc_example slicing:
    self.assertEqual(
        repr(dc_example[:5]).splitlines()[2].split(), ['0', '1', '>AAAAA']
    )

    self.assertTrue(dc_example.is_training)

    # dc_example iterate windows
    examples = dc_example.iter_examples()
    example = next(examples)
    self.assertEqual(
        repr(example).splitlines()[2].split(), ['0', '1', '>AAAAAAAAA']
    )
    example = next(examples)

    # Test final window label.
    self.assertEqual(repr(example).splitlines()[-1].split(), ['Label', '>A'])

    # Test ccs matches label
    self.assertTrue(dc_example.ccs_matches_label)

    # Slicing beyond width returns empty.
    self.assertTrue(dc_example[100:].is_empty)

    # Test stack features
    expected_bases_encoded = np.ones((dc_example.n_subreads, dc_example.width))
    calc_bases_encoded = dc_example.stack_subread_feature('bases_encoded')
    self.assertTrue((calc_bases_encoded == expected_bases_encoded).all())
    self.assertTrue(dc_example.extract_features().shape, (86, 10))

    # Test extract features to 2D array.
    # Extract base rows and sum - because A=1 we should have 9 rows of 1 = 9.
    self.assertEqual(
        np.sum(dc_example.extract_features()[:20,]),
        dc_example.width * dc_example.n_subreads,
    )

    # sn values = 0.5; So summing for one column should be equal to 2.
    self.assertEqual(
        np.sum(dc_example.extract_features()[dc_config.indices('sn')]),
        2 * dc_example.width,
    )

    # Test max_passes with subreads.
    low_max_pass = 5
    dc_example.config.max_passes = low_max_pass
    self.assertEqual(
        dc_example.keep_subreads,
        low_max_pass,
        msg='test keep_subreads is set to config.max_passes.',
    )

  def test_inference_setup(self):
    # Test DcExample functionality under inference conditions.
    dc_config = pre_lib.DcConfig(max_passes=3, max_length=3)
    # First, generate a bunch of reads
    read_set = []
    for i in range(0, 10):
      segment = create_segment(
          name=f'm0/1/{i}', bases='A' * 10, cigar='10M', reference_start=0
      )
      read = pre_lib.expand_clip_indent(segment)
      read_set.append(read)
    aln_reads = pre_lib.space_out_subreads(read_set)
    dc_example = pre_lib.DcExample('test_read_set', aln_reads, dc_config)

    self.assertEqual(dc_example.ccs.name, read_set[-1].name)
    self.assertIsNone(dc_example.label)
    self.assertEmpty(dc_example.label_coords)
    self.assertLen(dc_example.subreads, len(read_set) - 1)

    # Test to_features_dict()
    dc_iter = dc_example.iter_examples()
    example = next(dc_iter)
    example = next(dc_iter)
    self.assertEqual(example.to_features_dict()['name'], dc_example.name)
    self.assertEqual(example.to_features_dict()['subreads'].shape, (17, 3, 1))
    self.assertEqual(example.to_features_dict()['window_pos'], 3)

  def test_tf_example_train(self):
    dc_config = pre_lib.DcConfig(max_passes=20, max_length=10)
    read_set = []
    for i in range(0, 10):
      segment = create_segment(
          name=f'm0/1/{i}',
          bases='ATCG' * 25,
          cigar='100M',
          ip=[1, 2, 3, 4] * 25,
          pw=[5, 6, 7, 8] * 25,
          reference_start=0,
      )
      read = pre_lib.expand_clip_indent(segment)
      read_set.append(read)
    # Append a CCS Read.
    read_set.append(pre_lib.construct_ccs_read(segment))
    label_segment = create_segment(
        name='m0/1/truth', bases='ATCG' * 25, cigar='100M', reference_start=0
    )
    truth_range = {'contig': 'chr1', 'begin': 0, 'end': 100}
    label = pre_lib.expand_clip_indent(label_segment, truth_range)
    read_set += [label]
    dc_example = pre_lib.subreads_to_dc_example(
        read_set, 'm0/1/ccs', dc_config, None
    )

    # Fetch the second iter example.
    iter_examples = dc_example.iter_examples()
    next(iter_examples)
    window_2 = next(iter_examples)

    # Encode as tf example.
    tf_example = window_2.tf_example()

    # Serialize tf example and reverse.
    tf_example_str = tf_example.SerializePartialToString()
    parsed_example = data_providers.parse_example(
        tf_example_str,
        inference=False,
        max_length=dc_config.max_length,
    )
    self.assertSetEqual(
        set(parsed_example.keys()),
        set(data_providers.PROTO_FEATURES_TRAIN.keys()),
    )

    # Compare tf example converted back to DcExample
    features = pre_lib.tf_example_to_features_dict(
        tf_example_str,
        max_length=dc_config.max_length,
    )
    window_2_rev = pre_lib.from_features_dict(features)

    # Compare reversed values.
    self.assertTrue(
        (window_2.reads[0].bases == list(window_2_rev.reads[0].bases)).all(),
        'bases do not match',
    )
    self.assertEqual(
        window_2.reads[1].strand,
        window_2_rev.reads[1].strand,
        'strand does not match',
    )
    self.assertEqual(
        window_2.reads[2].strand,
        window_2_rev.reads[2].strand,
        'strand does not match',
    )
    self.assertTrue(
        (window_2.ccs.ccs_idx == window_2_rev.ccs.ccs_idx).all(),
        'ccs_idx does not match',
    )

  def test_large_label_insertion(self):
    dc_config = pre_lib.DcConfig(max_passes=20, max_length=8)
    # Test case where label contains large insertions.
    read_set = []
    for i in range(0, 3):
      segment = create_segment(
          name=f'm0/1/{i}', bases='A' * 15, cigar='15M', reference_start=0
      )
      read = pre_lib.expand_clip_indent(segment)
      read_set.append(read)
    label_segment = create_segment(
        name='m0/1/truth',
        bases=(5 * 'A') + ('G' * 8) + ('A' * 21),
        cigar='5M8I21M',
        reference_start=0,
    )
    truth_range = {'contig': 'chr1', 'begin': 0, 'end': 34}
    label = pre_lib.expand_clip_indent(label_segment, truth_range)
    read_set += [label]
    aln_reads = pre_lib.space_out_subreads(read_set)
    dc_example = pre_lib.DcExample('test_read_set', aln_reads, dc_config)
    # The first window is skipped because the large
    # label insertion causes it to exceed the padded size (9).
    # So we get a single output.
    for example in dc_example.iter_examples():
      self.assertEqual(
          'test_read_set CCS(8-14) chr1:16-22', repr(example).splitlines()[0]
      )
    self.assertEqual(dc_example.counter['n_examples_label_overflow'], 1)

  def test_remove_gaps_and_pad(self):
    dc_config = pre_lib.DcConfig(max_passes=20, max_length=100)
    read_set = []
    for i in range(0, 3):
      segment = create_segment(
          name=f'm0/1/{i}',
          bases=('A' * 5) + ('G' * 8) + ('A' * 5),
          cigar='18M',
          reference_start=0,
      )
      read = pre_lib.expand_clip_indent(segment)
      read_set.append(read)
    label_segment = create_segment(
        name='m0/1/truth',
        bases=(5 * 'A') + ('A' * 5),
        cigar='5M8D5M',
        reference_start=0,
    )
    truth_range = {'contig': 'chr1', 'begin': 0, 'end': 10}
    label = pre_lib.expand_clip_indent(label_segment, truth_range)
    read_set += [label]
    aln_reads = pre_lib.space_out_subreads(read_set)
    dc_example = pre_lib.DcExample('test_read_set', aln_reads, dc_config)
    self.assertEqual(
        str(dc_example.label.remove_gaps(100)), 'A' * 10 + dc_constants.GAP * 90
    )

  @parameterized.named_parameters(
      dict(
          testcase_name='simple case',
          segment_set=[
              create_segment(
                  name='ZMW/1/0',
                  bases='AAAAATTTTT',
                  cigar='10M',
                  reference_start=0,
              ),
              create_segment(
                  name='ZMW/1/1',
                  bases='AAAAATTTTT',
                  cigar='10M',
                  reference_start=0,
              ),
          ],
          window_widths=[2, 3, 4, 1],
          expected_examples=[
              (
                  'Read(m0/1/9) CCS(0-1)\n-----------------------------\n0     '
                  '               1 >AA   \nCCS                    >AA'
              ),
              (
                  'Read(m0/1/9) CCS(2-4)\n-----------------------------\n0     '
                  '               1 >AAA  \nCCS                    >AAA'
              ),
              (
                  'Read(m0/1/9) CCS(5-8)\n-----------------------------\n0     '
                  '               1 >TTTT \nCCS                    >TTTT'
              ),
              (
                  'Read(m0/1/9) CCS(9-9)\n-----------------------------\n0     '
                  '               1 >T    \nCCS                    >T'
              ),
          ],
      ),
      dict(
          testcase_name='overflow case',
          segment_set=[
              create_segment(
                  name='ZMW/1/0',
                  bases='AAGGGTTTTTTTT',
                  cigar='2M3I8M',
                  reference_start=0,
              ),
              create_segment(
                  name='ZMW/1/1',
                  bases='AAAAATTTTT',
                  cigar='10M',
                  reference_start=0,
              ),
          ],
          window_widths=[2, 3, 5],
          expected_examples=[
              (
                  'Read(m0/1/9) CCS(0-1)\n-----------------------------\n0     '
                  '               1 >AA   \nCCS                    >AA'
              ),
              (
                  'Read(m0/1/9) CCS(2-4)\n------------------------------\n0    '
                  '                1 >GGGTTT\nCCS                    >  '
                  ' AAA\noverflow               >True'
              ),
              (
                  'Read(m0/1/9) CCS(5-9)\n-----------------------------\n0     '
                  '               1 >TTTTT\nCCS                    >TTTTT'
              ),
          ],
      ),
  )
  def test_ccs_smart_windows(
      self, segment_set, window_widths, expected_examples
  ):
    dc_config = pre_lib.DcConfig(max_passes=20, max_length=5)
    read_set = []
    for segment in segment_set:
      read = pre_lib.expand_clip_indent(segment)
      read_set.append(read)
    aln_reads = pre_lib.space_out_subreads(read_set)
    dc_example = pre_lib.DcExample(
        'Read(m0/1/9)', aln_reads, dc_config, window_widths
    )
    examples = [repr(example).strip() for example in dc_example.iter_examples()]
    self.assertCountEqual(examples, expected_examples)


class TestTfExamplesToFeaturesDict(parameterized.TestCase):

  def test_tf_examples_to_features_dict(self):
    tf_examples = test_utils.deepconsensus_testdata(
        'human_1m/tf_examples/@split/@split.tfrecord.gz'
    )
    examples = test_utils.load_dataset(tf_examples, 'train')
    feature_dicts = pre_lib.tf_example_to_features_dict(
        examples[0], inference=False, use_ccs_bq=False
    )
    self.assertListEqual(
        list(feature_dicts['subreads/shape']),
        list(feature_dicts['subreads'].shape),
    )

  def test_tf_examples_bq_to_features_dict(self):
    tf_examples = test_utils.deepconsensus_testdata(
        'human_1m/tf_examples_bq/@split/@split.tfrecord.gz'
    )
    examples = test_utils.load_dataset(tf_examples, 'train')
    feature_dicts = pre_lib.tf_example_to_features_dict(
        examples[0], inference=False, use_ccs_bq=True
    )
    self.assertListEqual(
        list(feature_dicts['subreads/shape']),
        list(feature_dicts['subreads'].shape),
    )


if __name__ == '__main__':
  absltest.main()
