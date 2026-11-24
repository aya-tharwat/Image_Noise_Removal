# WASLA (`وَصْلَة`) — Branch Naming Conventions

## 1. Branch Naming Patterns

Always use lowercase, kebab-case, and prefix with the track and ticket/capability ID:

| Type | Pattern | Examples |
| :--- | :--- | :--- |
| **Feature** | `feat/<track>/<id>-<description>` | `feat/backend/c1-tenant-filter`<br>`feat/web/c7-kanban-board`<br>`feat/mobile/c15-notifications-ui` |
| **Sub-Task** | `feat/<track>/sub-<id>-<description>` | `feat/backend/sub-12-dto-validation`<br>`feat/data/sub-04-kpi-sql-views` |
| **Bug Fix** | `fix/<track>/<id>-<description>` | `fix/web/rtl-table-overflow`<br>`fix/backend/auth-token-expiry` |
| **Refactoring** | `refactor/<track>/<description>` | `refactor/ai/vector-indexer-modularization` |
| **Contracts** | `contract/<scope>-<description>` | `contract/openapi-projects-v1`<br>`contract/events-kpi-catalog` |
| **Documentation** | `docs/<area>/<id>-<description>` | `docs/srs/03-rbac-permission-matrix`<br>`docs/adr/adr-006-web-framework` |

> Documentation-only changes follow the [WASLA Documentation Standards (`WASLA-DS-001`)](../standards/documentation-standards.md). Code changes that affect documented behavior update the docs in the **same** branch — do not open a separate `docs/...` branch for them.

---