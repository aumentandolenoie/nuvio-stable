# Nuvio Stable — policy per le prossime GitHub Releases

Richiesta del 23 ottobre 2026 per le release FUTURE, non retroattiva.

- Titolo pubblico neutro: **Nuvio Stable <versione>**. Non usare il suffisso "LG webOS" nel titolo della release.
- Una release pubblica deve includere **entrambi** gli installabili verificati, per lo STESSO commit e la STESSA versione:
  - LG webOS: `space.nuvio.native.stable_<versione>_arm.ipk` (con gli indici Homebrew e gli hash già previsti).
  - Samsung Tizen 8/9: `Nuvio-<versione>-NuvioTpk.tpk`, installabile tramite Apps2Samsung (più checksum SHA-256).
- Prima di pubblicare verificare che entrambi i workflow, test, nomi/manifest, versioni, hash e artefatti siano corretti e coerenti. Nessuna pubblicazione parziale se il TPK manca o non è stato validato.
- Non sostituire o sovrascrivere gli asset delle release già pubblicate; preservare l'attuale canale Homebrew LG.
- Evitare la ricompilazione inutile e non introdurre regressioni nella variante LG.
- Questa nota NON autorizza a cambiare immediatamente o pubblicare automaticamente le release esistenti. Integrare la pipeline di pubblicazione con un handoff robusto degli artifact prima della prossima release.
