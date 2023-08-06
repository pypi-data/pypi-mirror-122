

.. _sphx_glr_auto_examples_parallel_random_state.py:


===================================
Random state within joblib.Parallel
===================================

Randomness is affected by parallel execution differently by the different
backends.

In particular, when using multiple processes, the random sequence can be
the same in all processes. This example illustrates the problem and shows
how to work around it.



.. code-block:: python


    import numpy as np
    from joblib import Parallel, delayed








A utility function for the example



.. code-block:: python

    def print_vector(vector, backend):
        """Helper function to print the generated vector with a given backend."""
        print('\nThe different generated vectors using the {} backend are:\n {}'
              .format(backend, np.array(vector)))








Sequential behavior
##############################################################################

 ``stochastic_function`` will generate five random integers. When
 calling the function several times, we are expecting to obtain
 different vectors. For instance, we will call the function five times
 in a sequential manner, we can check that the generated vectors are all
 different.



.. code-block:: python



    def stochastic_function(max_value):
        """Randomly generate integer up to a maximum value."""
        return np.random.randint(max_value, size=5)


    n_vectors = 5
    random_vector = [stochastic_function(10) for _ in range(n_vectors)]
    print('\nThe different generated vectors in a sequential manner are:\n {}'
          .format(np.array(random_vector)))





.. rst-class:: sphx-glr-script-out

 Out::

    The different generated vectors in a sequential manner are:
     [[1 1 8 2 3]
     [7 2 4 5 5]
     [3 2 0 0 7]
     [0 1 1 2 7]
     [3 0 5 3 7]]


Parallel behavior
##############################################################################

 Joblib provides three different backend: loky (default), threading, and
 multiprocessing.



.. code-block:: python


    backend = 'loky'
    random_vector = Parallel(n_jobs=2, backend=backend)(delayed(
        stochastic_function)(10) for _ in range(n_vectors))
    print_vector(random_vector, backend)





.. rst-class:: sphx-glr-script-out

 Out::

    The different generated vectors using the loky backend are:
     [[9 2 9 1 0]
     [3 5 0 9 4]
     [9 8 9 9 9]
     [2 6 6 5 5]
     [2 8 7 1 1]]



.. code-block:: python


    backend = 'threading'
    random_vector = Parallel(n_jobs=2, backend=backend)(delayed(
        stochastic_function)(10) for _ in range(n_vectors))
    print_vector(random_vector, backend)





.. rst-class:: sphx-glr-script-out

 Out::

    The different generated vectors using the threading backend are:
     [[2 8 6 3 2]
     [5 8 3 6 3]
     [2 7 3 1 3]
     [6 9 3 9 1]
     [7 6 9 8 4]]


Loky and the threading backends behave exactly as in the sequential case and
do not require more care. However, this is not the case regarding the
multiprocessing backend.



.. code-block:: python


    backend = 'multiprocessing'
    random_vector = Parallel(n_jobs=2, backend=backend)(delayed(
        stochastic_function)(10) for _ in range(n_vectors))
    print_vector(random_vector, backend)





.. rst-class:: sphx-glr-script-out

 Out::

    The different generated vectors using the multiprocessing backend are:
     [[5 8 9 8 6]
     [5 8 9 8 6]
     [7 0 1 4 1]
     [7 0 1 4 1]
     [9 9 0 4 4]]


Some of the generated vectors are exactly the same, which can be a
problem for the application.

Technically, the reason is that all forked Python processes share the
same exact random seed. As a results, we obtain twice the same randomly
generated vectors because we are using ``n_jobs=2``. A solution is to
set the random state within the function which is passed to
:class:`joblib.Parallel`.



.. code-block:: python



    def stochastic_function_seeded(max_value, random_state):
        rng = np.random.RandomState(random_state)
        return rng.randint(max_value, size=5)








``stochastic_function_seeded`` accepts as argument a random seed. We can
reset this seed by passing ``None`` at every function call. In this case, we
see that the generated vectors are all different.



.. code-block:: python


    random_vector = Parallel(n_jobs=2, backend=backend)(delayed(
        stochastic_function_seeded)(10, None) for _ in range(n_vectors))
    print_vector(random_vector, backend)





.. rst-class:: sphx-glr-script-out

 Out::

    The different generated vectors using the multiprocessing backend are:
     [[2 7 4 5 0]
     [5 6 4 2 9]
     [6 8 8 9 2]
     [1 5 4 5 3]
     [6 4 2 2 1]]


Fixing the random state to obtain deterministic results
##############################################################################

 The pattern of ``stochastic_function_seeded`` has another advantage: it
 allows to control the random_state by passing a known seed. So for instance,
 we can replicate the same generation of vectors by passing a fixed state as
 follows.



.. code-block:: python


    random_state = np.random.randint(np.iinfo(np.int32).max, size=n_vectors)

    random_vector = Parallel(n_jobs=2, backend=backend)(delayed(
        stochastic_function_seeded)(10, rng) for rng in random_state)
    print_vector(random_vector, backend)

    random_vector = Parallel(n_jobs=2, backend=backend)(delayed(
        stochastic_function_seeded)(10, rng) for rng in random_state)
    print_vector(random_vector, backend)




.. rst-class:: sphx-glr-script-out

 Out::

    The different generated vectors using the multiprocessing backend are:
     [[1 7 2 6 8]
     [1 3 7 5 8]
     [6 1 7 8 9]
     [0 9 3 1 1]
     [1 3 5 8 8]]

    The different generated vectors using the multiprocessing backend are:
     [[1 7 2 6 8]
     [1 3 7 5 8]
     [6 1 7 8 9]
     [0 9 3 1 1]
     [1 3 5 8 8]]


**Total running time of the script:** ( 0 minutes  0.803 seconds)



.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: parallel_random_state.py <parallel_random_state.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: parallel_random_state.ipynb <parallel_random_state.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.readthedocs.io>`_
