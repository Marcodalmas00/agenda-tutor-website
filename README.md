# Agenda Tutor — sito pubblico

Risorse per la beta privata dell’app iPhone Agenda Tutor. Questo repository contiene soltanto il sito pubblico; il codice dell’app è conservato separatamente in un repository privato.

- [Informazioni](https://marcodalmas00.github.io/agenda-tutor-website/)
- [Privacy](https://marcodalmas00.github.io/agenda-tutor-website/privacy/)
- [Assistenza](https://marcodalmas00.github.io/agenda-tutor-website/supporto/)
- [English](https://marcodalmas00.github.io/agenda-tutor-website/en/)

Contatto: [dev@marcodalmas00.com](mailto:dev@marcodalmas00.com).

## Modificare e visualizzare

I testi italiani e inglesi sono in `content.json`. Il generatore usa soltanto la libreria standard di Python 3 e produce pagine HTML statiche in `docs/`:

```sh
python3 scripts/build.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory docs
```

Aprire `http://127.0.0.1:8765/`. Gli stili e le icone sono in `docs/assets/`. Il sito segue il tema chiaro/scuro del sistema, non carica script, font esterni, analytics o pubblicità.

GitHub Pages pubblica il branch `main`, cartella `/docs`. Dopo una modifica ai testi, rigenerare e includere anche i file HTML nel commit. Le informazioni sulla privacy devono restare coerenti con i flussi effettivi dell’app e dell’assistenza.

## Ambito

La beta è disponibile su invito TestFlight. Le prenotazioni web e un’eventuale presentazione commerciale completa appartengono a una fase successiva; questo sito non le implementa.
