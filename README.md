# Laboratorio SCA: OWASP Dependency-Check sobre Spring PetClinic

Este paquete es un **complemento** para tu fork público de `spring-petclinic` (el del laboratorio de
análisis estático con SonarQube Cloud). Agrega un segundo job al workflow que revisa las librerías de
terceros contra la NVD, publica los hallazgos en **Security > Code scanning** y falla con CVSS >= 7.

> No incluye el código de PetClinic: se copia **encima** de tu fork para no pisar tu `pom.xml`
> (tus `sonar.organization` / `sonar.projectKey`) ni nada de lo que ya tienes funcionando.

## Estructura

```
.
├── .github/workflows/sonarqube-analysis.yml   # jobs: sonarqube (igual que antes) + dependency-check (nuevo)
├── dependency-check-suppression.xml           # archivo de supresiones (vacío, válido)
├── scripts/
│   ├── apply-pom-changes.py                   # agrega el plugin al pom.xml (idempotente)
│   ├── verify-nvd-key.sh                      # comprueba NVD_API_KEY sin imprimirla
│   ├── update-nvd-db.sh                       # primera descarga de la NVD
│   ├── run-sca.sh                             # dependency-check:check
│   └── serve-report.sh                        # sirve el HTML en el puerto 8000
├── docs/
│   ├── pom-snippets/                          # bloques XML del plugin (base y con supresiones)
│   ├── ejercicios/                            # 01 dependencia vulnerable, 02 supresiones
│   └── problemas-frecuentes.md                # troubleshooting y preguntas de reflexión
└── README.md
```

## Requisitos

- Lab de análisis estático terminado (fork público, Java 21 en `devcontainer.json`, workflow de Sonar funcionando).
- Una API key de la NVD activada: <https://nvd.nist.gov/developers/request-an-api-key>.

## Pasos

### 1. Secretos (no se versionan)

- **Actions:** fork > Settings > Secrets and variables > Actions > New repository secret → `NVD_API_KEY`.
- **Codespaces:** tu perfil > Settings > Codespaces > Codespaces secrets → `NVD_API_KEY`, con acceso a
  `TU_USUARIO_GITHUB/spring-petclinic`. Si el Codespace estaba abierto: **Codespaces: Rebuild Container**.

### 2. Copiar los archivos al fork

Desde la raíz de tu fork (en el Codespace, sube el zip o copia su contenido):

```bash
unzip spring-petclinic-sca.zip -d /tmp/sca
cp -r /tmp/sca/spring-petclinic-sca/. .
```

Esto agrega/reemplaza `.github/workflows/sonarqube-analysis.yml`, `dependency-check-suppression.xml`,
`scripts/` y `docs/`. Si ya tienes una carpeta `scripts/` o `docs/` propia, revisa que no haya choques.

> El job `sonarqube` del workflow es idéntico al del laboratorio anterior. Si cambiaste versiones o pasos
> en el tuyo, conserva tus cambios en ese job.

### 3. Agregar el plugin al `pom.xml`

```bash
python3 scripts/apply-pom-changes.py
git diff pom.xml        # revisa el cambio (también queda pom.xml.bak)
rm pom.xml.bak
```

Si prefieres hacerlo a mano, copia `docs/pom-snippets/dependency-check-plugin.xml` dentro de
`<build><plugins>` (no dentro de `<profiles>`). **No agregues `<executions>`**: el plugin no debe correr en
`./mvnw verify`.

### 4. Verificar la key y descargar la base de la NVD

```bash
./scripts/verify-nvd-key.sh
./scripts/update-nvd-db.sh      # 10 a 30 min la primera vez; déjalo en una terminal aparte
```

### 5. Ejecutar el análisis y leer el reporte

```bash
./scripts/run-sca.sh            # genera target/dependency-check-report.html y .sarif
./scripts/serve-report.sh       # abre el puerto 8000 > dependency-check-report.html
```

Si termina en `BUILD FAILURE`, revisa el reporte: puede haber un hallazgo real (actualiza la dependencia)
o un falso positivo (ver `docs/ejercicios/02-falsos-positivos-y-supresiones.md`).

### 6. Publicar

```bash
git add .github/workflows/sonarqube-analysis.yml pom.xml dependency-check-suppression.xml scripts docs
git commit -m "ci: add OWASP Dependency-Check job"
git push origin main
```

En **Actions** deben aparecer dos jobs: `sonarqube` y `dependency-check`. La primera ejecución descarga la
NVD completa; las siguientes restauran la caché. Resultados en:

- **Security > Code scanning** (alertas de *dependency-check*).
- **Summary > Artifacts** → `dependency-check-report` (HTML).

> Si `main` ya falla por CVSS, revisa los hallazgos antes del ejercicio.

### 7. Ejercicios

1. `docs/ejercicios/01-dependencia-vulnerable.md`: agregar `commons-text` 1.9 (CVE-2022-42889), ver el fallo y remediar con 1.15.0.
2. `docs/ejercicios/02-falsos-positivos-y-supresiones.md`: activar el archivo de supresión
   (`python3 scripts/apply-pom-changes.py --with-suppression`) y suprimir con criterio.

## Notas de diseño

- **Job separado y en paralelo:** si Dependency-Check falla, Sonar sigue publicándose.
- **Permisos mínimos:** `security-events: write` solo en el job nuevo.
- **Caché de la NVD en dos pasos** (`restore` + `save` con `if: always()`): se guarda aunque el job falle por el umbral. Clave por día.
- **Subidas con `if: always()`:** el SARIF y el HTML se publican justo cuando el umbral rompe el build.
- **OSS Index desactivado:** evita depender de otra cuenta; el análisis queda limitado a la NVD (+ CISA KEV).
- **`dataDirectory` fuera de `~/.m2`:** la base no entra en la caché de Maven que comparte el job de Sonar.
- **La key nunca va en un archivo:** el `pom.xml` solo contiene el *nombre* de la variable (`NVD_API_KEY`).

## Valores a reemplazar

- `TU_USUARIO_GITHUB`: tu usuario de GitHub, dueño del fork (solo aparece en la documentación y en la plantilla de supresiones).
