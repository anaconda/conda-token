===============================
Conda token
===============================

.. image:: https://img.shields.io/conda/v/anaconda/conda-token.svg
   :target: https://anaconda.org/anaconda/conda-token

.. sectnum::

Set your token and configure ``default_channels`` to access Anaconda Commercial Edition. Follow the steps below
to use ``conda-token`` to authenticate and configure your Anaconda or Miniconda install.

``conda-token`` will configure your Anaconda or Miniconda instllation to authenticate to Anaconda Commercial Edition
using the token you receive in your email after purchasing a subscription and will configure your ``default_channels``
setting in your Conda configuration.

Purchase Commercial Edition
---------------------------

After you have purchased a subscription to Commercial Edition at https://anaconda.cloud/register you will receive
an email containing an access token. 
The token is 48 characters in lengths and contains letters and numbers. You will need this token to authenticate
your Anaconda or Miniconda install

Install Anaconda or Miniconda
-----------------------------

If you already have Anaconda or Miniconda installed you can skip this step.
Otherwise download either `Anaconda`_ or `Miniconda`_ and install it on your system.


Install conda-token
-------------------

The ``conda-token`` package is available from the Anaconda Distribution.
You can install ``conda-token`` using either Anaconda Navigator or the Conda command-line-interface (CLI).

To use the Conda CLI run the following in your terminal

.. code-block:: text

   conda install conda-token


Authenticate to Anaconda Commercial Edition
-------------------------------------------

You will need to use the terminal to authenticate to Anaconda Commercial Edition and configure access.
In your terminal run the following command

.. code-block:: text

   conda-token set <TOKEN>

Replace ``<TOKEN>`` with the token value you received in your email after purchasing a subscription.

``conda-token`` will validate that your token works by checking that it can be used to connect to Anaconda Commercial
Edition.

Once you have run ``conda-token set`` you will be able to install packages from Anaconda Commercial Edition

Run ``conda-token set --help`` for more information and optional configuration parameters.


Remove token and reset Conda configuration
------------------------------------------

You can remove your token and reset your Conda configuration to its default state by running

.. code-block:: text

   conda-token remove


.. _`Anaconda`: https://anaconda.com/download
.. _`Miniconda`: https://docs.conda.io/en/latest/miniconda.html