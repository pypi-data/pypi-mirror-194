# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['separability']

package_data = \
{'': ['*']}

install_requires = \
['accelerate>=0.16.0,<0.17.0',
 'datasets>=2.9.0,<3.0.0',
 'dict-deep>=4.1.2,<5.0.0',
 'einops>=0.6.0,<0.7.0',
 'evaluate>=0.4.0,<0.5.0',
 'ipykernel>=6.21.1,<7.0.0',
 'ipywidgets>=8.0.4,<9.0.0',
 'matplotlib>=3.6.3,<4.0.0',
 'numexpr>=2.7.0,<3.0.0',
 'numpy>=1.23,<2.0',
 'pandas>=1.5.3,<2.0.0',
 'tensorboard>=2.11.2,<3.0.0',
 'tensorboardx>=2.5.1,<3.0.0',
 'torch>=1.13.0,<2.0.0',
 'transformers>=4.26.0,<5.0.0',
 'wandb>=0.13.9,<0.14.0',
 'welford-torch>=0.1.2,<0.2.0',
 'zstandard>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'separability',
    'version': '0.1.4',
    'description': 'separability of LLM Capabilities',
    'long_description': "# separability\n\nMy basic library for studying LLMs (currently, only the Meta OPT models).\nThis includes functions for analysing the activations of the models for different inputs, and for pruning different parts of the model based on those activations.\n\n## Pruning based on Capabilities\n\nFor a full example, see `src/separability.ipynb`.\n\nThe simple example is:\n```\nfrom model import Model\nfrom activations import prune_and_evaluate, evaluate_all\n\n#\xa0Load and Evaluate Model on Pile and Code\n\nopt = Model('125m', limit=1000)\neval_data = evaluate_all(opt, 1e5)\nprint(eval_data)\n\n#\xa0Prune Model, Removing coding capabilities (compared to pile), and evaluate\n\neval_data = prune_and_evaluate(opt, ff_prune_frac=0.05, attn_prune_frac=0.05,\n    ff_eps=1e-3, sample_size=1e5, eval_size=1e5, cripple='code', focus='pile')\nprint(eval_data)\n```\n\n## model.py\nThis defines a wrapper function that encapsulates the HuggingFace implementation of Meta OPT.\nTo get the model, simply run:\n\n```\nfrom model import Model\n\nopt = Model('125m', limit=1000)\n```\n\nWhere you can provide any of the model sizes that are pre-trained for OPT, and the token limit must be smaller than the max token length that the model is able to handle.\n\nNext, you can run the model to do 2 tokens of predictions, by, for example, running:\n```\ntext = 'Hello, my name is'\ninpt, output = opt.predict( text, num=2 )\n```\n\nWe can look at the residual stream of how the output changes over time.\n```\nresidual_stream = opt.get_residual_stream( text )\n```\nThis will return a tensor of size `2 + 2*n_layers`.\ni.e:\n- the input (w/ positional encoding)\n- n attention layer outputs\n- n feed forward layer outputs\n- the final output\n\nIf we want just the output of the attention / feed forward layers, we can instead look at the activations:\n```\ninpt, attn_out, ff_out, output = opt.get_text_activations( text )\n```\nor alternatively:\n```\ninpt, attn_out, ff_out, output = opt.get_text_activations( residual_stream=residual_stream )\n```\n\nTo get the activations for the input text at all of the MLP mid layers, we can look at:\n`opt.get_ff_key_activations( text )` or `opt.get_ff_key_activations( residual_stream=residual_stream )`.\n\n## texts.py\nHas some basic tools for loading the two text datasets I am using:\n- 'the_pile' ( validation set of The Pile )\n- 'codeparrot-clean-valid' ( validation set of codeparrot )\n\n## activations.py\nHas code specific to the two datasets I am using to analyze and attempt to remove capabilities from the OPT.\n\n",
    'author': 'Nicky Pochinkov',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pesvut/separability',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
