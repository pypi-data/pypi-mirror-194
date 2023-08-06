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
"""Utility functions being used for data processing."""

import collections
from collections import abc
import dataclasses
import functools
import itertools
from typing import Any, Counter, Dict, List, Optional, Tuple, Union

from absl import logging
import numpy as np
import pysam
import tensorflow as tf

from deepconsensus.models import data_providers
from deepconsensus.models import model_configs
from deepconsensus.utils import dc_constants
from deepconsensus.utils import utils

Issue = dc_constants.Issue


class SubreadGrouper(abc.Iterator):
  """Returns all subreads belonging to a single zmw as a list."""

  def __init__(self, subreads_to_ccs, reader_threads):
    save = pysam.set_verbosity(0)  # Avoid confusing index file warning.
    self.bam_reader = pysam.AlignmentFile(
        subreads_to_ccs, check_sq=False, threads=reader_threads
    )
    pysam.set_verbosity(save)
    self.keep_iter = True
    self.subread_group = []
    # Setup subread group.
    first_read = next(self.bam_reader)
    self.zmw = first_read.get_tag('zm')
    # Only add read if it is mapped.
    if not first_read.is_unmapped:
      self.subread_group.append(first_read)

  def __next__(self) -> List[pysam.libcalignedsegment.AlignedSegment]:
    if not self.keep_iter:
      raise StopIteration
    while self.keep_iter:
      try:
        read = next(self.bam_reader)
        if read.is_unmapped:
          continue
      except StopIteration:
        self.keep_iter = False
        break
      read_zmw = read.get_tag('zm')
      if read_zmw == self.zmw:
        self.subread_group.append(read)
      elif read_zmw != self.zmw:
        subreads_set = self.subread_group
        self.subread_group = [read]
        self.zmw = read_zmw
        if subreads_set:
          return subreads_set
    if self.subread_group:
      return self.subread_group
    else:
      raise StopIteration


def right_pad(arr: np.ndarray, length: int, value: Any) -> np.ndarray:
  """Right-pad an array with a given value.

  Args:
    arr: A numpy array (1 x n)
    length: The length of arr after padding.
    value: Pad value.

  Returns:
    A padded array.
  """
  # This function does not check for valid padding lengths.
  pad_amt = length - len(arr)
  return np.pad(arr, (0, pad_amt), 'constant', constant_values=value)[:length]


@dataclasses.dataclass
class Read(abc.Sequence):
  """Represents sequence alignments.

  The Read class is used to represent sequence alignments. This includes
  subreads,
  the circular consensus sequence (ccs), and the label sequence. Subread
  sequences and label sequences should both be aligned to the CCS sequence. This
  class is used to construct the DcExample class which in turn will generate
  DeepConsensus tf.Example model inputs.

  Attributes:
    name: The name of the read.
    bases: The sequence of the subread or CCS.
    cigar: The cigar operations string.
    pw: Pulse width.
    ip: interpulse duration.
    sn: Signal-to-noise ratio.
    strand: Indicates alignment strand (0=Unknown, 1=Forward, 2=Reverse).
    ec: Effective coverage.
    np_num_passes: Number of passes.
    rq: Predicted concordance.
    rg: Read group.
    ccs_idx: Positions in the sequence corresponding to CCS indices.
    base_quality_scores: phred-scaled base quality scores.
    truth_idx: The indices of label positions.
    truth_range: The range of positions found in the label dataset.
    idx_spaced: Indices of bases after they are spaced out.
    spacing_done: Whether spacing has been completed.
  """

  name: str
  bases: np.ndarray
  cigar: np.ndarray
  pw: np.ndarray
  ip: np.ndarray
  sn: np.ndarray
  strand: dc_constants.Strand

  # aux tags; from ccs read only.
  ec: Optional[float] = None
  np_num_passes: Optional[int] = None
  rq: Optional[float] = None
  rg: Optional[str] = None

  # base_quality_scores are only used for the ccs read.
  ccs_idx: np.ndarray = np.empty(0, dtype=int)
  base_quality_scores: np.ndarray = np.empty(0, dtype=np.uint8)

  # truth_idx and truth_range only used with label reads.
  truth_idx: np.ndarray = np.empty(0, int)
  # truth range is a dict containing contig, begin, end.
  # It is not modified when slicing is performed.
  # The truth_range['contig'] and truth_idx are used calculate
  # label_coords from sliced regions.
  # truth_range bounds are [begin, end) in keeping with bed format.
  truth_range: Union[Dict[str, Any], None] = None

  # Alignment Variables.
  _seq_indices: np.ndarray = np.empty(0, dtype=int)
  _is_insertion: np.ndarray = np.empty(0, dtype=bool)
  _seq_len: int = 0
  _idx_seq: int = 0
  idx_spaced: int = 0
  spacing_done: bool = False

  def setup_spacing(self):
    """Set up an array for storing spaced indices."""
    self._seq_indices = np.zeros(len(self.bases), dtype=int)
    self._is_insertion = self.cigar == dc_constants.PYSAM_CINS
    self._seq_len = len(self.bases)

  def move(self):
    """For each position, track its spaced index.

    Example:
      Sequence -> _seq_indices   -> put_spacing().
      'AAAA'   -> [0, 1, 3, 4]   -> 'AA AA'
      'MMIM'
    """
    self._seq_indices[self._idx_seq] = self.idx_spaced
    self._idx_seq += 1
    self.idx_spaced += 1

  def add_gap(self):
    self.idx_spaced += 1

  def is_out_of_bounds(self) -> bool:
    return self._idx_seq >= self._seq_len

  def next_is_insertion(self) -> bool:
    """Indicates if next position is an insertion.

    When run on labels, spacing is added to maintain alignment between
    subreads and ccs sequences.

    Returns:
      A boolean indicating whether the next position is an insertion.
    """
    if self.truth_range:
      while not self.is_out_of_bounds() and self._is_insertion[self._idx_seq]:
        # For label insertions, insert bases.
        self._seq_indices[self._idx_seq] = self.idx_spaced
        self._idx_seq += 1
        self.idx_spaced += 1
      return False
    return self._is_insertion[self._idx_seq]

  def put_spacing(self, seq_len: int):
    """Generate spaced sequences and replace the originals."""
    spaced_seq = np.repeat(dc_constants.GAP, seq_len)
    spaced_pw = np.zeros(seq_len, dtype=np.uint8)
    spaced_ip = np.zeros(seq_len, dtype=np.uint8)
    spaced_ccs_idx = np.repeat(-1, seq_len)
    spaced_seq[self._seq_indices] = self.bases
    spaced_pw[self._seq_indices] = self.pw
    spaced_ip[self._seq_indices] = self.ip
    spaced_ccs_idx[self._seq_indices] = self.ccs_idx
    if self.truth_range:
      spaced_cigar = np.repeat(dc_constants.PYSAM_CHARD_CLIP, seq_len)
      spaced_cigar[self._seq_indices] = self.cigar
      self.cigar = spaced_cigar
      truth_pos = np.repeat(-1, seq_len)
      truth_idx = np.arange(self.truth_range['begin'], self.truth_range['end'])
      truth_aln_base = np.isin(
          self.cigar, dc_constants.PYSAM_READ_ADVANCING_OPS
      )
      assert len(truth_pos[truth_aln_base]) == len(truth_idx)
      truth_pos[truth_aln_base] = truth_idx
      self.truth_idx = truth_pos

    self.bases = spaced_seq
    self.pw = spaced_pw
    self.ip = spaced_ip
    self.ccs_idx = spaced_ccs_idx

    # Handle base quality scores. Only present with ccs reads.
    if self.base_quality_scores.any():
      spaced_base_quality_scores = np.repeat(-1, seq_len)
      spaced_base_quality_scores[self._seq_indices] = self.base_quality_scores
      self.base_quality_scores = spaced_base_quality_scores

  @property
  def bases_encoded(self) -> np.ndarray:
    """Outputs bases as discrete integers, but cast as floats."""
    bases_encoded = np.ndarray(
        self.bases.shape, dtype=dc_constants.NP_DATA_TYPE
    )
    for k, base in enumerate(dc_constants.SEQ_VOCAB):
      bases_encoded[self.bases == base] = k
    return bases_encoded

  @property
  def avg_base_quality_score(self) -> float:
    """Outputs the average CCS base quality score."""
    return utils.avg_phred(self.base_quality_scores)

  @property
  def zmw(self) -> int:
    """Returns the zmw for the given read."""
    return int(self.name.split('/')[1])

  @property
  def label_coords(self) -> str:
    """Reports reference coordinates as chr:begin-end."""
    if self.is_label:
      begin = self.label_bounds.start
      end = self.label_bounds.stop
      return f'{self.truth_range["contig"]}:{begin}-{end}'
    return ''

  @property
  def is_label(self) -> bool:
    """Returns bool indicating if this read is a label."""
    return self.truth_range is not None

  @property
  def ccs_bounds(self) -> slice:
    """Return ccs min and max for a given slice."""
    ccs_idx = np.ma.masked_array(self.ccs_idx, self.ccs_idx == -1)
    if not ccs_idx.count():
      # If no ccs coordinates are covered in this region, return an empty slice.
      return slice(0, 0)
    ccs_start = np.min(ccs_idx)
    ccs_end = np.max(ccs_idx)
    return slice(ccs_start, ccs_end)

  @property
  def label_bounds(self) -> slice:
    """Return label reference min and max positions for given slice."""
    truth_idx = np.ma.masked_array(self.truth_idx, self.truth_idx == -1)
    if not truth_idx.count():
      # If no truth coords are covered in this region, return an empty slice.
      return slice(0, 0)
    truth_start = np.min(truth_idx)
    truth_end = np.max(truth_idx)
    return slice(truth_start, truth_end)

  def ccs_slice(self, start: int, end: int) -> 'Read':
    """Perform slicing based on ccs coordinates. Coordinates are inclusive."""
    # Note that these bounds are inclusive by design.
    locs = np.where(np.logical_and(self.ccs_idx >= start, self.ccs_idx <= end))[
        0
    ]
    if locs.any():
      ccs_slice = slice(np.min(locs), np.max(locs) + 1)
    else:
      ccs_slice = slice(0, 0)
    return Read(
        name=self.name,
        bases=self.bases[ccs_slice],
        cigar=self.cigar[ccs_slice],
        pw=self.pw[ccs_slice],
        ip=self.ip[ccs_slice],
        sn=self.sn,
        strand=self.strand,
        base_quality_scores=self.base_quality_scores[ccs_slice],
        ec=self.ec,
        np_num_passes=self.np_num_passes,
        rq=self.rq,
        rg=self.rg,
        ccs_idx=self.ccs_idx[ccs_slice],
        truth_idx=self.truth_idx[ccs_slice],
        truth_range=self.truth_range,
    )

  def pad(self, pad_width: int) -> 'Read':
    """Skip padding when not necessary."""
    if len(self) >= pad_width:
      return self
    return Read(
        name=self.name,
        bases=right_pad(self.bases, pad_width, dc_constants.GAP),
        cigar=right_pad(self.cigar, pad_width, dc_constants.PYSAM_CHARD_CLIP),
        pw=right_pad(self.pw, pad_width, 0),
        ip=right_pad(self.ip, pad_width, 0),
        sn=self.sn,
        strand=self.strand,
        base_quality_scores=right_pad(self.base_quality_scores, pad_width, -1),
        ec=self.ec,
        np_num_passes=self.np_num_passes,
        rq=self.rq,
        rg=self.rg,
        ccs_idx=right_pad(self.ccs_idx, pad_width, -1),
        truth_idx=right_pad(self.truth_idx, pad_width, -1),
        truth_range=self.truth_range,
    )

  def remove_gaps(self, pad_width: int) -> Union['Read', None]:
    """Removes gaps from sequence and returns padded."""
    # Useful for reducing label width.
    keep = self.bases != dc_constants.GAP
    if self.base_quality_scores.any():
      base_quality_scores = self.base_quality_scores[keep]
    else:
      base_quality_scores = np.empty(0, dtype=np.uint8)
    if sum(keep) > pad_width:
      return None
    return Read(
        name=self.name,
        bases=self.bases[keep],
        cigar=self.cigar[keep],
        pw=self.pw[keep],
        ip=self.ip[keep],
        sn=self.sn,
        strand=self.strand,
        base_quality_scores=base_quality_scores,
        ec=self.ec,
        np_num_passes=self.np_num_passes,
        rq=self.rq,
        rg=self.rg,
        ccs_idx=self.ccs_idx[keep],
        truth_idx=self.truth_idx[keep],
        truth_range=self.truth_range,
    ).pad(pad_width)

  def __str__(self):
    return ''.join(self.bases)

  def __len__(self):
    return len(self.bases)

  def __getitem__(self, r_slice: Union[slice, int]) -> 'Read':
    """Implements slicing across all attributes."""
    return Read(
        name=self.name,
        bases=self.bases[r_slice],
        cigar=self.cigar[r_slice],
        pw=self.pw[r_slice],
        ip=self.ip[r_slice],
        sn=self.sn,
        strand=self.strand,
        base_quality_scores=self.base_quality_scores[r_slice],
        ec=self.ec,
        np_num_passes=self.np_num_passes,
        rq=self.rq,
        rg=self.rg,
        ccs_idx=self.ccs_idx[r_slice],
        truth_idx=self.truth_idx[r_slice],
    )

  def __repr__(self):
    if np.any(self.ccs_idx >= 0):
      start = np.min(self.ccs_idx[self.ccs_idx >= 0])
      end = np.max(self.ccs_idx, initial=0)
    else:
      start = 0
      end = 0
    return (
        f'Read({self.name}) : CCS({start}-{end}) L={len(self.bases)} '
        + self.label_coords
    ).strip()


def dc_config_from_shape(
    subreads_shape: Tuple[int, int, int], use_ccs_bq: bool = False
) -> 'DcConfig':
  """Creates a DcConfig object based on subread shape and base quality usage.

  Args:
    subreads_shape: The shape of a subreads input.
    use_ccs_bq: Boolean indicating whether to use base quality scores.

  Returns:
    A DcConfig object.
  """
  height, width, _ = subreads_shape
  if use_ccs_bq:
    fixed_height = 6
  else:
    fixed_height = 5

  max_passes, remainder = divmod(
      height - fixed_height, len(DcConfig.n_subread_features)
  )
  if remainder != 0:
    raise ValueError(f'Invalid subreads shape {subreads_shape!r}.')
  return DcConfig(max_passes, width, use_ccs_bq)


class DcConfig:
  """Option for controlling DcExample configuration and calculating indices.

  Attributes:
    max_passes: Number of passes to incorporate into examples.
    max_length: Width of example.
    feature_rows: A dictionary indicating features and corresponding height.
    use_ccs_bq: Boolean indicating whether to incorporate base quality scores
      into model input.
    feature_indices: Calculated indices for each feature.
  """

  _HAS_DYNAMIC_ATTRIBUTES = True

  # Features with n_rows = n_subreads.
  n_subread_features = ['bases', 'pw', 'ip', 'strand']

  def __init__(
      self,
      max_passes: int,
      max_length: int,
      use_ccs_bq: bool = False,
  ):
    self.max_passes = max_passes
    self.max_length = max_length
    self.feature_rows = {
        'bases': max_passes,
        'pw': max_passes,
        'ip': max_passes,
        'strand': max_passes,
        'ccs': 1,
        'ccs_bq': 1 if use_ccs_bq else 0,
        'sn': 4,
    }
    # Sets slices indicating rows for each feature type.
    self.feature_indices = dict()
    self.use_ccs_bq = use_ccs_bq
    i_rows = 0
    for k, v in self.feature_rows.items():
      self.feature_indices[k] = slice(i_rows, i_rows + self.feature_rows[k])
      setattr(self, k, i_rows)
      i_rows += v

  def indices(self, feature: str, n_subreads: int = 0) -> slice:
    """Returns rows for a given feature.

    Args:
      feature: The feature to return indices for.
      n_subreads: The number of subreads to return indices for, when getting
        indices for features with variable height (ie, features with max_passes)

    Returns:
      A slice corresponding to the indices for a feature.
    """
    if n_subreads:
      assert feature in DcConfig.n_subread_features
      n_rows = min(n_subreads, self.max_passes)
      return slice(getattr(self, feature), getattr(self, feature) + n_rows)
    else:
      assert feature not in DcConfig.n_subread_features
      return slice(
          getattr(self, feature),
          getattr(self, feature) + self.feature_rows[feature],
      )

  @property
  def tensor_height(self) -> int:
    """Returns total rows for tf.Example input."""
    return sum(self.feature_rows.values())

  def to_dict(self) -> Dict[str, str]:
    """Output configuration properties as dict."""
    return {
        # Encode values as strings to prevent aggregation across shards.
        'max_passes': str(self.max_passes),
        'max_length': str(self.max_length),
        'tensor_height': str(self.tensor_height),
        'tensor_width': str(self.max_length),
    }


@dataclasses.dataclass
class DcExample:
  """Python container used to generate DeepConsensus tf.Example."""

  name: str
  reads: List[Read]
  config: DcConfig
  window_widths: Optional[np.ndarray] = None
  counter: Counter[str] = dataclasses.field(default_factory=collections.Counter)

  # Define cached variables.
  _width: Optional[int] = None
  _ccs_width: Optional[int] = None
  _overflow: bool = False

  @property
  def contig(self) -> Optional[str]:
    if self.label:
      return self.label.truth_range['contig']
    return None

  @property
  def is_training(self) -> bool:
    """If a label is in the last position we are in training mode."""
    return self.reads[-1].is_label

  @property
  def ccs(self) -> Read:
    if self.is_training:
      ccs_idx = -2
    else:
      ccs_idx = -1
    return self.reads[ccs_idx]

  @property
  def label(self) -> Union[Read, None]:
    if self.is_training:
      return self.reads[-1]
    return None

  @property
  def label_coords(self) -> str:
    if self.is_training:
      return self.label.label_coords
    return ''

  @property
  def subreads(self) -> List[Read]:
    if self.is_training:
      return self.reads[:-2]
    else:
      return self.reads[:-1]

  @property
  def n_subreads(self) -> int:
    """Returns the total number of subreads."""
    return len(self.subreads)

  @property
  def keep_subreads(self) -> int:
    """Returns usable number of subreads."""
    return min(self.config.max_passes, self.n_subreads)

  @property
  def width(self) -> int:
    if self._width:
      return self._width
    else:
      self._width = len(self.ccs.bases)
    return self._width

  @property
  def ccs_width(self) -> int:
    # Width - gaps at end.
    if self._ccs_width:
      return self._ccs_width
    else:
      self._ccs_width = len(str(self.ccs).rstrip())
    return self._ccs_width

  @property
  def is_empty(self) -> bool:
    return not (self.ccs.ccs_idx >= 0).any()

  @property
  def ccs_matches_label(self) -> bool:
    """Does the CCS match the label."""
    ccs = utils.left_shift_seq(self.ccs.bases_encoded)
    label = utils.left_shift_seq(self.label.bases_encoded)
    seq_len = max([len(ccs), len(label)])
    ccs = right_pad(ccs, seq_len, 0)
    label = right_pad(label, seq_len, 0)
    return np.equal(ccs, label).all()

  def calculate_windows(self, example_width: int) -> List[int]:
    """Calculate window widths for the given CCS widths with added spacing."""
    window_positions = []
    window_widths = []
    last_pos = 0
    if self.window_widths is not None:
      ccs_calculated_width = 0
      for window_width in self.window_widths:
        # Calculate window width with spaces
        original_width = 0
        window_width_spaced = 0
        while original_width < window_width:
          if self.ccs.bases[last_pos + window_width_spaced] != dc_constants.GAP:
            original_width += 1
          window_width_spaced += 1
        window_positions.append(last_pos)
        window_widths.append(window_width_spaced)
        last_pos += window_width_spaced
        ccs_calculated_width += window_width_spaced
      assert ccs_calculated_width == self.ccs_width
    else:
      num_of_full_windows = int(self.ccs_width / example_width)
      if self.ccs_width % example_width > 0:
        num_of_full_windows += 1
      window_widths = [example_width] * num_of_full_windows
    return window_widths

  def iter_examples(self) -> 'DcExample':
    """Generates partitions from a given window."""
    # Initiate counter
    self.counter = collections.Counter()
    max_length = self.config.max_length
    start_pos = 0
    for window_width in self.calculate_windows(max_length):
      self.counter['example_width_bucket_{}'.format(window_width)] += 1
      window = self[start_pos : start_pos + window_width]
      if start_pos > self.ccs_width:
        break
      start_pos += window_width
      if window.is_empty:
        self.counter['n_examples_no_ccs_idx'] += 1
        continue

      # If the label extends beyond max_length (width),
      # remove gaps and right pad.
      # Gaps are helpful for visualizing alignments, but are
      # used during training.
      if self.is_training and len(window.label.bases) > max_length:
        adjusted_label = window.label.remove_gaps(max_length)
        # Even with this adjustment it is still possible for the label to
        # be longer than the padded length. This is rare. Discard when training.
        if not adjusted_label:
          # Consider alternative solutions to incorporate these data.
          self.counter['n_examples_label_overflow'] += 1
          continue
        self.counter['n_examples_adjusted_label'] += 1
        window.reads[-1] = adjusted_label

      self._overflow = False
      if window_width > max_length:
        self.counter['n_examples_overflow'] += 1
        self._overflow = True
        # Overflown examples are not used for training.
        if self.is_training:
          continue
      else:
        self.counter['n_examples_skip_large_windows_keep'] += 1

      # Pad all reads so they have the same length.
      reads = [x.pad(max_length) for x in window.reads]
      # TODO Think about refactoring DCExample and DCExample
      # generator into different classes.
      yield DcExample(self.name, reads, self.config, _overflow=self._overflow)

  def stack_subread_feature(self, name: str) -> np.ndarray:
    """Extract read feature and stack."""
    max_passes = self.config.max_passes
    return np.stack([getattr(x, name) for x in self.subreads[:max_passes]])

  def extract_features(self) -> np.ndarray:
    """Convert features to a 2D array."""

    def repeat(feature):
      """Repeat a feature for the example width."""
      return np.repeat(np.expand_dims(feature, -1), self.width, -1)

    # Get shape (example_rows, width)
    n_subreads = self.n_subreads
    dims = (self.config.tensor_height, self.width)
    data = np.zeros(shape=dims, dtype=dc_constants.NP_DATA_TYPE)

    # Get feature indices.
    bases_idx = self.config.indices('bases', n_subreads)
    pw_idx = self.config.indices('pw', n_subreads)
    ip_idx = self.config.indices('ip', n_subreads)
    strand_idx = self.config.indices('strand', n_subreads)
    ccs_idx = self.config.indices('ccs')
    ccs_bq_idx = self.config.indices('ccs_bq')
    sn_idx = self.config.indices('sn')

    # Set features.
    data[bases_idx] = self.stack_subread_feature('bases_encoded')
    data[pw_idx] = self.stack_subread_feature('pw')
    data[ip_idx] = self.stack_subread_feature('ip')

    # Format strand feature.
    strand = self.stack_subread_feature('strand')
    strand = strand.astype(dc_constants.NP_DATA_TYPE)
    strand = repeat(strand)
    data[strand_idx] = strand

    # ccs features.
    data[ccs_idx] = self.ccs.bases_encoded
    if self.config.use_ccs_bq:
      data[ccs_bq_idx] = self.ccs.base_quality_scores

    # Format sn rows.
    data[sn_idx] = repeat(self.subreads[0].sn)

    return np.expand_dims(data, -1)

  def to_features_dict(self):
    """Convert DcExample to a dictionary for inference."""
    data = self.extract_features()
    # Add additional dimension.
    features = {
        'subreads': data,
        'subreads/num_passes': self.keep_subreads,
        'name': self.name,
        'window_pos': self.ccs.ccs_bounds.start,
        'ccs_base_quality_scores': self.ccs.base_quality_scores,
        'overflow': self._overflow,
        'ec': self.ccs.ec,
        'np_num_passes': self.ccs.np_num_passes,
        'rq': self.ccs.rq,
        'rg': self.ccs.rg,
    }
    return features

  def tf_example(self) -> tf.train.Example:
    """Convert DcExample to tf.Example."""
    data = self.extract_features()
    # Add additional dimension.
    example = tf.train.Example()
    features = example.features
    features.feature['subreads/encoded'].bytes_list.value.append(data.tobytes())
    features.feature['subreads/shape'].int64_list.value.extend(data.shape)
    features.feature['subreads/num_passes'].int64_list.value.append(
        self.keep_subreads
    )
    features.feature['name'].bytes_list.value.append(self.name.encode())
    features.feature['window_pos'].int64_list.value.append(
        self.ccs.ccs_bounds.start
    )
    features.feature['ccs_base_quality_scores'].int64_list.value.extend(
        self.ccs.base_quality_scores
    )

    if self.is_training:
      label = self.label.bases_encoded
      features.feature['label/encoded'].bytes_list.value.append(label.tobytes())
      features.feature['label/shape'].int64_list.value.extend(label.shape)
    return example

  def __getitem__(self, r_slice: Union[slice, int]) -> 'DcExample':
    """Implements windowed slicing of subreads and ccs_slicing of label."""
    if isinstance(r_slice, int):
      raise NotImplementedError
    reads = self.subreads + [self.ccs]
    reads = [x[r_slice] for x in reads]
    if self.label:
      ccs_slice = self.ccs[r_slice].ccs_bounds
      reads.append(self.label.ccs_slice(ccs_slice.start, ccs_slice.stop))
    return DcExample(self.name, reads, self.config)

  def __repr__(self):
    preview = self[:100]
    start = preview.ccs.ccs_bounds.start
    end = preview.ccs.ccs_bounds.stop
    output = ''
    output += (
        f'{self.name} CCS({start}-{end}) {self.label_coords}'.strip()
        + f'\n{"-"*(preview.width+24)}\n'
    )
    for subread in self.subreads:
      subread_range = subread.name.split('/')[2]
      output += f'{subread_range:<20} {subread.strand} >{str(subread)}\n'
    output += f'{"CCS":<22} >{str(preview.ccs)}\n'

    if self.is_training:
      label = str(self.label)
      output += f'{"Label":<22} >{label}\n'
    if self._overflow:
      output += f'{"overflow":<22} >{self._overflow}\n'
    return output


def decode_bases(bases_encoded: np.ndarray) -> np.ndarray:
  """Reverses DcExample encode_bases."""
  n_subreads, max_length = bases_encoded.shape
  bases = np.stack([np.repeat(dc_constants.GAP, max_length)] * n_subreads)
  for k, base in enumerate(dc_constants.SEQ_VOCAB):
    bases[bases_encoded == k] = base
  return bases


def from_features_dict(features_dict: Dict[str, Any]) -> DcExample:
  """Converts features_dict partially back to a DcExample object for tests."""
  dc_config = dc_config_from_shape(features_dict['subreads/shape'])
  data = np.squeeze(features_dict['subreads'])
  name = features_dict['name']
  n_subreads = features_dict['subreads/num_passes']
  # Note: The ccs start position is correct, but indices
  # may not be accurate beyond the first position.
  ccs_start_pos = features_dict['window_pos']

  # Get feature indices.
  bases_idx = dc_config.indices('bases', n_subreads)
  pw_idx = dc_config.indices('pw', n_subreads)
  ip_idx = dc_config.indices('ip', n_subreads)
  strand_idx = dc_config.indices('strand', n_subreads)
  ccs_idx = dc_config.indices('ccs')
  sn_idx = dc_config.indices('sn')

  # Convert 2D array back to features.
  bases = decode_bases(data[bases_idx])
  pw = data[pw_idx]
  ip = data[ip_idx]
  strand = data[strand_idx]
  ccs = decode_bases(data[ccs_idx])[0]
  sn = data[sn_idx][:, 1]

  ccs_idx = np.repeat(-1, dc_config.max_length)
  ccs_end_pos = ccs_start_pos + dc_config.max_length
  ccs_idx[0 : dc_config.max_length] = np.arange(ccs_start_pos, ccs_end_pos)

  movie, zmw, _ = name.split('/')

  # Generate DcExample
  read_set = []
  for i in range(n_subreads):
    read = Read(
        f'{movie}/{zmw}/{i}',
        bases=bases[i],
        cigar=np.repeat(np.uint8(pysam.CMATCH), dc_config.max_length),
        pw=pw[i],
        ip=ip[i],
        sn=sn,
        strand=dc_constants.Strand(int(strand[i][0])),
        ccs_idx=ccs_idx,
    )
    read_set.append(read)
  ccs_read = Read(
      name=name,
      bases=ccs,
      cigar=np.repeat(np.uint8(pysam.CMATCH), dc_config.max_length),
      pw=np.repeat(np.uint8(0), dc_config.max_length),
      ip=np.repeat(np.uint8(0), dc_config.max_length),
      sn=np.repeat(0, 4),
      strand=dc_constants.Strand.UNKNOWN,
      ccs_idx=ccs_idx,
  )
  read_set.append(ccs_read)
  return DcExample(name=name, reads=read_set, config=dc_config)


def set_feature(feature, shape):
  """Read in feature and set shape."""
  if not tf.executing_eagerly():
    feature = tf.io.decode_raw(feature, dc_constants.TF_DATA_TYPE)
    feature = tf.reshape(feature, shape)
  else:
    feature = np.frombuffer(feature, dtype=dc_constants.NP_DATA_TYPE)
    feature = feature.reshape(shape)
  return feature


def tf_example_to_features_dict(
    tf_example_proto_str: Dict[str, Any],
    inference: bool = False,
    use_ccs_bq: bool = False,
    max_length: int = 100,
) -> Dict[str, Any]:
  """Converts tf.Example to features_dict.

  Args:
    tf_example_proto_str: Input str-encoded tf.Example.
    inference: Bool indicating whether to only load inference-relevant fields.
    use_ccs_bq: Bool indicating whether subreads contain base quality scores.
    max_length: The width of the tf.Example.

  Returns:
    A dictionary containing tf.Example Tensor elements.
  """
  features = data_providers.parse_example(
      tf_example_proto_str,
      inference=inference,
      max_length=max_length,
  )

  for key, val in features.items():
    if tf.executing_eagerly():
      features[key] = val.numpy()

  # Cast types
  if 'name' in features.keys():
    if tf.executing_eagerly():
      features['name'] = str(features['name'][0], 'UTF-8')
    else:
      features['name'] = features['name'][0]
  features['subreads/num_passes'] = int(features['subreads/num_passes'])

  features['subreads'] = set_feature(
      features['subreads/encoded'], features['subreads/shape']
  )
  dc_config = dc_config_from_shape(
      features['subreads/shape'],
      use_ccs_bq,
  )
  # Get a default config and overwrite with specified values
  params = model_configs.get_config()
  with params.unlocked():
    params.use_ccs_bq = use_ccs_bq
    params.max_length = int(dc_config.max_length)
    params.max_passes = int(dc_config.max_passes)
    params.total_rows = data_providers.get_total_rows(
        params.max_passes,
        use_ccs_bq,
    )
  features['subreads'] = data_providers.format_rows(
      features['subreads'], params
  )
  del features['subreads/encoded']
  if not inference:
    features['label'] = set_feature(
        features['label/encoded'], features['label/shape']
    )
    del features['label/encoded']
  return features


def construct_ccs_read(
    ccs_bam_read: pysam.libcalignedsegment.AlignedSegment,
) -> Read:
  """Constructs a Read with quality scores using a ccs bam read."""
  ccs_seq = np.array(ccs_bam_read.seq, 'c')

  def get_tag(read: pysam.AlignedSegment, tag_name: str) -> Any:
    try:
      return read.get_tag(tag_name)
    except KeyError:
      return None

  # get aux variables
  ec = get_tag(ccs_bam_read, 'ec')
  np_num_passes = get_tag(ccs_bam_read, 'np')
  rq = get_tag(ccs_bam_read, 'rq')
  rg = get_tag(ccs_bam_read, 'RG')

  return Read(
      name=ccs_bam_read.qname,
      bases=ccs_seq,
      cigar=np.repeat(np.uint8(pysam.CMATCH), len(ccs_seq)),
      pw=np.repeat(np.uint8(0), len(ccs_seq)),
      ip=np.repeat(np.uint8(0), len(ccs_seq)),
      sn=np.repeat(0, 4),
      ec=ec,
      np_num_passes=np_num_passes,
      rq=rq,
      rg=rg,
      strand=dc_constants.Strand.UNKNOWN,
      base_quality_scores=np.array(ccs_bam_read.query_qualities),
      ccs_idx=np.arange(len(ccs_seq)),
  )


def fetch_label_alignment(
    ccs_seqname: str,
    truth_to_ccs: pysam.AlignmentFile,
    truth_range: Dict[str, Any],
) -> Union[dc_constants.Issue, Read]:
  """Fetches a label aligned to ccs sequence."""
  try:
    truth_alignment = next(truth_to_ccs.fetch(ccs_seqname))
  except (ValueError, StopIteration):
    return Issue.TRUTH_ALIGNMENT_NOT_FOUND
  if truth_alignment.is_supplementary:
    return Issue.SUPP_TRUTH_ALIGNMENT
  truth_alignment = expand_clip_indent(truth_alignment, truth_range)
  return truth_alignment


def read_truth_bedfile(truth_bed: str) -> Dict[str, Dict[str, Any]]:
  """Reads in complete truth bed file and returns dict."""
  bed_coords = {}
  with tf.io.gfile.GFile(truth_bed, 'r') as bedfile:
    for line in bedfile:
      contig, begin, end, ccs_seqname = line.strip().split('\t')[:4]
      bed_record = {'contig': contig, 'begin': int(begin), 'end': int(end)}
      bed_coords[ccs_seqname] = bed_record
  return bed_coords


def read_truth_split(split_fname: str) -> Dict[str, str]:
  """Reads in split bed file and returns dict."""
  contig_split = {}
  split_regions = {}
  if any([x in split_fname.lower() for x in ['chm13', 'hg00', 'human']]):
    train_regions = dc_constants.TRAIN_REGIONS['HUMAN']
    eval_regions = dc_constants.EVAL_REGIONS['HUMAN']
    test_regions = dc_constants.TEST_REGIONS['HUMAN']
  elif 'maize' in split_fname.lower():
    train_regions = dc_constants.TRAIN_REGIONS['MAIZE']
    eval_regions = dc_constants.EVAL_REGIONS['MAIZE']
    test_regions = dc_constants.TEST_REGIONS['MAIZE']
  else:
    raise ValueError(
        f'{split_fname} does not correspond to any genome specified in'
        f' dc_constants.py. Please either either change {split_fname} name or'
        ' add new train/eval/test regions to dc_constants.py'
    )

  for i in train_regions:
    split_regions[i] = 'train'
  for i in eval_regions:
    split_regions[i] = 'eval'
  for i in test_regions:
    split_regions[i] = 'test'
  with tf.io.gfile.GFile(split_fname, 'r') as f:
    for line in f:
      contig, chrom = line.split()
      if chrom in split_regions:
        contig_split[contig] = split_regions[chrom]
  return contig_split


def trim_insertions(
    read: pysam.AlignedSegment,
    ins_trim: int,
    counter: Optional[Counter[str]] = None,
) -> pysam.AlignedSegment:
  """Remove insertions larger than max length.

  This operation effectively
  modifies aligned sequence, cigar, and pw/ip tags.

  Args:
    read: pysam.AlignedSegment subread aligned to the ccs.
    ins_trim: int maximum length of insertions.
    counter: A counter object used to track information about processing data.

  Returns:
    pysam.AlignedSegment. Modified pysam.AlignedSegment subread.
  """
  if ins_trim <= 0:
    return read
  pw_vals = []
  ip_vals = []
  if read.has_tag('pw'):
    pw_vals = read.get_tag('pw')
  if read.has_tag('ip'):
    ip_vals = read.get_tag('ip')

  trimmed_cigar = []
  trimmed_seq = ''
  op_start = 0
  seq_pos = 0
  mask = [True] * len(read.seq)
  for cigar_op, op_len in read.cigartuples:
    if cigar_op == dc_constants.PYSAM_CINS and op_len > ins_trim:
      # Trim to zero, so this cigar operation is removed completely.
      mask[seq_pos : seq_pos + op_len] = [False] * op_len
      seq_pos += op_len
      if counter is not None:
        counter['zmw_trimmed_insertions'] += 1
        counter['zmw_trimmed_insertions_bp'] += op_len
    else:
      trimmed_cigar.append((cigar_op, op_len))
      if cigar_op not in [dc_constants.PYSAM_CDEL]:
        trimmed_seq += read.query_sequence[seq_pos : seq_pos + op_len]
        seq_pos += op_len

    if counter is not None:
      counter['zmw_total_bp'] += op_len
    op_start += op_len

  if pw_vals:
    if read.is_reverse:
      read.set_tag('pw', np.array(pw_vals)[mask[::-1]].tolist())
    else:
      read.set_tag('pw', np.array(pw_vals)[mask].tolist())

  if ip_vals:
    if read.is_reverse:
      read.set_tag('ip', np.array(ip_vals)[mask[::-1]].tolist())
    else:
      read.set_tag('ip', np.array(ip_vals)[mask].tolist())

  read.seq = trimmed_seq
  read.cigartuples = trimmed_cigar
  return read


def expand_clip_indent(
    read: pysam.AlignedSegment,
    truth_range: Union[Dict[str, Any], None] = None,
    ins_trim: int = 0,
    counter: Optional[Counter[str]] = None,
) -> Read:
  """Adds PAD tokens and clips reads.

  For both subreads and label:

  * Expand sequence by placing gaps where deletions are present in alignment.
  * Remove bases that are part of soft-clips.
  * Indent alignment if start position is > 0.
  * Reverse ip/pw values when the strand is reverse.

  Args:
      read: a pysam aligned segment representing a subread, ccs, or label aln.
      truth_range: truth genome alignment coordinates. If supplied, it is
        assumed this is the label alignment.
      ins_trim: insertions in the read are trimmed if true.
      counter: A counter object for tracking processing metrics.

  Returns:
      ExpandedRead
  """
  # Trim insertions
  if ins_trim > 0:
    read = trim_insertions(read, ins_trim, counter)

  # Extract read and reference indices.
  aligned_pairs = read.get_aligned_pairs()
  read_idx = np.array([x[0] if x[0] is not None else -1 for x in aligned_pairs])
  ccs_idx = np.array([x[1] if x[1] is not None else -1 for x in aligned_pairs])
  aln_len = len(read_idx)

  # Create empty expanded read objects.
  new_seq = np.repeat(dc_constants.GAP, aln_len)
  new_pw = np.repeat(np.uint8(0), aln_len)
  new_ip = np.repeat(np.uint8(0), aln_len)

  # Fill read objects based on aligned read idx positions.
  new_seq[read_idx >= 0] = list(read.seq)

  if read.is_reverse:
    strand = dc_constants.Strand.REVERSE
  else:
    strand = dc_constants.Strand.FORWARD

  # pw/ip values are never set for labels.
  # truth_range is used to test if we are working with a label Read.
  if not truth_range:
    # Reverse ip/pw values if the strand is reversed.
    pw_vals = read.get_tag('pw')
    ip_vals = read.get_tag('ip')
    if strand == dc_constants.Strand.REVERSE:
      pw_vals = pw_vals[::-1]
      ip_vals = ip_vals[::-1]
    new_pw[read_idx >= 0] = pw_vals
    new_ip[read_idx >= 0] = ip_vals
    sn = np.array(read.get_tag('sn'))
  else:
    sn = np.empty(0, dtype=np.uint8)

  # Extract additional read properties.
  cigar_seq = itertools.chain.from_iterable([[x] * y for x, y in read.cigar])
  new_cigar = np.fromiter(cigar_seq, dtype=np.uint8)
  # Filter hard_clip from cigar.
  new_cigar = new_cigar[new_cigar != dc_constants.PYSAM_CHARD_CLIP]

  # Trim sequence if it is soft-padded.
  if np.sum(new_cigar == dc_constants.PYSAM_CSOFT_CLIP) > 0:
    new_seq[new_cigar == dc_constants.PYSAM_CSOFT_CLIP] = dc_constants.GAP
    # TODO: binary search ignoring -1 vals here.
    qstart = np.where(read_idx == read.query_alignment_start)[0][0]
    qend = np.where(read_idx == read.query_alignment_end - 1)[0][0] + 1
    # Trim soft-padded segments from truth regions.
    if truth_range:
      op, op_len = read.cigartuples[0]
      if op == dc_constants.PYSAM_CSOFT_CLIP:
        truth_range['begin'] = truth_range['begin'] + op_len
      op, op_len = read.cigartuples[-1]
      if op == dc_constants.PYSAM_CSOFT_CLIP:
        truth_range['end'] = truth_range['end'] - op_len

    new_seq = new_seq[qstart:qend]
    new_pw = new_pw[qstart:qend]
    new_ip = new_ip[qstart:qend]
    new_cigar = new_cigar[qstart:qend]
    ccs_idx = ccs_idx[qstart:qend]

  # Indent sequence
  if read.pos:
    new_seq = np.insert(new_seq, 0, [dc_constants.GAP] * read.pos)
    # Add N cigar op at position 0 to indicate indent.
    new_cigar = np.insert(
        new_cigar, 0, np.repeat(int(pysam.CREF_SKIP), read.pos)
    )
    new_pw = np.insert(new_pw, 0, np.repeat(0, read.pos))
    new_ip = np.insert(new_ip, 0, np.repeat(0, read.pos))
    ccs_idx = np.insert(ccs_idx, 0, np.repeat(-1, read.pos))

  return Read(
      name=read.qname,
      bases=new_seq,
      cigar=new_cigar,
      pw=new_pw,
      ip=new_ip,
      sn=sn,
      strand=strand,
      ccs_idx=ccs_idx,
      truth_range=truth_range,
  )


def space_out_subreads(subreads: List[Read]) -> List[Read]:
  """Spaces out subreads to make room for insertions in any subset of them."""
  for r in subreads:
    r.setup_spacing()
  while not all([r.spacing_done for r in subreads]):
    # This loops over bases in all subreads at once, from left to right.
    any_insertions = False
    for r in subreads:
      if r.spacing_done:
        continue
      if r.next_is_insertion():
        any_insertions = True
        break

    for r in subreads:
      if r.spacing_done:
        continue
      if any_insertions and not r.next_is_insertion():
        # If other reads have insertions, but this one does NOT, add a gap to
        # this read to make space.
        r.add_gap()
      else:
        # In all other cases, just take the next base and move on.
        if not r.is_out_of_bounds():
          r.move()
        if r.is_out_of_bounds():
          # Finally, format reads with spacing.
          r.spacing_done = True

  # Right pad all spaced sequences so they have the same length.
  max_len = max([r.idx_spaced for r in subreads])
  for r in subreads:
    r.put_spacing(max_len)

  return subreads


def create_proc_feeder(
    subreads_to_ccs: str,
    ccs_bam: str,
    dc_config: DcConfig,
    ins_trim: int = 0,
    use_ccs_smart_windows: bool = False,
    truth_bed: Optional[str] = None,
    truth_to_ccs: Optional[str] = None,
    truth_split: Optional[str] = None,
    limit: int = 0,
    bam_reader_threads: int = 1,
):
  """Creates a generator to feed subread process jobs to a multiprocess pool."""
  main_counter = collections.Counter()

  # Initiate files
  subread_grouper = SubreadGrouper(subreads_to_ccs, bam_reader_threads)

  save = pysam.set_verbosity(0)  # Avoid confusing index file warning.
  ccs_bam_h = pysam.AlignmentFile(ccs_bam, check_sq=False)
  pysam.set_verbosity(save)

  is_training = truth_bed and truth_to_ccs and truth_split
  if is_training:
    # Load files required for training.
    truth_to_ccs_bam = pysam.AlignmentFile(truth_to_ccs, require_index=True)
    truth_ref_coords = read_truth_bedfile(truth_bed)
    truth_split_dict = read_truth_split(truth_split)

  def proc_feeder():
    for read_set in subread_grouper:
      main_counter['n_zmw_processed'] += 1
      expand_clip_indent_count = functools.partial(
          expand_clip_indent,
          truth_range=None,
          ins_trim=ins_trim,
          counter=main_counter,
      )
      subreads = list(map(expand_clip_indent_count, read_set))
      ccs_seqname = read_set[0].reference_name
      # Fetch ccs sequence and append to subread set.
      while True:
        ccs_bam_read = next(ccs_bam_h)
        if ccs_bam_read.qname == ccs_seqname:
          break
      # If ccs read is not present in subread_to_ccs bam, throw error.
      if ccs_bam_read.qname != ccs_seqname:
        raise ValueError(f'ccs bam does not contain {ccs_seqname}')

      ccs_read = construct_ccs_read(ccs_bam_read)
      window_widths = None
      if use_ccs_smart_windows:
        window_widths = np.array(ccs_bam_read.get_tag('wl'))
      subreads.append(ccs_read)

      if is_training:
        # Fetch truth to ccs alignment.
        truth_range = truth_ref_coords.get(ccs_seqname, None)
        if not truth_range:
          logging.info('No truth_range defined for %s.', ccs_seqname)
          main_counter['n_zmw_missing_truth_range'] += 1
          continue
        label = fetch_label_alignment(
            ccs_seqname, truth_to_ccs_bam, truth_range
        )
        if label == Issue.TRUTH_ALIGNMENT_NOT_FOUND:
          logging.info('Unable to fetch label alignment for %s.', ccs_seqname)
          main_counter['n_zmw_no_label_alignment'] += 1
          continue
        elif label == Issue.SUPP_TRUTH_ALIGNMENT:
          main_counter['n_zmw_truth_label_supp_alignment'] += 1
          continue
        subreads.append(label)
        # pytype: disable=attribute-error
        split = truth_split_dict.get(truth_range['contig'], None)
        # pytype: enable=attribute-error
        if not split:
          logging.info('No split defined for %s.', ccs_seqname)
          main_counter['n_zmw_missing_contig_split'] += 1
          continue
      else:
        split = 'inference'
      main_counter[f'n_zmw_{split}'] += 1
      main_counter['n_zmw_pass'] += 1
      yield (subreads, ccs_seqname, dc_config, split, window_widths)
      if limit and main_counter['n_zmw_pass'] >= limit:
        break

  return proc_feeder, main_counter


def subreads_to_dc_example(
    subreads: List[Read],
    ccs_seqname: str,
    dc_config: DcConfig,
    window_widths: np.ndarray,
) -> DcExample:
  """Process subreads and return a DcExample object."""
  aln_reads = space_out_subreads(subreads)
  dc_example = DcExample(
      name=ccs_seqname,
      reads=aln_reads,
      config=dc_config,
      window_widths=window_widths,
  )
  return dc_example
