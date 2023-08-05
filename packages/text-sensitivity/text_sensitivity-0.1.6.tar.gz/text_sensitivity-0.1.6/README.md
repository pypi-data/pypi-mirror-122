<p align="center">
  <img src="https://i.ibb.co/2nzcC1P/Text-Logo-Logo-large-sensitivity.png" alt="T_xt Sensitivity logo" width="70%">
</p>

[![PyPI](https://img.shields.io/pypi/v/text_sensitivity)](https://pypi.org/project/text-sensitivity/)
[![Python_version](https://img.shields.io/badge/python-3.8%20%7C%203.9-blue)](https://pypi.org/project/text-sensitivity/)
[![Build_passing](https://img.shields.io/badge/build-passing-brightgreen)](https://git.science.uu.nl/m.j.robeer/text_sensitivity/-/pipelines)
[![License](https://img.shields.io/pypi/l/text_sensitivity)](https://www.gnu.org/licenses/lgpl-3.0.en.html)
[![Docs_passing](https://img.shields.io/badge/docs-external-blueviolet)](https://marcelrobeer.github.io/text_sensitivity)

---

_Extension of [text_explainability](https://git.science.uu.nl/m.j.robeer/text_explainability) for sensitivity testing (robustness, fairness)._

Marcel Robeer, 2021

## Installation
| Method | Instructions |
|--------|--------------|
| `pip` | Install from [PyPI](https://pypi.org/project/text-sensitivity/) via `pip3 install text_sensitivity`. |
| Local | Clone this repository and install via `pip3 install -e .` or locally run `python3 setup.py install`.

## Documentation
Full documentation of the latest version is provided at [https://marcelrobeer.github.io/text_sensitivity/](https://marcelrobeer.github.io/text_sensitivity/).

## Example usage
See [example_usage.md](example_usage.md) to see an example of how the package can be used, or run the lines in `example_usage.py` to do explore it interactively.

## Releases
`text_explainability` is officially released through [PyPI](https://pypi.org/project/text-sensitivity/).

See [CHANGELOG.md](CHANGELOG.md) for a full overview of the changes for each version.

## Citation
```
@misc{text_sensitivity,
  title = {Python package text_sensitivity},
  author = {Marcel Robeer and Elize Herrewijnen},
  howpublished = {https://git.science.uu.nl/m.j.robeer/text_sensitivity},
  year = {2021}
}
```

## Maintenance
### Contributors
- [Marcel Robeer](https://www.uu.nl/staff/MJRobeer) (`@m.j.robeer`)
- Elize Herrewijnen (`@e.herrewijnen`)

### Todo
Tasks yet to be done:

* Word-level perturbations
* Add fairness-specific metrics:
    - Subgroup fairness
    - Counterfactual fairness
* Tests
    - Add tests for data generation
    - Add tests for perturbations
    - Add tests for test-schemes
* Add visualization ability
