from text_sensitivity.sensitivity import compare_accuracy, compare_precision, compare_recall
from text_sensitivity.perturbation import Perturbation, OneToOnePerturbation, OneToManyPerturbation
from text_sensitivity.data.random.string import (RandomString, RandomAscii, RandomDigits, RandomEmojis,
                                                 RandomLower, RandomPunctuation, RandomSpaces, RandomUpper,
                                                 RandomWhitespace, RandomCyrillic, combine_generators)
from text_sensitivity.data.random.entity import (RandomAddress, RandomCity, RandomCountry,
                                                 RandomFirstName, RandomLastName, RandomName,
                                                 RandomEmail, RandomPhoneNumber, RandomPriceTag,
                                                 RandomYear, RandomMonth, RandomDay, RandomDayOfWeek,
                                                 RandomCurrencySymbol, RandomCryptoCurrency)

__version__ = '0.1.10'
