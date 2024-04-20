# EUSolver for Nix

This repository contains a fork of the original [EUSolver][eusolver] with a [Nix](https://nixos.org/nix/) derivation.

Supported platforms for this Nix derivation include:
- `x86_64-linux`
- `aarch64-linux`
- `x86_64-darwin`
- `aarch64-darwin`

## Getting Started

### Prerequisites

To use this fork of EUSolver, make sure you have Nix installed on your system. If not, follow the instructions provided in the [Nix installation guide][nix].\

### Building EUSolver

To build EUSolver using Nix, execute the following command:

```shell
nix build .
```

This will generate the executable in the `./result/bin/` directory.

### Running EUSolver

After building, you can run EUSolver directly by specifying the path to a benchmark file. For example,

```shell
./result/bin/eusolver benchmarks/max/max_2.sl
```

This command should output the synthesized function similar to the following:

```lisp
(define-fun max2 ((a0 Int) (a1 Int)) Int
     (ite (>= a0 a1) a0 a1))
```

### Combining Build and Run

Alternatively, you can use `nix run` to build and immediately execute EUSolver with the desired benchmark:

```shell
nix run . -- benchmarks/max/max_2.sl
```

[eusolver]: https://bitbucket.org/abhishekudupa/eusolver/
[nix]: https://zero-to-nix.com/start/install