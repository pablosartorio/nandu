# Misión Ñandú

App de práctica matemática para la **Olimpíada Ñandú** (certamen argentino de
matemática para nivel primario), empaquetada como **un único HTML portable**.

El alumno entrena por módulos (patrones, lógica, geometría, conteo,
divisibilidad, "encuentra el error" y olímpico), gana XP que hace evolucionar a
una mascota Ñandú, y puede simular las 5 instancias oficiales del certamen en el
**Modo Competencia**. El progreso se guarda en `localStorage`.

## Estructura

| Archivo | Rol |
|---------|-----|
| `generate_problems.py` | Genera el banco de problemas → `problemas_nandu.json` |
| `build_html.py` | Embebe el banco en la plantilla → `mision_nandu.html` |
| `problemas_nandu.json` | Banco de problemas (artefacto versionado) |
| `mision_nandu.html` | **Producto final** — abrir en cualquier navegador |
| `plan-de-mejora.md` | Hoja de ruta de mejoras |

## Cómo regenerar

```bash
python3 generate_problems.py   # crea problemas_nandu.json
python3 build_html.py          # crea mision_nandu.html
```

> `generate_problems.py` usa `random` sin semilla: cada corrida produce un banco
> distinto. Por eso `problemas_nandu.json` y `mision_nandu.html` se versionan,
> para fijar una versión estable.

## Uso

Abrir `mision_nandu.html` en el navegador. No necesita servidor ni dependencias.

## Flujo de trabajo

- `main`: versión estable.
- `develop`: rama de trabajo.
