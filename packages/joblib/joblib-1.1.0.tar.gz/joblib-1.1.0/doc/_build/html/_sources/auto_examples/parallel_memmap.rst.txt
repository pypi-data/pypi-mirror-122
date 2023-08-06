

.. _sphx_glr_auto_examples_parallel_memmap.py:


===============================
NumPy memmap in joblib.Parallel
===============================

This example illustrates some features enabled by using a memory map
(:class:`numpy.memmap`) within :class:`joblib.Parallel`. First, we show that
dumping a huge data array ahead of passing it to :class:`joblib.Parallel`
speeds up computation. Then, we show the possibility to provide write access to
original data.



Speed up processing of a large data array
#############################################################################

 We create a large data array for which the average is computed for several
 slices.



.. code-block:: python


    import numpy as np

    data = np.random.random((int(1e7),))
    window_size = int(5e5)
    slices = [slice(start, start + window_size)
              for start in range(0, data.size - window_size, int(1e5))]







The ``slow_mean`` function introduces a :func:`time.sleep` call to simulate a
more expensive computation cost for which parallel computing is beneficial.
Parallel may not be beneficial for very fast operation, due to extra overhead
(workers creations, communication, etc.).



.. code-block:: python


    import time


    def slow_mean(data, sl):
        """Simulate a time consuming processing."""
        time.sleep(0.01)
        return data[sl].mean()








First, we will evaluate the sequential computing on our problem.



.. code-block:: python


    tic = time.time()
    results = [slow_mean(data, sl) for sl in slices]
    toc = time.time()
    print('\nElapsed time computing the average of couple of slices {:.2f} s'
          .format(toc - tic))





.. rst-class:: sphx-glr-script-out

 Out::

    Elapsed time computing the average of couple of slices 1.03 s


:class:`joblib.Parallel` is used to compute in parallel the average of all
slices using 2 workers.



.. code-block:: python


    from joblib import Parallel, delayed


    tic = time.time()
    results = Parallel(n_jobs=2)(delayed(slow_mean)(data, sl) for sl in slices)
    toc = time.time()
    print('\nElapsed time computing the average of couple of slices {:.2f} s'
          .format(toc - tic))





.. rst-class:: sphx-glr-script-out

 Out::

    Elapsed time computing the average of couple of slices 0.86 s


Parallel processing is already faster than the sequential processing. It is
also possible to remove a bit of overhead by dumping the ``data`` array to a
memmap and pass the memmap to :class:`joblib.Parallel`.



.. code-block:: python


    import os
    from joblib import dump, load

    folder = './joblib_memmap'
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass

    data_filename_memmap = os.path.join(folder, 'data_memmap')
    dump(data, data_filename_memmap)
    data = load(data_filename_memmap, mmap_mode='r')

    tic = time.time()
    results = Parallel(n_jobs=2)(delayed(slow_mean)(data, sl) for sl in slices)
    toc = time.time()
    print('\nElapsed time computing the average of couple of slices {:.2f} s\n'
          .format(toc - tic))





.. rst-class:: sphx-glr-script-out

 Out::

    Elapsed time computing the average of couple of slices 0.69 s


Therefore, dumping large ``data`` array ahead of calling
:class:`joblib.Parallel` can speed up the processing by removing some
overhead.


Writable memmap for shared memory :class:`joblib.Parallel`
##############################################################################

 ``slow_mean_write_output`` will compute the mean for some given slices as in
 the previous example. However, the resulting mean will be directly written on
 the output array.



.. code-block:: python



    def slow_mean_write_output(data, sl, output, idx):
        """Simulate a time consuming processing."""
        time.sleep(0.005)
        res_ = data[sl].mean()
        print("[Worker %d] Mean for slice %d is %f" % (os.getpid(), idx, res_))
        output[idx] = res_








Prepare the folder where the memmap will be dumped.



.. code-block:: python


    output_filename_memmap = os.path.join(folder, 'output_memmap')







Pre-allocate a writable shared memory map as a container for the results of
the parallel computation.



.. code-block:: python


    output = np.memmap(output_filename_memmap, dtype=data.dtype,
                       shape=len(slices), mode='w+')







``data`` is replaced by its memory mapped version. Note that the buffer as
already been dumped in the previous section.



.. code-block:: python


    data = load(data_filename_memmap, mmap_mode='r')







Fork the worker processes to perform computation concurrently



.. code-block:: python


    Parallel(n_jobs=2)(delayed(slow_mean_write_output)(data, sl, output, idx)
                       for idx, sl in enumerate(slices))







Compare the results from the output buffer with the expected results



.. code-block:: python


    print("\nExpected means computed in the parent process:\n {}"
          .format(np.array(results)))
    print("\nActual means computed by the worker processes:\n {}"
          .format(output))





.. rst-class:: sphx-glr-script-out

 Out::

    Expected means computed in the parent process:
     [ 0.50010533  0.50002398  0.49950524  0.50015061  0.50002933  0.49989966
      0.49978892  0.49958872  0.49909721  0.49913467  0.4992835   0.49935351
      0.49981403  0.49997001  0.49988522  0.49991579  0.49972933  0.49924144
      0.49917908  0.49914755  0.49916882  0.49933635  0.49986397  0.50000391
      0.50006188  0.500146    0.5000887   0.49990336  0.49989457  0.50010151
      0.49980707  0.50020054  0.50036211  0.50015808  0.5000748   0.50043913
      0.50060394  0.50021738  0.50014315  0.49992611  0.49980787  0.4993734
      0.49965423  0.49958403  0.50004792  0.49950331  0.4993449   0.49907318
      0.49883915  0.49860399  0.49934747  0.49955007  0.4993136   0.49966861
      0.49949513  0.49914998  0.49894131  0.49946034  0.49970671  0.5000256
      0.50027029  0.50073433  0.50064927  0.50052123  0.50046062  0.500303
      0.49967301  0.49965423  0.49993784  0.49977079  0.50011973  0.50037111
      0.50010885  0.50015505  0.50003335  0.50003072  0.50010419  0.50038757
      0.49991109  0.50006162  0.49947948  0.49945476  0.49930417  0.49960099
      0.49923874  0.49977268  0.49959364  0.49957331  0.49915307  0.49959267
      0.49922498  0.49916978  0.49931598  0.49975446  0.49944583]

    Actual means computed by the worker processes:
     [ 0.50010533  0.50002398  0.49950524  0.50015061  0.50002933  0.49989966
      0.49978892  0.49958872  0.49909721  0.49913467  0.4992835   0.49935351
      0.49981403  0.49997001  0.49988522  0.49991579  0.49972933  0.49924144
      0.49917908  0.49914755  0.49916882  0.49933635  0.49986397  0.50000391
      0.50006188  0.500146    0.5000887   0.49990336  0.49989457  0.50010151
      0.49980707  0.50020054  0.50036211  0.50015808  0.5000748   0.50043913
      0.50060394  0.50021738  0.50014315  0.49992611  0.49980787  0.4993734
      0.49965423  0.49958403  0.50004792  0.49950331  0.4993449   0.49907318
      0.49883915  0.49860399  0.49934747  0.49955007  0.4993136   0.49966861
      0.49949513  0.49914998  0.49894131  0.49946034  0.49970671  0.5000256
      0.50027029  0.50073433  0.50064927  0.50052123  0.50046062  0.500303
      0.49967301  0.49965423  0.49993784  0.49977079  0.50011973  0.50037111
      0.50010885  0.50015505  0.50003335  0.50003072  0.50010419  0.50038757
      0.49991109  0.50006162  0.49947948  0.49945476  0.49930417  0.49960099
      0.49923874  0.49977268  0.49959364  0.49957331  0.49915307  0.49959267
      0.49922498  0.49916978  0.49931598  0.49975446  0.49944583]


Clean-up the memmap
##############################################################################

 Remove the different memmap that we created. It might fail in Windows due
 to file permissions.



.. code-block:: python


    import shutil

    try:
        shutil.rmtree(folder)
    except:  # noqa
        print('Could not clean-up automatically.')






**Total running time of the script:** ( 0 minutes  3.192 seconds)



.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: parallel_memmap.py <parallel_memmap.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: parallel_memmap.ipynb <parallel_memmap.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.readthedocs.io>`_
