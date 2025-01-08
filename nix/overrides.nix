{ pkgs ? import <nixpkgs> { }, lib ? pkgs.lib, stdenv ? pkgs.stdenv }:

self: super: {
  watchfiles = super.watchfiles.override { preferWheel = false; };
  aioauth-client = super.aioauth-client.overridePythonAttrs
    (old: { buildInputs = (old.buildInputs or [ ]) ++ [ super.poetry-core ]; });
}
