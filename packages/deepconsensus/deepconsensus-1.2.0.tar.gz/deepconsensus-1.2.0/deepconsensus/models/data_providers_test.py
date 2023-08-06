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
"""Tests for deepconsensus.models.data_providers."""

import json
from typing import Any, Dict, Tuple

from absl.testing import absltest
from absl.testing import parameterized
import numpy as np
import tensorflow as tf

from deepconsensus.models import data_providers
from deepconsensus.models import model_configs
from deepconsensus.models import model_utils
from deepconsensus.utils import dc_constants
from deepconsensus.utils import test_utils


def get_test_dataset(inference: bool) -> Tuple[str, Dict[str, Any]]:
  """Loads inference or training dataset and json summary."""
  if inference:
    dataset_path = 'human_1m/tf_examples/inference/*.tfrecord.gz'
    summary_json = 'human_1m/tf_examples/summary/summary.inference.json'
    size_key = 'n_examples_inference'
  else:
    dataset_path = 'human_1m/tf_examples/train/*.tfrecord.gz'
    summary_json = 'human_1m/tf_examples/summary/summary.training.json'
    size_key = 'n_examples_train'
  file_pattern = test_utils.deepconsensus_testdata(dataset_path)
  summary_json_path = test_utils.deepconsensus_testdata(summary_json)
  summary = json.load(tf.io.gfile.GFile(summary_json_path))
  return file_pattern, summary[size_key]


class DataProvidersTest(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='batch size evenly divides # examples train',
          num_epochs=1,
          batch_size=1,
          inference=False,
      ),
      dict(
          testcase_name='multiple epochs train',
          num_epochs=5,
          batch_size=1,
          inference=False,
      ),
      dict(
          testcase_name='batch size does not evenly divide # examples train',
          num_epochs=5,
          batch_size=10,
          inference=False,
      ),
      dict(
          testcase_name='batch size evenly divides # examples inference',
          num_epochs=1,
          batch_size=1,
          inference=True,
      ),
      dict(
          testcase_name='multiple epochs inference',
          num_epochs=5,
          batch_size=1,
          inference=True,
      ),
      dict(
          testcase_name=(
              'batch size does not evenly divide # examples inference'
          ),
          num_epochs=5,
          batch_size=10,
          inference=True,
      ),
  )
  def test_get_dataset(self, num_epochs, batch_size, inference):
    """Checks that batches are of expected size and all examples yielded."""

    # Dataset sizes computed using gqui. Currently, eval set is empty because
    # the testdata only contains one molecule, which is added to training set
    # based on end position.
    file_pattern, dataset_size = get_test_dataset(inference)
    params = model_configs.get_config('transformer+test')
    model_utils.modify_params(params)
    dataset = data_providers.get_dataset(
        file_pattern=file_pattern,
        num_epochs=num_epochs,
        batch_size=batch_size,
        params=params,
        drop_remainder=False,
        inference=inference,
        example_label_tuple=True,
    )
    total = 0
    for rows, label in dataset.as_numpy_iterator():
      # Last batch may contain fewer examples.
      if not inference:
        self.assertLen(rows, len(label))
      self.assertLessEqual(len(rows), batch_size)
      total += len(rows)
    self.assertEqual(total, num_epochs * dataset_size)

  @parameterized.named_parameters(
      dict(
          testcase_name='batch size evenly divides # examples train',
          num_epochs=1,
          batch_size=1,
          inference=False,
      ),
      dict(
          testcase_name='multiple epochs train',
          num_epochs=5,
          batch_size=1,
          inference=False,
      ),
      dict(
          testcase_name='batch size does not evenly divide # examples train',
          num_epochs=5,
          batch_size=10,
          inference=False,
      ),
      dict(
          testcase_name='batch size evenly divides # examples inference',
          num_epochs=1,
          batch_size=1,
          inference=True,
      ),
      dict(
          testcase_name='multiple epochs inference',
          num_epochs=5,
          batch_size=1,
          inference=True,
      ),
      dict(
          testcase_name=(
              'batch size does not evenly divide # examples inference'
          ),
          num_epochs=5,
          batch_size=10,
          inference=True,
      ),
  )
  def test_get_dataset_with_metadata(self, num_epochs, batch_size, inference):
    """Checks that batches are of expected size and all examples yielded."""
    # Dataset sizes computed using gqui. Currently, eval set is empty because
    # the testdata only contains one molecule, which is added to training set
    # based on end position.
    file_pattern, dataset_size = get_test_dataset(inference)
    params = model_configs.get_config('transformer+test')
    model_utils.modify_params(params)
    dataset = data_providers.get_dataset(
        file_pattern=file_pattern,
        num_epochs=num_epochs,
        batch_size=batch_size,
        params=params,
        drop_remainder=False,
        inference=inference,
    )
    total = 0
    for tf_example in dataset.as_numpy_iterator():
      rows = tf_example['rows']
      label = tf_example['label']
      num_passes = tf_example['num_passes']
      window_pos = tf_example['window_pos']
      name = tf_example['name']
      # Last batch may contain fewer examples.
      actual_batch_size = len(rows)
      if not inference:
        self.assertLen(label, actual_batch_size)
      self.assertLen(window_pos, actual_batch_size)
      self.assertLen(name, actual_batch_size)
      self.assertLessEqual(actual_batch_size, batch_size)
      # Sanity check the values in the num_passes array.
      self.assertTrue(tf.reduce_all(num_passes <= 20))
      self.assertTrue(tf.reduce_all(num_passes > 0))
      total += actual_batch_size
    self.assertEqual(total, num_epochs * dataset_size)

  @parameterized.named_parameters(
      dict(
          testcase_name='batch size evenly divides # examples train',
          num_epochs=1,
          batch_size=1,
          inference=False,
      ),
      dict(
          testcase_name='batch size evenly divides # examples inference',
          num_epochs=1,
          batch_size=1,
          inference=True,
      ),
  )
  def test_get_dataset_with_pw_ip(self, num_epochs, batch_size, inference):
    """Checks that batches are of expected size and all examples yielded."""
    file_pattern, _ = get_test_dataset(inference)
    params = model_configs.get_config('transformer_learn_values+test')
    model_utils.modify_params(params)
    dataset = data_providers.get_dataset(
        file_pattern=file_pattern,
        num_epochs=num_epochs,
        batch_size=batch_size,
        params=params,
        inference=inference,
    )
    check_not_empty = False
    for data in dataset.as_numpy_iterator():
      rows = data['rows']
      check_not_empty = True
      (
          base_indices,
          pw_indices,
          ip_indices,
          strand_indices,
          ccs_indices,
          _,
          sn_indices,
      ) = data_providers.get_indices(params.max_passes, params.use_ccs_bq)
      base_rows = rows[:, slice(*base_indices), :, :]
      pw_rows = rows[:, slice(*pw_indices), :, :]
      ip_rows = rows[:, slice(*ip_indices), :, :]
      strand_rows = rows[:, slice(*strand_indices), :, :]
      ccs_rows = rows[:, slice(*ccs_indices), :, :]
      sn_rows = rows[:, slice(*sn_indices), :, :]
      self.assertNotEmpty(base_rows)
      self.assertNotEmpty(pw_rows)
      self.assertNotEmpty(ip_rows)
      self.assertNotEmpty(strand_rows)
      self.assertNotEmpty(ccs_rows)
      self.assertNotEmpty(sn_rows)
      self.assertTrue(np.all(base_rows < dc_constants.SEQ_VOCAB_SIZE))
      self.assertTrue(np.all(ip_rows <= params.IP_MAX))
      self.assertTrue(np.all(pw_rows <= params.PW_MAX))
    self.assertTrue(check_not_empty)  # Used to fail on empty dataset.

  @parameterized.named_parameters(
      dict(
          testcase_name='limit number of examples train',
          limit=42,
          inference=False,
      ),
      dict(
          testcase_name='limit set to size greater than dataset train',
          limit=int(1e6),
          inference=False,
      ),
      dict(
          testcase_name='limit number of examples inference',
          limit=42,
          inference=True,
      ),
      dict(
          testcase_name='limit set to size greater than dataset inference',
          limit=int(1e6),
          inference=True,
      ),
  )
  def test_dataset_with_limit_option(self, limit, inference):
    """Checks that batches are of expected size and all examples yielded."""
    file_pattern, _ = get_test_dataset(inference)
    params = model_configs.get_config('transformer_learn_values+test')
    model_utils.modify_params(params)
    # Fetch the complete dataset.
    full_dataset = data_providers.get_dataset(
        file_pattern=file_pattern,
        num_epochs=1,
        batch_size=1,
        params=params,
        inference=inference,
    )
    full_dataset_size = sum(1 for record in full_dataset)

    # Fetch dataset with the limit flag.
    dataset = data_providers.get_dataset(
        file_pattern=file_pattern,
        num_epochs=1,
        batch_size=1,
        params=params,
        limit=limit,
        inference=inference,
    )
    limit_dataset_size = sum(1 for record in dataset)
    self.assertEqual(min(limit, full_dataset_size), limit_dataset_size)

  def test_remove_internal_gaps_and_shift(self):
    label, expected = (
        '   GGGCGAG   ACATA   ACATA ATA ATA      ',
        'GGGCGAGACATAACATAATAATA                 ',
    )
    label = [float(dc_constants.SEQ_VOCAB.index(x)) for x in label]
    label = tf.expand_dims(tf.constant(label), axis=0)
    shifted = data_providers.remove_internal_gaps_and_shift(label)
    result = ''.join([dc_constants.SEQ_VOCAB[int(x)] for x in shifted])
    self.assertEqual(result, expected)


class GetTotalRowsTest(parameterized.TestCase):

  @parameterized.parameters(
      [20, False, 85],
      [20, True, 86],
      [25, False, 105],
      [25, True, 106],
  )
  def test_get_total_rows(self, max_passes, use_ccs_bq, expected_total_rows):
    total_rows = data_providers.get_total_rows(max_passes, use_ccs_bq)
    self.assertEqual(total_rows, expected_total_rows)


class GetIndicesTest(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='use_ccs_bq',
          use_ccs_bq=True,
          expected_ccs_bq_rows=(81, 82),
          expected_sn_rows=(82, 86),
      ),
      dict(
          testcase_name='no_use_ccs_bq',
          use_ccs_bq=False,
          expected_ccs_bq_rows=(0, 0),
          expected_sn_rows=(81, 85),
      ),
  )
  def test_get_indices(
      self, use_ccs_bq, expected_ccs_bq_rows, expected_sn_rows
  ):
    (
        _,
        _,
        _,
        _,
        _,
        ccs_bq_rows,
        sn_rows,
    ) = data_providers.get_indices(20, use_ccs_bq)
    self.assertEqual(ccs_bq_rows, expected_ccs_bq_rows)
    self.assertEqual(sn_rows, expected_sn_rows)


if __name__ == '__main__':
  absltest.main()
