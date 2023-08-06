"""Apply perturbation to one or multiple (tokenized) strings."""

from text_sensitivity.perturbation.base import Perturbation, OneToOnePerturbation, OneToManyPerturbation
from text_sensitivity.perturbation.characters import (add_typos, random_case_swap, random_lower,
                                                      random_spaces, random_upper, swap_random, delete_random)
# from text_sensitivity.perturbation.words import 
from text_sensitivity.perturbation.sentences import to_lower, to_upper, repeat_n_times
