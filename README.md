# Misión Ñandú

App de práctica matemática para la **Olimpíada Ñandú** (certamen argentino de
matemática para nivel primario), empaquetada como **un único HTML portable**.

El alumno entrena por módulos (patrones, lógica, geometría, conteo,
divisibilidad, "encuentra el error" y olímpico), gana XP que hace evolucionar a
una mascota Ñandú, y puede simular las 5 instancias oficiales del certamen en el
**Modo Competencia** (con contrarreloj opcional y corrección al final de cada
etapa, como en el certamen real). Los problemas fallados quedan en una cola de
**Revancha** para reintentarlos, y el **Panel del Entrenador** muestra precisión
por módulo, racha diaria y qué conviene practicar. El progreso se guarda en
`localStorage`.

Las decisiones didácticas (doble intento, pistas con costo, feedback diferido
en competencia, etc.) están explicadas en [`PEDAGOGIA.md`](PEDAGOGIA.md).

## Estructura

| Archivo | Rol |
|---------|-----|
| `generate_problems.py` | Genera el banco de problemas → `problemas_nandu.json` |
| `test_banco.py` | Verifica el banco: recalcula cada respuesta desde el enunciado |
| `build_html.py` | Embebe el banco en la plantilla → `mision_nandu.html` |
| `problemas_nandu.json` | Banco de problemas (artefacto versionado) |
| `mision_nandu.html` | **Producto final** — abrir en cualquier navegador |
| `index.html` | Landing page del sitio público |
| `PEDAGOGIA.md` | Decisiones de diseño didáctico/pedagógico |
| `pedagogia.html` | Versión web de `PEDAGOGIA.md` (linkeada desde la landing) |
| `plan-de-mejora.md` | Hoja de ruta de mejoras |

## Cómo regenerar

```bash
python3 generate_problems.py   # crea problemas_nandu.json
python3 test_banco.py          # verifica el banco (no commitear si falla)
python3 build_html.py          # crea mision_nandu.html
```

> `generate_problems.py` usa una **semilla fija**: la misma corrida produce
> exactamente el mismo banco (reproducible y diffeable). Para publicar un banco
> distinto hay que cambiar la semilla en el script y regenerar.
>
> ⚠️ Regenerar con otra semilla cambia los `id` de los problemas: el progreso
> guardado en `localStorage` (en particular la cola de Revancha) puede quedar
> apuntando a problemas distintos.

## Jugar online

🎮 **https://pablosartorio.github.io/nandu/**

Abre la landing y, con el botón "Jugar", entra al juego. No hay que descargar ni
instalar nada — ideal para compartir con quien quiera practicar.

(También se puede ir directo al juego: `…/nandu/mision_nandu.html`.)

## Uso local

Abrir `mision_nandu.html` en el navegador. No necesita servidor ni dependencias.

## Flujo de trabajo

- `main`: versión estable. **Es lo que sirve GitHub Pages** (rama `main`, raíz).
- `develop`: rama de trabajo.

> ⚠️ El sitio online se publica desde `main`. Los cambios hechos en `develop`
> **no se ven en la web** hasta llevarlos a `main`:
>
> ```bash
> git switch main
> git merge develop
> git push origin main      # GitHub Pages re-despliega solo en ~1-2 min
> git switch develop        # volver a trabajar
> ```
