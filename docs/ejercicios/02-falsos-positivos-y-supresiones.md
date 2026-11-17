# Ejercicio 2: falsos positivos y supresiones

## 1. Activar el archivo de supresión

El archivo `dependency-check-suppression.xml` ya está en la raíz (sin supresiones activas).
Actívalo en el plugin:

```bash
python3 scripts/apply-pom-changes.py --with-suppression
```

(o copia el bloque de `docs/pom-snippets/dependency-check-plugin-con-supresiones.xml`).

## 2. Suprimir con criterio

1. Revisa el reporte de `main` y elige un hallazgo cuyo CPE no coincida con la evidencia del JAR.
2. Si no hay ninguno, practica con `CVE-2022-42889` en una rama nueva con `commons-text` 1.9, sabiendo que
   **no es un falso positivo**: el motivo es una aceptación temporal de riesgo.
3. Completa el archivo y ejecuta `./scripts/run-sca.sh`. El hallazgo debe aparecer en
   **Suppressed Vulnerabilities** del HTML y el build debe pasar.
4. Si usaste `commons-text`, **no hagas merge**: cierra el PR y borra la rama.

Ejemplo para `commons-text` (reemplaza los valores en mayúsculas):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<suppressions xmlns="https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.4.xsd">

  <!--
    Motivo: aceptación temporal de riesgo, no es falso positivo.
    Evidencia: el proyecto no invoca StringSubstitutor.createInterpolator()
    con entrada externa (búsqueda en el código: sin usos).
    Revisado por: TU_USUARIO_GITHUB
    Fecha de revisión: AAAA-MM-DD
  -->
  <suppress until="AAAA-MM-DDZ">
    <notes><![CDATA[
      Text4Shell: aceptado temporalmente; el proyecto no usa interpolación
      con entrada externa. Remediar actualizando a commons-text >= 1.10.0.
    ]]></notes>
    <packageUrl regex="true">^pkg:maven/org\.apache\.commons/commons-text@.*$</packageUrl>
    <vulnerabilityName>CVE-2022-42889</vulnerabilityName>
  </suppress>

</suppressions>
```

## Riesgos de suprimir sin criterio

- Una supresión oculta el hallazgo para siempre; una regla amplia también oculta CVE futuros.
- Un "falso positivo" puede no serlo: que hoy no uses la función vulnerable no significa que mañana nadie la use.
- Un build verde da falsa tranquilidad.
- Buenas prácticas: una supresión por CVE y dependencia, motivo y evidencia, fecha `until`, revisión en PR.
