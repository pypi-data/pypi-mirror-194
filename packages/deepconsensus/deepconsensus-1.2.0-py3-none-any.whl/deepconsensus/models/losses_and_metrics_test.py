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
"""Tests for losses_and_metrics."""

from typing import Sequence, Tuple, List
from absl.testing import absltest
from absl.testing import parameterized
import numpy as np
import tensorflow as tf

from deepconsensus.models import losses_and_metrics
from deepconsensus.utils import dc_constants
from deepconsensus.utils import test_utils


class PerExampleAccuracyTest(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='all padding',
          y_true=np.array(
              [
                  [dc_constants.GAP_INT, dc_constants.GAP_INT],
              ]
          ),
          # Using one hot inputs to create a 'distribution'. The metric will
          # compute the prediction by taking the argmax of the distribution.
          y_pred_scores=np.array(
              [
                  [test_utils.get_one_hot(dc_constants.GAP_INT)] * 2,
              ]
          ),
          # All windows are correct.
          exp_accuracy=1.0,
      ),
      dict(
          testcase_name='Left shift testing',
          y_true=np.stack([
              test_utils.seq_to_array('A T C G'),
              test_utils.seq_to_array('T T T T'),
              test_utils.seq_to_array('A A A A'),
          ]),
          # Using one hot inputs to create a 'distribution'. The metric will
          # compute the prediction by taking the argmax of the distribution.
          y_pred_scores=np.stack([
              test_utils.seq_to_one_hot('   ATCG'),
              test_utils.seq_to_one_hot('   GGGG'),
              test_utils.seq_to_one_hot('   AAAA'),
          ]),
          # Of the 3 examples, 1 and 3 are fully correct.
          exp_accuracy=0.6666667,
      ),
  )
  def test_accuracy(self, y_true, y_pred_scores, exp_accuracy):
    """Checks that accuracy is correct."""
    accuracy_obj = losses_and_metrics.PerExampleAccuracy()
    accuracy_obj.update_state(y_true, y_pred_scores)
    self.assertAlmostEqual(accuracy_obj.result().numpy(), exp_accuracy)

  def test_accuracy_multiple_updates(self):
    """Checks that accuracy is correct with multiple updates."""

    accuracy_obj = losses_and_metrics.PerExampleAccuracy()

    y_true = np.array([
        test_utils.seq_to_array('A T C G'),
        test_utils.seq_to_array('A T C G'),
        test_utils.seq_to_array('A T C G'),
    ])
    y_pred_scores = np.array([
        test_utils.seq_to_one_hot('   ATCG'),
        test_utils.seq_to_one_hot('ATCG   '),
        test_utils.seq_to_one_hot('  ATCG '),
    ])

    # Update 1 is all correct
    accuracy_obj.update_state(y_true, y_pred_scores)
    self.assertEqual(accuracy_obj.result().numpy(), 1.0)

    y_true = np.array([
        test_utils.seq_to_array('C C C C'),
        test_utils.seq_to_array('A T C G'),
        test_utils.seq_to_array('C C C C'),
    ])
    y_pred_scores = np.array([
        test_utils.seq_to_one_hot('   ATCG'),
        test_utils.seq_to_one_hot('ATCG   '),
        test_utils.seq_to_one_hot('  CCCC '),
    ])

    # Update 2 has 1 errors
    accuracy_obj.update_state(y_true, y_pred_scores)
    self.assertAlmostEqual(accuracy_obj.result().numpy(), 0.833333333)


class PerClassAccuracyTest(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='all correct',
          y_true=np.array([[0, 1, 0, 0]]),
          y_pred_scores=np.array([[
              test_utils.get_one_hot(0),
              test_utils.get_one_hot(1),
              test_utils.get_one_hot(0),
              test_utils.get_one_hot(0),
          ]]),
          class_value=1,
          exp_accuracy=1 / 1,
      ),
      dict(
          testcase_name='all positions correct for given class value',
          y_true=np.array([[0, 1, 0, 0]]),
          y_pred_scores=np.array([[
              test_utils.get_one_hot(0),
              test_utils.get_one_hot(1),
              test_utils.get_one_hot(1),
              test_utils.get_one_hot(1),
          ]]),
          class_value=1,
          exp_accuracy=1.0,
      ),
      dict(
          testcase_name='some positions incorrect for given class value',
          y_true=np.array([[0, 1, 1, 1]]),
          y_pred_scores=np.array([[
              test_utils.get_one_hot(0),
              test_utils.get_one_hot(1),
              test_utils.get_one_hot(0),
              test_utils.get_one_hot(0),
          ]]),
          class_value=1,
          exp_accuracy=1 / 3,
      ),
      dict(
          testcase_name='given class value not present',
          y_true=np.array([[0, 1, 1, 1]]),
          y_pred_scores=np.array([[
              test_utils.get_one_hot(0),
              test_utils.get_one_hot(1),
              test_utils.get_one_hot(0),
              test_utils.get_one_hot(0),
          ]]),
          class_value=4,
          # Metric is initialized as 0.
          exp_accuracy=0.0,
      ),
  )
  def test_accuracy(self, y_true, y_pred_scores, class_value, exp_accuracy):
    """Checks that per-class accuracy is correct."""
    accuracy_obj = losses_and_metrics.PerClassAccuracy(class_value=class_value)
    accuracy_obj.update_state(y_true, y_pred_scores)
    self.assertAlmostEqual(accuracy_obj.result().numpy(), exp_accuracy)


class LeftShiftTrueLabels(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='Convert internal gaps',
          sequences=(
              ['TTAGGC    ', 'AGCTGG    '],
              ['T T A G GC', 'A   G CTGG'],
          ),
      ),
      dict(
          testcase_name='Do not convert internal gaps',
          sequences=(
              ['TTAGGC    ', 'AGCTGG    '],
              ['T T A G GC', 'A   G CTGG'],
          ),
      ),
  )
  def test_left_shift_sequence(self, sequences):
    """Checks that edit distance calculation matches expected value."""
    y_true, y_true_gapped = sequences
    y_true = test_utils.multiseq_to_array(y_true)
    y_true_gapped = test_utils.multiseq_to_array(y_true_gapped)

    y_true_ungapped = losses_and_metrics.left_shift_sequence(y_true_gapped)
    self.assertTrue(bool(tf.reduce_all(y_true == y_true_ungapped)))


class XentropySubsCostFn(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='Equal lengths',
          b=2,
          m=4,
          n=4,
          seed=0,
          dtype=tf.float32,
      ),
      dict(
          testcase_name='Unequal lengths',
          b=2,
          m=4,
          n=6,
          seed=0,
          dtype=tf.float32,
      ),
  )
  def test_xentropy_subs_cost_fn(self, b, m, n, seed, dtype):
    """Checks that pointwise XEntropy values agree with tf.keras.losses."""
    # Generates random data.
    n_tokens = dc_constants.SEQ_VOCAB_SIZE
    n_base_tokens = len(dc_constants.ALLOWED_BASES)

    y_true = tf.argmax(
        tf.random.stateless_normal([b, m, n_base_tokens], [seed, 0]), -1
    )
    y_true_oh = tf.one_hot(y_true, n_tokens, dtype=dtype)

    y_pred = tf.random.stateless_uniform(
        [b, n, n_tokens], [seed, 1], dtype=dtype
    )
    y_pred = y_pred / tf.reduce_sum(y_pred, -1, True)

    xent = losses_and_metrics.xentropy_subs_cost_fn(y_true_oh, y_pred)
    # Compares with tf.losses.sparse_categorical_crossentropy as reference.
    for i in range(m):
      for j in range(n):
        y_true_i, y_pred_j = y_true[:, i], y_pred[:, j]
        xent_ij = tf.losses.sparse_categorical_crossentropy(y_true_i, y_pred_j)
        self.assertTrue(np.allclose(xent[:, i, j], xent_ij))


class XentropyInsCostFn(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='Base case',
          b=4,
          n=8,
          seed=0,
          dtype=tf.float32,
      ),
  )
  def test_xentropy_subs_cost_fn(self, b, n, seed, dtype):
    """Checks that pointwise XEntropy values agree with tf.keras.losses."""
    # Generates random data.
    gap_token = dc_constants.SEQ_VOCAB.find(dc_constants.GAP)
    n_tokens = len(dc_constants.SEQ_VOCAB)

    y_pred = tf.random.stateless_uniform(
        [b, n, n_tokens], [seed, 0], dtype=dtype
    )
    y_pred = y_pred / tf.reduce_sum(y_pred, -1, True)

    xent = losses_and_metrics.xentropy_ins_cost_fn(y_pred)
    # Compares with tf.losses.sparse_categorical_crossentropy as reference.
    y_true = gap_token * tf.ones([b, n], dtype=tf.int32)
    xent_keras = tf.losses.sparse_categorical_crossentropy(y_true, y_pred)
    self.assertTrue(np.allclose(xent, xent_keras))


class AlignmentLossTest(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='Hard, identical sequences, no pad',
          sequences=(['TTAGGC', 'AGCTGG'], ['TTAGGC', 'AGCTGG']),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=0.0,
          width=None,
      ),
      dict(
          testcase_name='Hard, identical sequences, with same pad',
          sequences=(
              ['TTAGGC    ', 'AGCTGG    '],
              ['TTAGGC    ', 'AGCTGG    '],
          ),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=0.0,
          width=None,
      ),
      dict(
          testcase_name='Hard, identical sequences, with different pad',
          sequences=(['TTAGGCAT', 'AGCTGG  '], ['TTAGGCAT  ', 'AGCTGG    ']),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=0.0,
          width=None,
      ),
      dict(
          testcase_name='Hard, correct insertions only, no pad',
          sequences=(['TTAGGC', 'AGCTGG'], ['T TA G G C', 'AGC    TGG']),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=0.0,
          width=None,
      ),
      dict(
          testcase_name='Hard, correct insertions only, with pad',
          sequences=(
              ['TTAGGC    ', 'AGCTGG    '],
              ['TTA G GC  ', 'AGC    TGG'],
          ),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=0.0,
          width=None,
      ),
      dict(
          testcase_name='Hard, one deletion at cost one, with pad',
          sequences=(['TTAGGC', 'AGCTGG'], ['TTAGG ', 'GCTGG ']),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=1.0,
          width=None,
      ),
      dict(
          testcase_name='Hard, one deletion at cost two, with pad',
          sequences=(['TTAGGC', 'AGCTGG'], ['TAGGC ', 'AGCGG ']),
          del_cost=2.0,
          loss_reg=None,
          expected_loss=2.0,
          width=None,
      ),
      dict(
          testcase_name='Hard, two deletions at cost one, with pad',
          sequences=(['TTAGGC', 'AGCTGG'], ['TTAG  ', 'GCGG  ']),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=2.0,
          width=None,
      ),
      dict(
          testcase_name='Hard, one error, no pad',
          sequences=(['TTAGGC', 'AGCTGG'], ['ATAGGC', 'TGCTGG']),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=16.118,  # log(eps), with eps = 1e-7
          width=None,
      ),
      dict(
          testcase_name='Hard, two errors, no pad',
          sequences=(['TTAGGC', 'AGCTGG'], ['AAAGGC', 'TGCTGC']),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=32.236,  # 2*log(eps), with eps = 1e-7
          width=None,
      ),
      dict(
          testcase_name='Hard, one erroneous insertion, no pad',
          sequences=(
              ['TTAGGC', 'ATCGAC', 'AGCTGG'],
              ['TTAGGCA', 'ATCCGAC', 'CAGCTGG'],
          ),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=16.118,  # log(eps), with eps = 1e-7
          width=None,
      ),
      dict(
          testcase_name='Hard, one deletion, small deletion cost, with pad',
          sequences=(['ATCG ', 'ATCG '], ['TCG  ', 'TCG  ']),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=1.0,
          width=None,
      ),
      dict(
          testcase_name='Hard, one deletion, large deletion cost, with pad',
          sequences=(['ATCG ', 'ATCG '], ['TCG  ', 'TCG  ']),
          del_cost=1e9,
          loss_reg=None,
          expected_loss=64.472,  # 4*log(eps), with eps = 1e-7
          width=None,
      ),
      # TODO: included test cases for soft alignment.
      dict(
          testcase_name='with band, identical sequences',
          sequences=(['TTAGGC', 'AGCTGG'], ['TTAGGC', 'AGCTGG']),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=0.0,
          width=2,
      ),
      dict(
          testcase_name='with band, one deletion at cost one, with pad',
          sequences=(['TTAGGC', 'AGCTGG'], ['TTAGG ', 'GCTGG ']),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=1.0,
          width=2,
      ),
      dict(
          testcase_name='with band, identical sequences, with same pad',
          sequences=(
              ['TTAGGC    ', 'AGCTGG    '],
              ['TTAGGC    ', 'AGCTGG    '],
          ),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=0.0,
          width=1,
      ),
      dict(
          testcase_name='with band, correct insertions only, no pad',
          sequences=(['TTAGGC   ', 'AGCTG   G'], ['T TAG G C', 'AGC   TGG']),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=0.0,
          width=8,
      ),
      dict(
          testcase_name='with band, correct insertions only, with pad',
          sequences=(
              ['TTAGGC    ', 'AGCTGG    '],
              ['TTA G GC  ', 'AGC    TGG'],
          ),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=0.0,
          width=8,
      ),
      dict(
          testcase_name='with band, two errors, no pad',
          sequences=(['TTAGGC', 'AGCTGG'], ['AAAGGC', 'TGCTGC']),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=32.236,  # 2*log(eps), with eps = 1e-7
          width=4,
      ),
      dict(
          testcase_name='with band of 2, two dels, one align, two pads',
          sequences=(['TTA', 'GGC'], ['A  ', 'C  ']),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=2.0,
          width=2,
      ),
      dict(
          testcase_name='with band of 1,one del, one align, two pads, one del',
          sequences=(['TTA', 'GGC'], ['A  ', 'C  ']),
          del_cost=1.0,
          loss_reg=None,
          expected_loss=18.118,  # 2.0 + log(eps), with eps = 1e-7
          width=1,
      ),
  )
  def test_alignment_loss(
      self, sequences, del_cost, loss_reg, width, expected_loss
  ):
    """Checks that edit distance calculation matches expected value."""
    y_true, y_pred_scores = test_utils.convert_seqs(sequences)
    loss_obj = losses_and_metrics.AlignmentLoss(
        del_cost=del_cost, loss_reg=loss_reg, width=width
    )
    loss = loss_obj(y_true, y_pred_scores)
    self.assertAlmostEqual(float(loss), expected_loss, places=2)


class AlignmentMetricTest(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='Identical sequences, no pad',
          sequences=(['TTAGGC', 'AGCTGG'], ['TTAGGC', 'AGCTGG']),
          matching_score=2.0,
          mismatch_penalty=5.0,
          gap_open_penalty=5.0,
          gap_extend_penalty=4.0,
          expected_pid=(1.0, 1.0),
      ),
      dict(
          testcase_name='Two errors, no pad',
          sequences=(['TTAGGC', 'AGCTGG'], ['AAAGGC', 'TGCTGC']),
          matching_score=2.0,
          mismatch_penalty=5.0,
          gap_open_penalty=5.0,
          gap_extend_penalty=4.0,
          expected_pid=(0.667, 0.667),
      ),
      dict(
          testcase_name='Correct insertions only, no pad.',
          sequences=(['TTAGGC', 'AGCTGG'], ['T TA G G C', 'AGC    TGG']),
          matching_score=2.0,
          mismatch_penalty=5.0,
          gap_open_penalty=5.0,
          gap_extend_penalty=4.0,
          expected_pid=(1.0, 1.0),
      ),
      dict(
          testcase_name='One deletion, with pad.',
          sequences=(['TTAGGC', 'AGCTGG'], ['TTAGG ', 'GCTGG ']),
          matching_score=2.0,
          mismatch_penalty=5.0,
          gap_open_penalty=5.0,
          gap_extend_penalty=4.0,
          expected_pid=(0.833, 0.833),
      ),
      dict(
          testcase_name='One erroneous insertion, no pad.',
          sequences=(
              ['TTAGGC', 'ATCGAC', 'AGCTGG'],
              ['TTAGGCA', 'ATCCGAC', 'CAGCTGG'],
          ),
          matching_score=2.0,
          mismatch_penalty=5.0,
          gap_open_penalty=5.0,
          gap_extend_penalty=4.0,
          expected_pid=(0.857, 0.857, 0.857),
      ),
      dict(
          testcase_name='One deletion, shorter, with pad.',
          sequences=(['ATCG ', 'ATCG '], ['TCG  ', 'TCG  ']),
          matching_score=2.0,
          mismatch_penalty=5.0,
          gap_open_penalty=5.0,
          gap_extend_penalty=4.0,
          expected_pid=(0.75, 0.75),
      ),
      dict(
          testcase_name='Empty predictions.',
          sequences=(['ATCG ', 'ATCG '], ['     ', '     ']),
          matching_score=2.0,
          mismatch_penalty=5.0,
          gap_open_penalty=5.0,
          gap_extend_penalty=4.0,
          expected_pid=(0.0, 0.0),
      ),
      dict(
          testcase_name='Empty ground-truth.',
          sequences=(['     ', '     '], ['ATCG ', 'ATCG ']),
          matching_score=2.0,
          mismatch_penalty=5.0,
          gap_open_penalty=5.0,
          gap_extend_penalty=4.0,
          expected_pid=(0.0, 0.0),
      ),
      dict(
          testcase_name='Empty predictions, ground-truth length one.',
          sequences=(['A    ', 'T    '], ['     ', '     ']),
          matching_score=2.0,
          mismatch_penalty=5.0,
          gap_open_penalty=5.0,
          gap_extend_penalty=4.0,
          expected_pid=(0.0, 0.0),
      ),
      dict(
          testcase_name='Empty ground-truth, predictions length one.',
          sequences=(['     ', '     '], ['A    ', 'T    ']),
          matching_score=2.0,
          mismatch_penalty=5.0,
          gap_open_penalty=5.0,
          gap_extend_penalty=4.0,
          expected_pid=(0.0, 0.0),
      ),
      dict(
          testcase_name='Both empty.',
          sequences=(['     ', '     '], ['     ', '     ']),
          matching_score=2.0,
          mismatch_penalty=5.0,
          gap_open_penalty=5.0,
          gap_extend_penalty=4.0,
          expected_pid=(1.0, 1.0),
      ),  # Expected PID defined as special case.
  )
  def test_alignment_metric(
      self,
      sequences: Tuple[Sequence[str], Sequence[str]],
      matching_score: float,
      mismatch_penalty: float,
      gap_open_penalty: float,
      gap_extend_penalty: float,
      expected_pid: Tuple[float],
  ):
    y_true, y_pred_scores = test_utils.convert_seqs(sequences)
    alignment_metric_obj = losses_and_metrics.AlignmentMetric(
        matching_score=matching_score,
        mismatch_penalty=mismatch_penalty,
        gap_open_penalty=gap_open_penalty,
        gap_extend_penalty=gap_extend_penalty,
    )
    pid = alignment_metric_obj.alignment(y_true, y_pred_scores)[2]['pid']
    for i, _ in enumerate(sequences):
      self.assertAlmostEqual(float(pid[i]), expected_pid[i], places=2)


class AlignmentIdentityBatchMetricTest(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='Identical sequences.',
          pred_seqs=['TTAGGC', 'AGCTGG'],
          ccs_seqs=['TTAGGC', 'AGCTGG'],
          label_seqs=['TTAGGC', 'AGCTGG'],
          alignment_metric_obj=losses_and_metrics.AlignmentMetric(),
          expected_pid_pred=1.0,
          expected_pid_ccs=1.0,
      ),
      dict(
          testcase_name='3 mismatches in CCS, 6 in DC over multiple examples.',
          pred_seqs=['CCCCCC', 'TGCTGG'],
          ccs_seqs=['CCAGGC', 'TGCTGG'],
          label_seqs=['TTAGGC', 'AGCTGG'],
          alignment_metric_obj=losses_and_metrics.AlignmentMetric(),
          expected_pid_pred=0.5,
          expected_pid_ccs=0.75,
      ),
      dict(
          testcase_name='Empty CCS, DC, and label.',
          pred_seqs=['     ', '     '],
          ccs_seqs=['     ', '     '],
          label_seqs=['     ', '     '],
          alignment_metric_obj=losses_and_metrics.AlignmentMetric(),
          expected_pid_pred=1.0,
          expected_pid_ccs=1.0,
      ),  # Expected PID defined as special case.
  )
  def test_get_batch_identity_ccs_pred(
      self,
      pred_seqs: Sequence[str],
      ccs_seqs: Sequence[str],
      label_seqs: Sequence[str],
      alignment_metric_obj: losses_and_metrics.AlignmentMetric,
      expected_pid_pred: float,
      expected_pid_ccs: float,
  ):
    """Checks per batch identity for DeepConsensus and CCS."""

    sequences = tuple((label_seqs, pred_seqs))
    labels, predictions = test_utils.convert_seqs(sequences)
    ccs = test_utils.multiseq_to_array(ccs_seqs).astype(
        dc_constants.NP_DATA_TYPE
    )

    # Calculate identity per batch for CCS and DC.
    (identity_ccs, identity_pred) = (
        losses_and_metrics.get_batch_identity_ccs_pred(
            ccs, predictions, labels, alignment_metric_obj
        )
    )
    self.assertAlmostEqual(identity_pred.numpy(), expected_pid_pred, places=2)
    self.assertAlmostEqual(identity_ccs.numpy(), expected_pid_ccs, places=2)


class YieldOverCCSMetricTest(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='CCS and DC have the same yield.',
          quality_threshold=0.99,
          identities_dc=[1.0, 1.0],
          identities_ccs=[1.0, 1.0],
          exp_yields_dc=[1.0, 2.0],
          exp_yields_ccs=[1.0, 2.0],
          exp_yields_over_ccs=[1.0, 1.0],
      ),
      dict(
          testcase_name='DC yield < CCS yield.',
          quality_threshold=0.99,
          identities_dc=[0.9, 1.0],
          identities_ccs=[1.0, 1.0],
          exp_yields_dc=[0.0, 1.0],
          exp_yields_ccs=[1.0, 2.0],
          exp_yields_over_ccs=[0.0, 0.5],
      ),
      dict(
          testcase_name='DC yield > CCS yield.',
          quality_threshold=0.99,
          identities_dc=[1.0, 1.0],
          identities_ccs=[0.9, 1.0],
          exp_yields_dc=[1.0, 2.0],
          exp_yields_ccs=[0.0, 1.0],
          exp_yields_over_ccs=[0.0, 2.0],
      ),
      dict(
          testcase_name='DC yield >= CCS yield, low CCS identity in 2nd batch.',
          quality_threshold=0.99,
          identities_dc=[1.0, 1.0],
          identities_ccs=[1.0, 0.9],
          exp_yields_dc=[1.0, 2.0],
          exp_yields_ccs=[1.0, 1.0],
          exp_yields_over_ccs=[1.0, 2.0],
      ),
      dict(
          testcase_name='Lower identity quality threshold.',
          quality_threshold=0.9,
          identities_dc=[0.9, 1.0],
          identities_ccs=[1.0, 1.0],
          exp_yields_dc=[1.0, 2.0],
          exp_yields_ccs=[1.0, 2.0],
          exp_yields_over_ccs=[1.0, 1.0],
      ),
  )
  def test_yield_over_ccs_metric_multiple_updates(
      self,
      quality_threshold: float,
      identities_dc: List[Sequence[str]],
      identities_ccs: List[Sequence[str]],
      exp_yields_dc: List[float],
      exp_yields_ccs: List[float],
      exp_yields_over_ccs: List[float],
  ):
    """Checks that yield over ccs metrics and attributes match expected values.

    Since during trainig metric values are continually updated, this function
    checks the expected values over multiple updates (after seeing a new batch).

    Args:
      quality_threshold: a float value for thersholding DC and CCS identities.
      identities_dc: List of DC identities for each batch.
      identities_ccs: List of CCS identities for each batch.
      exp_yields_dc: Expected cumulative (over batches) yield for DeepConsensus
        sequences after each update.
      exp_yields_ccs: Expected cumulative (over batches) yield for CCS sequences
        after each update.
      exp_yields_over_ccs: Expected yield over CCS for each metric update.
    """
    yield_over_ccs_obj = losses_and_metrics.YieldOverCCSMetric(
        quality_threshold=quality_threshold, name='yield_over_ccs_metric'
    )

    for (
        identity_ccs,
        identity_pred,
        exp_yield_dc,
        exp_yield_ccs,
        exp_yield_over_ccs,
    ) in zip(
        identities_ccs,
        identities_dc,
        exp_yields_dc,
        exp_yields_ccs,
        exp_yields_over_ccs,
    ):
      # Update metric.
      yield_over_ccs_obj.update_state(identity_ccs, identity_pred)
      # Test accumulated CCS and DC yield.
      self.assertAlmostEqual(
          yield_over_ccs_obj.yield_ccs.numpy(), exp_yield_ccs
      )
      self.assertAlmostEqual(yield_over_ccs_obj.yield_dc.numpy(), exp_yield_dc)
      # Test accumulated yield of DC over CCS.
      self.assertAlmostEqual(
          yield_over_ccs_obj.result().numpy(), exp_yield_over_ccs
      )


def softmax(x):
  """Compute softmax values for logits in x."""
  return np.exp(x) / np.sum(np.exp(x), axis=0)


def distill_loss_per_pos_fn_np(
    teacher_logits, student_logits, temperature, logit_loss_identifier
):
  """Computes per position distillation loss."""
  teacher_probs = softmax(teacher_logits / temperature)
  student_probs = softmax(student_logits / temperature)
  if logit_loss_identifier == 'kl_divergence':
    # Compute the KL divergence.
    loss = np.sum(
        teacher_probs * np.log(teacher_probs / student_probs), axis=-1
    )
  elif logit_loss_identifier == 'mean_squared_error':
    # Compute MSE
    loss = np.square(np.subtract(teacher_probs, student_probs)).mean()
  return loss


class DistillationLossTest(parameterized.TestCase):

  @parameterized.named_parameters(
      dict(
          testcase_name='Temperature=1',
          temperature=1,
          logit_loss_identifier='kl_divergence',
          are_logits_equal=False,
      ),
      dict(
          testcase_name='MSE logit loss type',
          temperature=1,
          logit_loss_identifier='mean_squared_error',
          are_logits_equal=False,
      ),
      dict(
          testcase_name='Temperature=10',
          temperature=10,
          logit_loss_identifier='kl_divergence',
          are_logits_equal=False,
      ),
      dict(
          testcase_name='Student and teacher have the same logits.',
          temperature=1,
          logit_loss_identifier='kl_divergence',
          are_logits_equal=True,
      ),
  )
  def test_distillation_loss_fn(
      self, temperature, logit_loss_identifier, are_logits_equal
  ):
    """Checks that pointwise Distillation values agree with numpy."""
    # Generate random data.
    batch_size = 2
    window_length = 10

    seed_teacher = 0
    if are_logits_equal:
      seed_student = seed_teacher
    else:
      seed_student = seed_teacher + 1
    np.random.seed(seed_teacher)
    teacher_logits = np.random.normal(
        size=(batch_size, window_length, dc_constants.SEQ_VOCAB_SIZE)
    )
    np.random.seed(seed_student)
    student_logits = np.random.normal(
        size=(batch_size, window_length, dc_constants.SEQ_VOCAB_SIZE)
    )

    distill_loss_fn = losses_and_metrics.DistillationLoss(
        temperature=temperature,
        logit_loss=tf.keras.losses.get(logit_loss_identifier),
        reduction=tf.keras.losses.Reduction.NONE,
    )
    expected_loss = distill_loss_fn(
        tf.constant(teacher_logits, dtype=tf.float32),
        tf.constant(student_logits, dtype=tf.float32),
    ).numpy()

    # Compute distillation loss in numpy pointwise.
    for example_ind in range(batch_size):
      distill_loss = 0
      for pos_ind in range(window_length):
        loss_ij = distill_loss_per_pos_fn_np(
            teacher_logits[example_ind, pos_ind, :],
            student_logits[example_ind, pos_ind, :],
            temperature,
            logit_loss_identifier,
        )
        distill_loss = distill_loss + loss_ij
      # Get the distillation loss over the whole window.
      distill_loss = distill_loss / window_length
      self.assertAlmostEqual(distill_loss, expected_loss[example_ind], places=6)


if __name__ == '__main__':
  absltest.main()
