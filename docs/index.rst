




Sijuiacion Language
===========================================

.. |fig| image:: http://raw.githubusercontent.com/thautwarm/static-resources/master/sijuiacion/sij.png



.. table::
   :align: center
   :widths: auto

   +--------------------------------------+--------------------------+
   |**An IR on Python VM**                | .. toctree::             |
   ||fig|                                 |                          |
   |                                      |                          |
   |                                      |    get-started.md        |
   |                                      |    instructions.md       |
   |                                      |                          |
   |                                      |                          |
   |                                      |                          |
   |                                      |                          |
   |                                      |                          |
   |                                      |                          |
   |                                      |                          |
   +--------------------------------------+--------------------------+


Features of sijuiacion:

- No similar framework so far in the whole Python world, but needed for many compiler stuffs.
- Compiling to stand-alone :code:`.pyc` file.
- Providing **Label as Values**, indirect jump, switch instructions for advanced language constructs.
- Taking advantage of Python's error reporting mechanisms by providing metadata.
- Generalising Python constants other than only marshallable python objects, by link time processing.


There's an example for implementing the stackless coroutine in Python with sijuiacion: `stack-less.sij <https://github.com/RemuLang/sijuiacion-lang/blob/master/test/sij-scripts/stack-less.sij>`_ ,
by using indirect jumps and Label As Value.
