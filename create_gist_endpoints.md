# SPEED PROOFS - Custom Gist Endpoints Setup

## Instructions

Create 8 GitHub Gists with the following content at these paths:

### 1. Version Check
**Path:** `raw`  
**Content:** `V2`

### 2. Expiry Check
**Path:** `raw/Expiry`  
**Content:** `V2|2099-12-31`  ← Change date to whatever you want

### 3. Status Check
**Path:** `raw`  
**Content:** `LIVE`

### 4. APK Run/Crash Control
**Path:** `raw/ApkRunOrCrash`  
**Content:** `LIVE`

### 5. Redirect Link
**Path:** `raw/RedirectLink`  
**Content:** `Ok`

### 6. APK Update Check
**Path:** `raw/ApkUpdate`  
**Content:** `V2`

### 7. Base Expiry (same as #2)
**Path:** `raw` (of second gist)  
**Content:** `V2|2099-12-31`

### 8. Base Status (same as #3)
**Path:** `raw` (of third gist)  
**Content:** `LIVE`

---

## How to Create Gists

1. Go to https://gist.github.com
2. Click "Create a new gist"
3. Name the file (e.g., `version.txt`)
4. Paste the content above
5. Make it PUBLIC
6. Copy the raw URL from the gist

You need 3 gists total:
- **Gist 1:** `version.txt` → https://gist.githubusercontent.com/YOURUSER/GIST1_ID/raw
- **Gist 2:** `expiry.txt` → https://gist.githubusercontent.com/YOURUSER/GIST2_ID/raw/Expiry  
- **Gist 3:** `status.txt` → https://gist.githubusercontent.com/YOURUSER/GIST3_ID/raw/ApkRunOrCrash

---

## After Creating Gists

Run the patcher:
```bash
python patch_demoN.py DEMON-X.sh DEMON-X-patched "https://gist.githubusercontent.com/YOURUSER/YOUR_GIST_BASE"
```

Example:
```bash
python patch_demoN.py DEMON-X.sh DEMON-X-patched "https://gist.githubusercontent.com/karlosays01-prog/speedproofs-keys"
```

---

## Testing

After patching:
1. Push patched binary to device: `adb push DEMON-X-patched /data/local/tmp/DEMON-X`
2. Make executable: `adb shell chmod +x /data/local/tmp/DEMON-X`
3. Run: `adb shell /data/local/tmp/DEMON-X`
4. Should show: `✓ ACCESS GRANTED ✓` (if expiry date is in future)

To expire: Change gist content to `V2|2024-01-01` → Shows `HACK IS EXPIRED`
