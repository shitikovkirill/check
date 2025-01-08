{ pkgs ? import <nixpkgs> { } }:

let
  sources = import ./nix/sources.nix;
  overrides = sources.poetry2nix.overrides.withDefaults (import ./nix/overrides.nix {
    pkgs = pkgs;
    lib = pkgs.lib;
  });
in sources.poetry2nix.mkPoetryApplication {
  python = pkgs.python312;
  src = pkgs.lib.cleanSource ./.;
  pyproject = ./pyproject.toml;
  poetrylock = ./poetry.lock;
  overrides = overrides;
}
