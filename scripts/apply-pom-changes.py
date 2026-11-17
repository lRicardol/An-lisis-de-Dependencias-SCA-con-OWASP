#!/usr/bin/env python3
"""Agrega el plugin dependency-check-maven al pom.xml de tu fork de spring-petclinic.

Uso:
    python3 scripts/apply-pom-changes.py                      # plugin base (sección 3)
    python3 scripts/apply-pom-changes.py --with-suppression   # plugin + suppressionFiles (sección 6)
    python3 scripts/apply-pom-changes.py --pom ruta/pom.xml

Es idempotente: si el plugin ya existe no lo duplica. No toca tus propiedades de
SonarQube ni ninguna otra parte del pom.xml. Crea pom.xml.bak antes de modificar.
"""
import argparse
import re
import shutil
import sys
import xml.dom.minidom

PLUGIN_BASE = """      <plugin>
        <groupId>org.owasp</groupId>
        <artifactId>dependency-check-maven</artifactId>
        <version>13.0.0</version>
        <configuration>
          <!-- Nombre de la variable de entorno con la key (no la key) -->
          <nvdApiKeyEnvironmentVariable>NVD_API_KEY</nvdApiKeyEnvironmentVariable>
          <!-- Base de datos fuera de ~/.m2 para cachearla por separado -->
          <dataDirectory>${user.home}/.dependency-check-data</dataDirectory>
          <formats>
            <format>HTML</format>
            <format>SARIF</format>
          </formats>
          <!-- Falla con cualquier vulnerabilidad High o Critical -->
          <failBuildOnCVSS>7</failBuildOnCVSS>
          <!-- OSS Index exige cuenta en Sonatype; se desactiva -->
          <ossIndexAnalyzerEnabled>false</ossIndexAnalyzerEnabled>
%(suppression)s        </configuration>
      </plugin>
"""

SUPPRESSION = """          <suppressionFiles>
            <suppressionFile>${project.basedir}/dependency-check-suppression.xml</suppressionFile>
          </suppressionFiles>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pom", default="pom.xml")
    ap.add_argument("--with-suppression", action="store_true")
    args = ap.parse_args()

    with open(args.pom, encoding="utf-8") as f:
        text = f.read()

    nl = "\r\n" if "\r\n" in text else "\n"
    text = text.replace("\r\n", "\n")
    has_plugin = "<artifactId>dependency-check-maven</artifactId>" in text
    has_supp = "<suppressionFiles>" in text

    if has_plugin and (has_supp or not args.with_suppression):
        print("El plugin dependency-check-maven ya está en el pom.xml. Nada que hacer.")
        return 0

    shutil.copyfile(args.pom, args.pom + ".bak")

    if has_plugin:
        # Solo falta suppressionFiles: se inserta tras ossIndexAnalyzerEnabled.
        pattern = r"([ \t]*<ossIndexAnalyzerEnabled>[^<]*</ossIndexAnalyzerEnabled>\n)"
        if not re.search(pattern, text):
            print("No encontré <ossIndexAnalyzerEnabled>; agrega suppressionFiles a mano "
                  "(ver docs/pom-snippets/).", file=sys.stderr)
            return 1
        text = re.sub(pattern, lambda m: m.group(1) + SUPPRESSION, text, count=1)
        msg = "Se agregó suppressionFiles al plugin existente."
    else:
        # Primer </plugins> a 4 espacios que sigue a '  <build>' (build principal, no profiles).
        m = re.search(r"^  <build>\n(?:.*\n)*?^    </plugins>\n", text, flags=re.M)
        if not m:
            print("No encontré <build><plugins> en el pom.xml.", file=sys.stderr)
            return 1
        end = m.end() - len("    </plugins>\n")
        block = PLUGIN_BASE % {"suppression": SUPPRESSION if args.with_suppression else ""}
        text = text[:end] + block + text[end:]
        msg = "Plugin dependency-check-maven agregado a <build><plugins>."

    xml.dom.minidom.parseString(text.encode("utf-8"))  # valida que siga bien formado
    with open(args.pom, "w", encoding="utf-8", newline="") as f:
        f.write(text.replace("\n", nl))
    print(msg + " Copia de seguridad: " + args.pom + ".bak")
    return 0


if __name__ == "__main__":
    sys.exit(main())
