# Ejercicio 1: introducir y remediar una dependencia vulnerable

Requisitos: el job `dependency-check` ya está en `main` y funcionando.

## 1. Crear la rama

```bash
git checkout main
git pull
git checkout -b lab/dependencia-vulnerable
```

## 2. Agregar la dependencia vulnerable

Dentro de `<dependencies>` del `pom.xml`:

```xml
<dependency>
  <groupId>org.apache.commons</groupId>
  <artifactId>commons-text</artifactId>
  <version>1.9</version>
</dependency>
```

CVE esperado: `CVE-2022-42889` (*Text4Shell*), CVSS 3.1 **9.8 Critical**, versiones 1.5 a 1.9 (corregido en 1.10.0).
La NVD puede reclasificar o agregar CVE con el tiempo: compáralo con tu reporte.

## 3. Probar en el Codespace

```bash
./scripts/run-sca.sh        # equivale a ./mvnw -B dependency-check:check
```

Debe terminar en `BUILD FAILURE` mencionando el umbral CVSS 7 y `CVE-2022-42889`.
Abre el HTML (`./scripts/serve-report.sh`) y localiza `commons-text-1.9.jar`: revisa su CPE, su evidencia y el CVE.
Observa también `commons-lang3` (transitiva): su versión la impone Spring Boot.

## 4. Pull request (contra TU fork)

```bash
git add pom.xml
git commit -m "feat: add commons-text"
git push origin lab/dependencia-vulnerable
```

Compare & pull request → cambia el repositorio base a `TU_USUARIO_GITHUB/spring-petclinic`, rama `main`
(un PR hacia `spring-projects/spring-petclinic` no recibe tus secretos).

## 5. Observar

- Checks del PR: `dependency-check` en rojo, `sonarqube` en verde.
- Log del paso **Run OWASP Dependency-Check**: mensaje del umbral.
- Los pasos de subida se ejecutan pese al fallo (`if: always()`).
- **Security > Code scanning** (filtra por la rama) y **Summary > Artifacts** (HTML).

## 6. Remediar

Cambia la versión a `1.15.0`:

```xml
<dependency>
  <groupId>org.apache.commons</groupId>
  <artifactId>commons-text</artifactId>
  <version>1.15.0</version>
</dependency>
```

```bash
./scripts/run-sca.sh        # debe terminar en BUILD SUCCESS
git add pom.xml
git commit -m "fix: upgrade commons-text to 1.15.0 (CVE-2022-42889)"
git push origin lab/dependencia-vulnerable
```

El job pasa a verde y la alerta queda **Fixed** en la rama. **Cierra el PR sin hacer merge**: PetClinic no usa `commons-text`.
