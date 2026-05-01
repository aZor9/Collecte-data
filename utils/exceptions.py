"""Exceptions metier du pipeline."""


class SiteBlockedError(RuntimeError):
    """Le site cible a bloque la requete (anti-bot / WAF)."""
