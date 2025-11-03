# Folder Rename Instructions: AAgents → Agent-Cleo

## What Has Been Done

All file references have been updated:
- ✅ `app.py` - BASE_PATH updated to `Agent-Cleo`
- ✅ `README.md` - All folder paths updated
- ✅ `agent_utils.py` - Documentation comment updated
- ✅ `Coach-Cleo/Context/Files/Integration Summary.md` - File paths updated

## What You Need to Do

The actual folder needs to be renamed from outside this Claude Code session, as the folder is currently in use.

### Option 1: Manual Rename (Simplest)

1. **Close this Claude Code session**
2. **Open File Explorer**
3. **Navigate to**: `C:\Users\AndrewSmart\Claude_Projects\`
4. **Right-click** on the `AAgents` folder
5. **Select** "Rename"
6. **Type**: `Agent-Cleo`
7. **Press Enter**

### Option 2: Using Command Prompt

1. **Close this Claude Code session**
2. **Open Command Prompt** (cmd)
3. **Run these commands**:
   ```cmd
   cd C:\Users\AndrewSmart\Claude_Projects
   ren AAgents Agent-Cleo
   cd Agent-Cleo
   ```

### Option 3: Using PowerShell

1. **Close this Claude Code session**
2. **Open PowerShell**
3. **Run these commands**:
   ```powershell
   cd C:\Users\AndrewSmart\Claude_Projects
   Rename-Item -Path "AAgents" -NewName "Agent-Cleo"
   cd Agent-Cleo
   ```

## After Renaming

1. **Open Claude Code** in the new folder location:
   ```bash
   cd C:\Users\AndrewSmart\Claude_Projects\Agent-Cleo
   ```

2. **Verify the application still works**:
   ```bash
   python app.py
   ```

3. **Access the dashboard** at: `http://localhost:5000`

4. **Click "Initialize System"** to refresh agent paths

5. **Delete this instruction file** (it's no longer needed):
   ```bash
   del RENAME_INSTRUCTIONS.md
   ```

## Notes

- The git repository will remain intact during the rename
- All staged files will be preserved
- The SQLite database (`agents.db`) will continue to work
- Remote repository connections will not be affected

## Additional Files With Old Path References

The following Python scripts in `DecideWright-EA/` contain hardcoded paths to the old folder name. These are utility scripts that may need updating if you run them:

- `implement_business_unit_analysis.py`
- `generate_performance_analysis_sheets.py`
- `generate_risk_documentation_sheets.py`
- `generate_risk_dashboard.py`
- And approximately 18 other utility scripts

If you need to use any of these scripts, update the paths inside them from `AAgents` to `Agent-Cleo`.

## Troubleshooting

**If the rename fails with "Device or resource busy"**:
- Make sure all terminal windows are closed
- Make sure Claude Code is not running in that directory
- Make sure no Python processes are running (`tasklist | findstr python`)
- Restart your computer if needed

**If the application doesn't work after rename**:
- Double-check the BASE_PATH in `app.py` (line 16)
- Run "Initialize System" from the web dashboard
- Check the console for error messages
