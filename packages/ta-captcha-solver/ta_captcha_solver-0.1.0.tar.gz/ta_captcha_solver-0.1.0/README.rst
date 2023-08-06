==================
ta-captcha-solver
==================


.. image:: https://img.shields.io/pypi/v/ta_captcha_solver.svg
        :target: https://pypi.python.org/pypi/ta_captcha_solver

.. image:: https://img.shields.io/travis/macejiko/ta_captcha_solver.svg
        :target: https://travis-ci.com/macejiko/ta_captcha_solver

.. image:: https://readthedocs.org/projects/ta-captcha/badge/?version=latest
        :target: https://ta-captcha.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

|

Thoughtful Automation Captcha Solver

|

Installation
------------

::

   python3 -m virtualenv venv
   source venv/bin/activate
   pip install ta-captcha-solver

|

Example Usage
-------------

.. code:: python

   captcha = TACaptchaSolver.get(
       captcha_type="v2",
       browser=self.browser,
       captcha_guru_api_key=self.captcha_guru_api_key,
   )
  captcha.solve()

|

Development
-----------

**Prepare local dev env:**

::

   python3 -m virtualenv venv
   source venv/bin/activate
   pip install -r requirements.txt

**Testing:**

::

   CAPTCHA_GURU_API_KEY=XXX pytest

**Push new package version:**

::

  bump2version minor
  git push origin YOUR_BRANCH



