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
"""Tests for preprocess."""

import json
import os

from absl import flags
from absl.testing import absltest
from absl.testing import flagsaver
from absl.testing import parameterized

from deepconsensus.preprocess import pre_lib
from deepconsensus.preprocess import preprocess
from deepconsensus.utils import test_utils
from deepconsensus.utils.test_utils import deepconsensus_testdata
from absl import app


testdata = deepconsensus_testdata

FLAGS = flags.FLAGS


def load_summary(tmp_dir, path):
  summary_path = os.path.join(tmp_dir, path)
  return json.load(open(summary_path, 'r'))


def get_unique_zmws(examples):
  zmws = []
  for example in examples:
    features = pre_lib.tf_example_to_features_dict(example)
    zmws.append(int(features['name'].split('/')[1]))
  return len(set(zmws))


class PreprocessE2E(parameterized.TestCase):

  @parameterized.parameters([0, 2])
  def test_e2e_inference(self, n_cpus):
    """Tests preprocessing inference in both single and multiprocess mode."""
    n_zmws = 3
    FLAGS.subreads_to_ccs = testdata('human_1m/subreads_to_ccs.bam')
    FLAGS.ccs_bam = testdata('human_1m/ccs.bam')
    FLAGS.cpus = n_cpus
    FLAGS.limit = n_zmws
    tmp_dir = self.create_tempdir()
    output = os.path.join(tmp_dir, 'tf-@split.tfrecord.gz')
    FLAGS.output = output
    preprocess.main([])
    examples = test_utils.load_dataset(output, 'inference')
    features = pre_lib.tf_example_to_features_dict(examples[0], inference=True)

    # Check that window_pos incr. monotonically for each ZMW.
    last_pos = -1
    last_zmw = -1
    for example in examples:
      features = pre_lib.tf_example_to_features_dict(example, inference=True)
      zmw = int(features['name'].split('/')[1])
      if zmw != last_zmw:
        last_zmw = zmw
        last_pos = -1
      window_pos = int(features['window_pos'])
      self.assertGreater(window_pos, last_pos)
      last_zmw = zmw
      last_pos = window_pos

    summary = load_summary(tmp_dir, 'tf-summary.inference.json')

    self.assertEqual(summary['n_zmw_pass'], n_zmws)
    self.assertLen(examples, summary['n_examples'])

  @parameterized.parameters([0, 2])
  def test_e2e_train(self, n_cpus):
    """Tests preprocessing training in both single and multiprocess mode."""
    n_zmws = 10
    FLAGS.subreads_to_ccs = testdata('human_1m/subreads_to_ccs.bam')
    FLAGS.ccs_bam = testdata('human_1m/ccs.bam')
    FLAGS.truth_to_ccs = testdata('human_1m/truth_to_ccs.bam')
    FLAGS.truth_bed = testdata('human_1m/truth.bed')
    FLAGS.truth_split = testdata('human_1m/truth_split.tsv')
    FLAGS.cpus = n_cpus
    FLAGS.limit = n_zmws
    tmp_dir = self.create_tempdir()
    output = os.path.join(tmp_dir, 'tf-@split.tfrecord.gz')
    FLAGS.output = output
    preprocess.main([])
    train_examples = test_utils.load_dataset(output, 'train')
    eval_examples = test_utils.load_dataset(output, 'eval')
    test_examples = test_utils.load_dataset(output, 'test')
    all_examples = train_examples + eval_examples + test_examples

    # Check that window_pos incr. monotonically for each ZMW.
    last_pos = -1
    last_zmw = -1
    for example in all_examples:
      features = pre_lib.tf_example_to_features_dict(example, inference=False)
      zmw = int(features['name'].split('/')[1])
      if zmw != last_zmw:
        last_zmw = zmw
        last_pos = -1
      window_pos = int(features['window_pos'])
      self.assertGreater(window_pos, last_pos)
      last_zmw = zmw
      last_pos = window_pos

    summary = load_summary(tmp_dir, 'tf-summary.training.json')

    # Total count
    self.assertLen(all_examples, summary['n_examples'])

    # Test ZMW counts match
    n_zmw_train = get_unique_zmws(train_examples)
    n_zmw_eval = get_unique_zmws(eval_examples)
    n_zmw_test = get_unique_zmws(test_examples)
    self.assertLessEqual(summary['n_zmw_pass'], n_zmws)
    self.assertEqual(
        n_zmw_train + n_zmw_eval + n_zmw_test, summary['n_zmw_pass']
    )
    self.assertEqual(n_zmw_train, summary['n_zmw_train'])
    self.assertEqual(n_zmw_eval, summary['n_zmw_eval'])
    self.assertEqual(n_zmw_test, summary['n_zmw_test'])

    # Test n example counts match
    self.assertLen(train_examples, summary['n_examples_train'])
    self.assertLen(eval_examples, summary['n_examples_eval'])
    self.assertLen(test_examples, summary['n_examples_test'])

    features = pre_lib.tf_example_to_features_dict(train_examples[0])
    self.assertIn('label', features)
    self.assertIn('label/shape', features)
    self.assertSameElements(
        features['subreads'].shape, features['subreads/shape']
    )

  def test_invalid_tf_examples(self):
    """Tests for proper error thrown when loading improprer tf example."""
    output = os.path.join(self.create_tempdir(), 'tf-@split.tfrecord.gz')
    with flagsaver.flagsaver(
        subreads_to_ccs=testdata('human_1m/subreads_to_ccs.bam'),
        ccs_bam=testdata('human_1m/ccs.bam'),
        use_ccs_bq=True,
        cpus=0,
        limit=1,
        output=output,
    ):
      preprocess.main([])
      examples = test_utils.load_dataset(output, 'train')
      with self.assertRaisesRegex(ValueError, 'Invalid subreads shape'):
        _ = pre_lib.tf_example_to_features_dict(
            examples[0], inference=True, use_ccs_bq=False
        )

  def test_bq_tf_examples(self):
    """Tests preprocessing inference with base quality score features."""
    output = os.path.join(self.create_tempdir(), 'tf-@split.tfrecord.gz')
    with flagsaver.flagsaver(
        subreads_to_ccs=testdata('human_1m/subreads_to_ccs.bam'),
        ccs_bam=testdata('human_1m/ccs.bam'),
        use_ccs_bq=True,
        cpus=0,
        limit=1,
        output=output,
    ):
      preprocess.main([])
      examples = test_utils.load_dataset(output, 'inference')

      features = pre_lib.tf_example_to_features_dict(
          examples[0],
          inference=True,
          use_ccs_bq=True,
      )
      self.assertEqual(list(features['subreads/shape']), [86, 100, 1])
      self.assertEqual(list(features['subreads'].shape), [86, 100, 1])


if __name__ == '__main__':
  absltest.main()
