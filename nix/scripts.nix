{ pkgs ? import <nixpkgs> { }, projectName ? "app" }:
let
  scriptPrefix = "${projectName}-";

  docScript = pkgs.writeShellScriptBin (scriptPrefix + "doc")
    "nix-build docs/ --out-link .docs";
  docRunScript = pkgs.writeShellScriptBin (scriptPrefix + "doc-wotch")
    "python -m http.server 8001 --directory .docs --bind 127.0.0.1";

  coverageRunScript = pkgs.writeShellScriptBin (scriptPrefix + "coverage-wotch")
    "python -m http.server 8002 --directory htmlcov/ --bind 127.0.0.1";

  styleScript = let
    styleNix = "find . -name '*.nix' -not -path '.direnv' -exec nixfmt {} \\;";
    styleOrder = "isort ./${projectName}/";
    stylePython =
      "black ${projectName} --exclude ${projectName}/migrations -l 79";
  in pkgs.writeShellScriptBin (scriptPrefix + "style")
  "${styleOrder} && ${stylePython} && ${styleNix}";

  mypyScript =
    pkgs.writeShellScriptBin (scriptPrefix + "mypy") "mypy ${projectName}";

  lintScript =
    pkgs.writeShellScriptBin (scriptPrefix + "lint") "flake8 ${projectName}";

  preCommitInit = pkgs.writeShellScriptBin (scriptPrefix + "pre-commit-init")
    "pre-commit install";
  preCommitChackAll = pkgs.writeShellScriptBin (scriptPrefix + "pre-commit")
    "pre-commit run --all-files";

  migrationsScript = pkgs.writeShellScriptBin (scriptPrefix + "migrations") ''
    alembic revision --autogenerate
  '';
  migrateScript = pkgs.writeShellScriptBin (scriptPrefix + "migrate") ''
    alembic upgrade head
  '';

  memoScript = pkgs.writeShellScriptBin (scriptPrefix + "memo") ''
    sqlite_web ./.pymon
  '';

in with pkgs.python312Packages;
with pkgs; [
  # Linting
  pkgs.nixfmt
  isort
  black
  styleScript

  mypy
  mypyScript

  flake8
  lintScript

  # Documantation
  docScript
  docRunScript

  coverageRunScript

  pkgs.pre-commit
  preCommitInit
  preCommitChackAll

  migrationsScript
  migrateScript

  sqlite-web
  memoScript

  action-validator
]
