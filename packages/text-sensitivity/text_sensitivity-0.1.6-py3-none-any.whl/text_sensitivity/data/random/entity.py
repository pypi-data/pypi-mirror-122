from typing import Union, List, Tuple, Dict
import numpy as np

from faker.factory import Factory
from faker.generator import Generator

from instancelib.instances.text import TextInstanceProvider
from instancelib.labels.memory import MemoryLabelProvider

from text_explainability.default import Readable

from text_sensitivity.data.random.base import SeedMixin
from text_sensitivity.internationalization import get_locale, LOCALE_MAP


class RandomEntity(Readable, SeedMixin):
    def __init__(self,
                 languages: Union[str, List[str]] = get_locale(),
                 providers: List[str] = ['person'],
                 fn_name: Union[str, List[str]] = 'name',
                 sep: str = '\n',
                 seed: int = 0):
        """Base class to generate entity data for (a) given language(s).

        Args:
            languages (Union[str, List[str]], optional): .... Defaults to your current locale (see `get_locale()`).
            providers (List[str], optional): Providers from `faker` used in generation. Defaults to ['person'].
            fn_name (Union[str, List[str]], optional): Function name(s) to call for each generator. Defaults to 'name'.
            sep (str, optional): Separator to replace '\n' character with. Defaults to '\n'.
            seed (int, optional): Seed for reproducibility. Defaults to 0.
        """
        self.languages = [languages] if isinstance(languages, str) else languages
        self.providers = [f'faker.providers.{provider}' if not provider.startswith('faker.providers.') else provider
                          for provider in providers]
        self.generators = {lang: Factory.create(LOCALE_MAP[lang] if lang in LOCALE_MAP.keys() else lang,
                                                self.providers,
                                                Generator(),
                                                None)
                           for lang in self.languages}
        self.sep = sep
        self.fn_name = fn_name if isinstance(fn_name, list) else [fn_name]
        self._original_seed = self._seed = seed

    def generate_list(self,
                      n: int,
                      attributes: bool = False) -> Union[List[str], List[Tuple[str, Dict[str, str]]]]:
        """Generate n instances of random data and return as list. 

        Args:
            n (int): Number of instances to generate.
            attributes (bool, optional): Include attributes (language, which function was used, etc.) or not. 
                Defaults to False.

        Returns:
            List[str]: Generated instances (if attributes = False).
            List[Tuple[str, Dict[str, str]]]: Generated instances and corresponding attributes (if attributes = True).
        """
        np.random.seed(self._seed)
        self._seed += 1
        languages = np.random.choice(self.languages, size=n)
        fn_names = np.random.choice(self.fn_name, size=n)
        for generator in self.generators.values():
            generator.seed(self._seed)
        sentences = [eval(f'self.generators[lang].{fn}()').replace('\n', self.sep)
                     for fn, lang in zip(fn_names, languages)]
        if not attributes:
            return sentences
        attr = [{'language': lang} for lang in languages] if len(self.fn_name) == 1 \
            else [{'language': lang, 'fn': fn} for lang, fn in zip(languages, fn_names)]
        return list(zip(sentences, attr))

    def generate(self,
                 n: int,
                 attributes: bool = False
                 ) -> Union[TextInstanceProvider, Tuple[TextInstanceProvider, Dict[str, MemoryLabelProvider]]]:
        """Generate n instances of random data. 

        Args:
            n (int): Number of instances to generate.
            attributes (bool, optional): Include attributes (language, which function was used, etc.) or not. 
                Defaults to False.

        Returns:
            TextInstanceProvider: Provider containing generated instances (if attributes = False).
            Tuple[TextInstanceProvider, Dict[str, MemoryLabelProvider]]: Provider and corresponding attribute 
                labels (if attributes = True).
        """
        res = self.generate_list(n=n, attributes=attributes)
        values = [v for v, _ in res] if attributes else res         
        values = TextInstanceProvider.from_data(values)

        if attributes:
            # Group labels, and put all of them into labelproviders with the same keys as the instanceprovider
            labels = [l for _, l in res]
            labels = {key: MemoryLabelProvider.from_tuples(zip(list(values),
                                                               [frozenset({label[key]}) for label in labels]))
                      for key in labels[0].keys()}
            return values, labels
        return values


class RandomAddress(RandomEntity):
    def __init__(self,
                 languages: Union[str, List[str]] = get_locale(),
                 sep: str = '\n',
                 seed: int = 0):
        """Generate random cities in (a) given language(s)."""
        super().__init__(languages=languages,
                         providers=['address', 'person'],
                         fn_name='address',
                         sep=sep,
                         seed=seed)


class RandomCity(RandomEntity):
    def __init__(self,
                 languages: Union[str, List[str]] = get_locale(),
                 seed: int = 0):
        """Generate random cities in (a) given language(s)."""
        super().__init__(languages=languages,
                         providers=['address'],
                         fn_name='city',
                         seed=seed)


class RandomCountry(RandomEntity):
    def __init__(self,
                 languages: Union[str, List[str]] = get_locale(),
                 seed: int = 0):
        """Generate random countries for (a) given language(s)."""
        super().__init__(languages=languages,
                         providers=['address'],
                         fn_name='country',
                         seed=seed)


class RandomName(RandomEntity):
    def __init__(self,
                 languages: Union[str, List[str]] = get_locale(),
                 sex: List[str] = ['male', 'female'],
                 seed: int = 0):
        """Generate random full names for (a) given language(s)."""
        if isinstance(sex, str):
            sex = [sex]
        super().__init__(languages=languages,
                         providers=['person'],
                         fn_name=[f'name_{s}' for s in sex],
                         seed=seed)


class RandomFirstName(RandomEntity):
    def __init__(self,
                 languages: Union[str, List[str]] = get_locale(),
                 sex: List[str] = ['male', 'female'],
                 seed: int = 0):
        """Generate random first names for (a) given language(s)."""
        if isinstance(sex, str):
            sex = [sex]
        super().__init__(languages=languages,
                         providers=['person'],
                         fn_name=[f'first_name_{s}' for s in sex],
                         seed=seed)


class RandomLastName(RandomEntity):
    def __init__(self,
                 languages: Union[str, List[str]] = get_locale(),
                 seed: int = 0):
        """Generate random last names for (a) given language(s)."""
        super().__init__(languages=languages,
                         providers=['person'],
                         fn_name='last_name',
                         seed=seed)


class RandomEmail(RandomEntity):
    def __init__(self,
                 languages: Union[str, List[str]] = get_locale(),
                 seed: int = 0):
        """Generate random e-mail addresses for (a) given language(s)."""
        super().__init__(languages=languages,
                         providers=['person', 'company', 'internet'],
                         fn_name='email',
                         seed=seed)


class RandomPhoneNumber(RandomEntity):
    def __init__(self,
                 languages: Union[str, List[str]] = get_locale(),
                 seed: int = 0):
        """Generate random phone numbers for (a) given language(s) / country."""
        super().__init__(languages=languages,
                         providers=['phone_number'],
                         fn_name='phone_number',
                         seed=seed)


class RandomYear(RandomEntity):
    def __init__(self,
                 seed: int = 0):
        """Generate random year."""
        super().__init__(languages='en',
                         providers=['date_time'],
                         fn_name='day_of_week',
                         seed=seed)


class RandomMonth(RandomEntity):
    def __init__(self,
                 languages: Union[str, List[str]] = get_locale(),
                 seed: int = 0):
        """Generate random month name in (a) given language(s)."""
        super().__init__(languages=languages,
                         providers=['date_time'],
                         fn_name='month',
                         seed=seed)


class RandomDay(RandomEntity):
    def __init__(self,
                 seed: int = 0):
        """Generate random day of the month."""
        super().__init__(languages='en',
                         providers=['date_time'],
                         fn_name='day_of_month',
                         seed=seed)


class RandomDayOfWeek(RandomEntity):
    def __init__(self,
                 languages: Union[str, List[str]] = get_locale(),
                 seed: int = 0):
        """Generate random day of week in (a) given language(s)."""
        super().__init__(languages=languages,
                         providers=['date_time'],
                         fn_name='day_of_week',
                         seed=seed)


class RandomPriceTag(RandomEntity):
    def __init__(self,
                 languages: Union[str, List[str]] = get_locale(),
                 seed: int = 0):
        """Generate random pricetag names in (a) given languages' currency."""
        super().__init__(languages=languages,
                         providers=['currency'],
                         fn_name='pricetag',
                         seed=seed)


class RandomCurrencySymbol(RandomEntity):
    def __init__(self,
                 seed: int = 0):
        """Generate random currency symbols."""
        super().__init__(languages='en',
                         providers=['currency'],
                         fn_name='currency_symbol',
                         seed=seed)


class RandomCryptoCurrency(RandomEntity):
    def __init__(self,
                 seed: int = 0):
        """Generate random cryptocurrency names."""
        super().__init__(languages='en',
                         providers=['currency'],
                         fn_name='cryptocurrency_name',
                         seed=seed)
