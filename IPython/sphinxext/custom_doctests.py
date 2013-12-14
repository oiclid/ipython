"""
Module containing custom doctests.

"""

def str_to_array(s):
    """
    Simplistic converter of strings from repr to float NumPy arrays.

    If the repr representation has ellipsis in it, then this will fail.

    Parameters
    ----------
    s : str
        The repr version of a NumPy array.

    Examples
    --------
    >>> s = "array([ 0.3,  inf,  nan])"
    >>> a = str_to_array(s)

    """
    import numpy as np

    # Need to make sure eval() knows about inf and nan.
    # This also assumes default printoptions for NumPy.
    from numpy import inf, nan

    if s.startswith(u'array'):
        # Remove array( and )
        s = s[6:-1]

    if s.startswith(u'['):
        a = np.array(eval(s), dtype=float)
    else:
        # Assume its a regular float. Force 1D so we can index into it.
        a = np.atleast_1d(float(s))
    return a

def float_doctest(sphinx_shell, args, input_lines, found, submitted):
    """
    Doctest which allow the submitted output to vary slightly from the input.

    Here is how it might appear in an rst file:

    .. code-block:: rst

       .. ipython::

          @doctest float
          In [1]: 0.1 + 0.2
          Out[1]: 0.3

    """
    import numpy as np

    if len(args) == 2:
        rtol = 1e-05
        atol = 1e-08
    else:
        # Both must be specified if any are specified.
        try:
            rtol = float(args[2])
            atol = float(args[3])
        except IndexError:
            e = ("Both `rtol` and `atol` must be specified "
                 "if either are specified: {0}".format(args))
            raise IndexError(e)

    try:
        submitted = str_to_array(submitted)
        found = str_to_array(found)
    except:
        # For example, if the array is huge and there are ellipsis in it.
        error = True
    else:
        found_isnan = np.isnan(found)
        submitted_isnan = np.isnan(submitted)
        error = not np.allclose(found_isnan, submitted_isnan)
        error |= not np.allclose(found[~found_isnan],
                                 submitted[~submitted_isnan],
                                 rtol=rtol, atol=atol)

    if error:
        e = ('doctest float comparison failure for input_lines={0} with '
             'found_output={1} and submitted '
             'output="{2}"'.format(input_lines, repr(found), repr(submitted)) )
        raise RuntimeError(e)

doctests = {
    'float': float_doctest,
}
