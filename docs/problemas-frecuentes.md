# Problemas frecuentes

| Síntoma | Causa y solución |
|---|---|
| `NVD Returned Status Code: 403` | La key no llegó o no está activada. Revisa el secreto `NVD_API_KEY` (Actions y Codespaces) y el enlace de activación. En Codespaces, reconstruye el contenedor tras crear el secreto. |
| Descarga lenta o `429` / `503` | La NVD limita peticiones o está saturada. Reintenta más tarde (continúa donde quedó). Si persiste, agrega `<nvdApiDelay>8000</nvdApiDelay>` en la configuración del plugin. |
| Cada ejecución descarga la NVD completa | La caché está vacía o no se guarda. Verifica que **Save NVD database** corra y que **Restore NVD database** muestre `Cache restored`. Las cachés de un PR no se comparten con otros PR; la de `main` sí. |
| Errores raros de base de datos tras un fallo | Caché dañada: bórrala en **Actions > Caches** (las `Linux-nvd-`) y vuelve a ejecutar. |
| El SARIF no aparece en **Security** | Falta `security-events: write`, el paso se saltó por no existir el archivo, o el PR iba hacia el repositorio original. |
| `Resource not accessible by integration` | El job no tiene `security-events: write`. |
| Errores de **OSS Index** (`401`) | Confirma `<ossIndexAnalyzerEnabled>false</ossIndexAnalyzerEnabled>`. |
| `Unable to load suppression file` | Ruta incorrecta en `suppressionFiles` o XML mal formado. |
| El job de Sonar dejó de funcionar | El job `sonarqube` debe quedar idéntico al del laboratorio anterior. |
| `./mvnw verify` ejecuta Dependency-Check | Se agregó un `<executions>` al plugin. Quítalo: se invoca solo con `dependency-check:check`. |

## Preguntas de reflexión

1. ¿Qué umbral de `failBuildOnCVSS` usarías en un equipo real? ¿El mismo para desarrollo y para un release?
2. ¿Qué aporta Dependency-Check que Dependabot no, y viceversa?
3. Un CVE 9.8 en una librería que tu código nunca invoca, ¿es urgente? ¿Qué información necesitas?
4. ¿Quién debería aprobar cambios en `dependency-check-suppression.xml` y con qué controles?

## Reto opcional

- Activa **Dependabot alerts** y **Dependabot security updates** (Settings > Advanced Security) y compara con Dependency-Check.
- Protege `main` exigiendo el check `dependency-check` antes del merge.
