# Google Antigravity

Setup guidance for Antigravity. Host execution is not verified here.
See also the [Antigravity Guide](../antigravity-guide.md) for why skills are not
discovered out-of-the-box and how progressive disclosure works.

## Option A: One-Touch Setup Script (Recommended)

Automatically link skills to Antigravity's discovery path (`.agents/skills/`) or
machine-global path (`~/.gemini/config/skills/`):

```powershell
# Windows (PowerShell): Setup for current workspace
.\scripts\setup-antigravity.ps1 -Target workspace

# Or install globally for all Antigravity projects
.\scripts\setup-antigravity.ps1 -Target global
```

```bash
# macOS / Linux (Bash): Setup for current workspace
bash scripts/setup-antigravity.sh workspace

# Or install globally
bash scripts/setup-antigravity.sh global
```

## Option B: Marketplace Catalog or UI

- Go to **Customizations** > **Marketplace** in Antigravity IDE.
- Search for `dev-team-skills` and click **[Install]**.
- Or use the one-click card in chat:
  ```markdown
  <plugin-card catalog-id="dev-team-skills"></plugin-card>
  ```

## Option C: Global Plugins Directory

```bash
# Windows (PowerShell) & macOS/Linux (Bash)
git clone https://github.com/DongJinNam/dev-team-skills.git ~/.gemini/config/plugins/dev-team-skills
```

## Option D: Workspace Plugin

- Clone into `.agents/plugins/dev-team-skills` in your project root, or declare it in
  `.agents/plugins.json` to share with your team via Git.
