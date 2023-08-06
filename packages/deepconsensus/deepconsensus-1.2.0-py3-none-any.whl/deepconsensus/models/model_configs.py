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
"""Architecture and training hyperparameters for networks."""
# pylint: disable=line-too-long
import os

from typing import Optional
import ml_collections
from ml_collections import config_dict

# Do not add any additional imports to the config.
# It can lead to circular dependencies easily and should not be necessary
# for setting parameters.

############### Base params for different model architectures ###############


def _set_base_fc_hparams(params):
  """Updates given params with base values for the fully connected model."""
  # Architecture
  params.model_name = 'fc'
  params.fc_size = [256, 512, 256, 128]
  params.fc_dropout = 0.0

  params.num_channels = 1

  params.per_base_hidden_size = 1
  params.pw_hidden_size = 1
  params.ip_hidden_size = 1
  params.strand_hidden_size = 1
  params.ccs_bq_hidden_size = 1
  params.sn_hidden_size = 1

  # Training
  params.l2 = 0.0
  params.batch_size = 256
  params.num_epochs = 15
  params.num_epochs_for_decay = 15
  params.buffer_size = 1_000_000

  # Optimizer params (optimized for transformer).
  params.initial_learning_rate = 3.6246e-3
  params.end_learning_rate = 2.86594e-5
  params.warmup_steps = 35536
  params.weight_decay_rate = 6.9868e-3
  params.beta_1 = 0.9
  params.beta_2 = 0.999
  params.epsilon = 1e-6


def _set_base_transformer_hparams(params):
  """Updates given config with base values for the Transformer model."""
  # Architecture
  params.model_name = 'transformer'
  params.add_pos_encoding = True
  # Num heads should be divisible by hidden size. This value should be tuned for
  # the production setting. TODO: update this parameter after
  # tuning.
  params.num_heads = 2
  params.layer_norm = False
  # Whether to use ReZero instead of LayerNorms.
  params.rezero = True
  params.condense_transformer_input = False
  params.transformer_model_size = 'base'

  # The width of the band for mask-based attention is (2 * attn_win_size + 1).
  # Set to None to use full attention.
  params.attn_win_size = 12

  params.num_channels = 1
  params.per_base_hidden_size = 1
  params.pw_hidden_size = 1
  params.ip_hidden_size = 1
  params.sn_hidden_size = 1
  params.ccs_bq_hidden_size = 1
  params.strand_hidden_size = 1

  # Dropout values (only used when training).
  params.layer_postprocess_dropout = 0.1
  params.attention_dropout = 0.1
  params.relu_dropout = 0.1

  # Training
  params.batch_size = 256
  # We use this number of epochs to obtain fast training results.
  params.num_epochs = 9
  # We use this number of epochs to obtain the finalized models. This parameter
  # keeps the learning rate schedule the same when num_epochs is changed.
  params.num_epochs_for_decay = 9
  params.buffer_size = 1_000_000

  # Optimizer params (values obtained in b/246369335#comment3).
  params.initial_learning_rate = 3.6246e-3
  params.end_learning_rate = 2.86594e-5
  params.warmup_steps = 35536
  params.weight_decay_rate = 6.9868e-3
  params.beta_1 = 0.9
  params.beta_2 = 0.999
  params.epsilon = 1e-6


def _set_transformer_learned_embeddings_hparams(params):
  """Updates given config with values for the learned embeddings transformer."""
  _set_base_transformer_hparams(params)
  params.model_name = 'transformer_learn_values'
  params.per_base_hidden_size = 8
  params.pw_hidden_size = 8
  params.ip_hidden_size = 8
  params.strand_hidden_size = 2
  params.sn_hidden_size = 8
  params.ccs_bq_hidden_size = 8

  params.condense_transformer_input = True
  params.transformer_input_size = 280


def _set_custom_data_hparams(params):
  """Updates the given config with values for custom dataset (subreads are aligned to CCS)."""
  params.tf_dataset = [
      '/path_to_training_data'
  ]  # This needs to point to the actual training examples
  params.max_passes = 20


def _set_transformer_learned_embeddings_distill_hparams(params):
  """Updates given config with values for the distilled transformer."""
  _set_transformer_learned_embeddings_hparams(params)
  params.model_name = 'transformer_learn_values_distill'

  # Student architecture parameters.
  params.num_hidden_layers = 5
  params.filter_size = 2048

  # Dropout values (only used when training).
  params.layer_postprocess_dropout = 0.0
  params.attention_dropout = 0.1
  params.relu_dropout = 0.0

  # Whether to initialize encoder layers using the teacher model.
  params.init_encoder_stack = True
  # Whether to initialize non-encoder layers using the teacher model.
  params.init_nonencoder_layers = True
  # The order of indices in params.teacher_encoder_layers and
  # params.student_encoder_layers determines the layer to layer initialization.
  params.teacher_encoder_layers = [1, 2, 3, 4, 5]
  params.student_encoder_layers = [0, 1, 2, 3, 4]
  if params.init_encoder_stack:
    assert len(params.teacher_encoder_layers) == len(
        params.student_encoder_layers
    )
    assert len(params.student_encoder_layers) == params.num_hidden_layers
    assert max(params.student_encoder_layers) < params.num_hidden_layers

  # Optimizer parameters.
  params.warmup_steps = 0

  # Distillation loss parameters.
  # Weight corresponding to the distillation loss.
  params.distill_alpha = 1.0e5
  # Weight corresponding to the student loss.
  params.student_alpha = 1.0
  # Temperature for softening probability distributions.
  params.temperature = 1.0
  # Loss type for comparing teacher and student logits (e.g. kl_divergence).
  params.logit_loss_identifier = 'mean_squared_error'




############### Base params for different datasets ###############


def _set_test_data_hparams(params):
  """Updates the given config with values for a test dataset."""
  curr_dir = os.path.dirname(__file__)
  params.train_path = [
      os.path.join(curr_dir, '../testdata/human_1m/tf_examples/train/*')
  ]
  # Use same data for train/eval/hard eval because the eval test data is empty.
  params.eval_path = params.train_path
  params.test_path = params.train_path
  params.inference_path = os.path.join(
      curr_dir, '../testdata/human_1m/tf_examples/inference/*'
  )
  params.n_examples_train = 253
  params.n_examples_eval = 253
  params.max_passes = 20

  # The test dataset uniquely sets these model-level parameters because the test
  # dataset is small and we want to keep model files small.
  params.batch_size = 1
  params.num_epochs = 1
  params.buffer_size = 10
  if params.model_name == 'fc':
    params.fc_size = [4, 4]


def _set_test_bq_data_hparams(params):
  """Updates the given config with values for a test dataset."""
  curr_dir = os.path.dirname(__file__)
  params.use_ccs_bq = True
  params.train_path = [
      os.path.join(curr_dir, '../testdata/human_1m/tf_examples_bq/train/*')
  ]
  # Use same data for train/eval/hard eval because the eval test data is empty.
  params.eval_path = params.train_path
  params.test_path = params.train_path
  params.inference_path = os.path.join(
      curr_dir, '../testdata/human_1m/tf_examples_bq/inference/*'
  )
  params.n_examples_train = 253
  params.n_examples_eval = 253
  params.max_passes = 20

  # The test dataset uniquely sets these model-level parameters because the test
  # dataset is small and we want to keep model files small.
  params.batch_size = 1
  params.num_epochs = 1
  params.buffer_size = 10
  if params.model_name == 'fc':
    params.fc_size = [4, 4]


############### Core function for setting all config values ###############


def get_config(config_name: Optional[str] = None) -> ml_collections.ConfigDict:
  """Returns the default configuration as instance of ConfigDict.

  Valid config names must consist of two parts: {model_name}+{dataset_name}. The
  "+" must be present as a separator between the two parts. For example,
  transformer_learn_values+ccs is a valid name.

  Valid model names include:
    * fc
    * transformer
    * transformer_learn_values

  Valid dataset names include:
    * ecoli
    * ccs
    * poa
    * test

  Args:
    config_name: String consisting of two parts, model name and dataset name,
      separated by a "+".

  Returns:
    A config dictionary containing the valid configs for the model and dataset
    specified.
  """
  params = ml_collections.ConfigDict()

  # Used for generating replicates.
  params.trial = 1

  # Defaults for backward compatibilitiy
  # Older models initiate with the default config, so initialize those values
  # here to set for older models.
  params.rezero = False

  # Base config
  params.PW_MAX = 255
  params.IP_MAX = 255
  params.SN_MAX = 500
  params.CCS_BQ_MAX = 95
  params.STRAND_MAX = 2

  # Features
  params.use_bases = True
  params.use_pw = True
  params.use_ip = True
  params.use_strand = True
  params.use_sn = True
  params.use_ccs = True
  params.use_ccs_bq = False
  params.per_base_hidden_size = 1
  params.pw_hidden_size = 1
  params.ip_hidden_size = 1
  params.sn_hidden_size = 1
  params.strand_hidden_size = 1
  params.ccs_bq_hidden_size = 1

  params.total_rows = config_dict.placeholder(int)

  # Specify common configs here.
  params.vocab_size = 5
  params.tensorboard_update_freq = 'batch'
  params.model_checkpoint_freq = 'epoch'
  params.seed = 1
  params.remove_label_gaps = False
  params.loss_function = 'alignment_loss'

  # AlignmentLoss parameters
  params.del_cost = 10.0
  params.loss_reg = 0.1
  params.band_width = None

  # Window
  params.max_length = 100

  # Default model and dataset
  params.model_config_name = 'transformer_learn_values'
  params.dataset_config_name = 'ccs'

  # CNN-specific
  params.conv_model = 'resnet50'


  # Scaling factor to multiply the batch_size when using TPUs since they have
  # more memory than GPUs.
  params.tpu_scale_factor = 1

  # Allow for a base config to be loaded when no config_name is passed.
  if config_name is None:
    return params

  model_config_name, dataset_config_name = config_name.split('+')
  params.model_config_name = model_config_name
  params.dataset_config_name = dataset_config_name
  params.tf_dataset = None
  params.limit = -1
  if model_config_name == 'fc':
    _set_base_fc_hparams(params)
  elif model_config_name == 'transformer':
    _set_base_transformer_hparams(params)
  elif model_config_name == 'transformer_learn_values':
    _set_transformer_learned_embeddings_hparams(params)
  elif model_config_name == 'transformer_learn_values_distill':
    _set_transformer_learned_embeddings_distill_hparams(params)
  else:
    raise ValueError('Unknown model_config_name: %s' % model_config_name)

  if dataset_config_name == 'poa':
    _set_human_aligned_to_poa_data_hparams(params)
  elif dataset_config_name == 'ccs':
    _set_human_aligned_to_ccs_data_hparams(params)
  elif dataset_config_name == 'ccs_test':
    _set_human_test_set_ccs_hparams(params)
  elif dataset_config_name == 'ecoli':
    _set_ecoli_data_hparams(params)
  elif dataset_config_name == 'test':
    _set_test_data_hparams(params)
  elif dataset_config_name == 'test_bq':
    _set_test_bq_data_hparams(params)
  elif dataset_config_name == 'custom':
    _set_custom_data_hparams(params)
  else:
    raise ValueError(
        'dataset_config_name is %s. Must be one of the following: '
        'ccs, poa, ecoli, test' % dataset_config_name
    )
  return params
