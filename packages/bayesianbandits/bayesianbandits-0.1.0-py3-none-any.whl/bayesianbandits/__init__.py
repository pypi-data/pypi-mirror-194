"""
========================================
bayesianbandits (:mod:`bayesianbandits`)
========================================

.. currentmodule:: bayesianbandits

A Python library for Bayesian Multi-Armed Bandits.

This library implements a variety of multi-armed bandit algorithms, including
epsilon-greedy, Thompson sampling, and upper confidence bound. It also
handles a number of common problems in multi-armed bandit problems, including
contextual bandits, delayed reward, and restless bandits.

This library is designed to be easy to use and extend. It is built on top of
scikit-learn, and uses scikit-learn's estimators to model the arms. This
allows you to use any scikit-learn estimator that supports the `partial_fit`
and `sample` methods as an arm in a bandit. Restless bandits also require the
`decay` method.

This library is still under development, and the API is subject to change.

Arm Class
=========

The `Arm` class is the base class for all arms in a bandit. Its constructor
takes two arguments, `action_function` and `reward_function`, which represent
the action taken by the `pull` method of the arm and the mechanism for computing
the reward from the outcome of the action.

.. autosummary::
    :toctree: _autosummary

    Arm


Bandit Decorators
=================

These class decorators can be used to create bandit algorithms from classes
that define variables that implement the `Arm` protocol.

.. autosummary::
    :toctree: _autosummary

    bandit
    contextual
    delayed_reward
    restless

Policies
========

These functions can be used to create policy functions for bandits. They should
be passed to the `policy` argument of the `bandit` decorator.

.. autosummary::
    :toctree: _autosummary

    epsilon_greedy
    thompson_sampling
    upper_confidence_bound

Estimators
==========

These estimators are the underlying models for the arms in a bandit. They
should be passed to the `learner` argument of the `bandit` decorator.

.. autosummary::
    :toctree: _autosummary

    DirichletClassifier


"""


from ._bandit import Arm, bandit, contextual, delayed_reward, restless
from ._policy_decorators import (
    epsilon_greedy,
    thompson_sampling,
    upper_confidence_bound,
)
from ._estimators import DirichletClassifier
