# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2024-12-27

### Added

- Initial release of VlaamsCodex toolchain
- Platskript-to-Python transpiler (`compiler.py`)
- Custom source encoding codec `vlaamsplats` (`codec.py`)
- CLI with `run`, `build`, and `show-python` commands (`cli.py`)
- Magic mode: execute `.plats` files directly with `python script.plats`
- Automatic codec registration via `.pth` startup hook
- Custom PEP 517 build backend for wheel packaging
- Example program: `examples/hello.plats`
- Comprehensive documentation in `docs/`
- Test suite with compiler and magic mode tests

### Language Features (v0.1)

- Program blocks: `plan doe ... gedaan`
- Statement terminator: `amen`
- Variable assignment: `zet <var> op <expr> amen`
- Print statement: `klap <expr> amen`
- Function definition: `maak funksie <name> met <params> doe ... gedaan`
- Function call: `roep <name> met <args> amen`
- Return statement: `geeftterug <expr> amen`
- String literals: `tekst <words>`
- Numeric literals: `getal <n>`
- Variable reference: `da <name>`
- Space literal: `spatie`
- Operators: `plakt`, `derbij`, `deraf`, `keer`, `gedeeld`, `isgelijk`, `isniegelijk`, `isgroterdan`, `iskleinerdan`, `enook`, `ofwel`, `nie`

[Unreleased]: https://github.com/vlaamscodex/vlaamscodex/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/vlaamscodex/vlaamscodex/releases/tag/v0.1.0
