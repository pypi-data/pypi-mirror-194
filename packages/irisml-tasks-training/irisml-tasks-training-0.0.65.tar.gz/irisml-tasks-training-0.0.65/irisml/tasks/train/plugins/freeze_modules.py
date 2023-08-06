"""Freeze parameters as per provided freeze pattern(s)."""

import logging
import re
import torch
from .plugin_base import PluginBase

logger = logging.getLogger(__name__)


class Plugin(PluginBase):
    def __init__(self, freeze_pattern: str):
        """
        Args:
            freeze_pattern (str): A regular expression to find a module. If empty, this plugin does nothing.
        """

        self._freeze_pattern = freeze_pattern and re.compile(freeze_pattern)
        if not freeze_pattern:
            logger.info('No module name patterns provided. Skipping freezing modules.')

    def on_train_epoch_start(self, trainer, model, epoch_index):
        if self._freeze_pattern:
            _freeze(self._freeze_pattern, model, verbose=(epoch_index == 0))
        return True

    def on_train_epoch_end(self, trainer, model, epoch_index):
        model.requires_grad_(True)


def _freeze(freeze_pattern: re.Pattern, model: torch.nn.Module, verbose=False):
    for name, module in model.named_modules():
        if freeze_pattern.search(name):
            if verbose:
                logger.debug(f"Freezing module {name}")
            module.requires_grad_(False)
            module.eval()
