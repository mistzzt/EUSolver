{
  description = "Application packaged using poetry2nix";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/release-23.11";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    systems = [
      "x86_64-linux"
      "aarch64-linux"
      "x86_64-darwin"
      "aarch64-darwin"
    ];

    forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f system);
  in {
    packages = forAllSystems (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      inherit (pkgs.stdenv) mkDerivation;
      inherit (pkgs) makeWrapper lib stdenv;

      python311 = pkgs.python311.withPackages (ps: with ps; [pyparsing z3]);
      disableLTO = stdenv.cc.isClang && stdenv.isDarwin; # workaround issue nixpkgs#19098
      libeusolver = mkDerivation {
        name = "libeusolver";
        version = "0.1.0";
        src = ./thirdparty/libeusolver;
        buildInputs = [pkgs.cmake pkgs.python3];
        installPhase = ''
          mkdir -p $out
          cp eusolver.py $out
          cp libeusolver.* $out
        '';
        NIX_CFLAGS_COMPILE = lib.optional disableLTO "-fno-lto";
      };
    in {
      libeusolver = libeusolver;
      eusolver = mkDerivation {
        name = "EUSolver";
        version = "0.1.0";
        src = ./.;

        buildInputs = [python311 libeusolver makeWrapper pkgs.cmake];
        dontUseCmakeConfigure = true;

        installPhase = ''
          mkdir -p $out/bin
          cp -r $src/src $out/src

          makeWrapper ${python311}/bin/python $out/bin/eusolver \
            --argv0 "eusolver" \
            --add-flags $out/src/benchmarks.py \
            --prefix PYTHONPATH : ${libeusolver}
        '';
      };
      default = self.packages.${system}.eusolver;
    });
  };
}
