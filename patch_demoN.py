#!/usr/bin/env python3
"""
SPEED PROOFS - DEMON-X Key System Patcher
Replaces old gist URLs with your custom Firebase/hosted endpoints.
Usage: python patch_demoN.py <input_binary> <output_binary> [gist_base_url]

Example:
  python patch_demoN.py DEMON-X.sh DEMON-X-patched https://gist.githubusercontent.com/YOURUSER/YOURGIST
"""

import sys
import re
import os

# Original gist URLs from DEMON-X
OLD_URLS = [
    b'https://gist.githubusercontent.com/tonmoyahmedshuvo11-hash/e76593497e5a25b542a2db71a49ddaf4/raw',           # Version check
    b'https://gist.githubusercontent.com/tonmoyahmedshuvo11-hash/6ccbe39667dd7258b4b562ccb40b145b/raw/Expiry', # Expiry check
    b'https://gist.githubusercontent.com/tonmoyahmedshuvo11-hash/981daf056060f174795de81893a57ced/raw',          # Status check
    b'https://gist.githubusercontent.com/tonmoyahmedshuvo11-hash/981daf056060f174795de81893a57ced/raw/ApkRunOrCrash', # Run/Crash control
    b'https://gist.githubusercontent.com/tonmoyahmedshuvo11-hash/22fd95f870135c42e7d8c65ba6388fa5/raw/RedirectLink', # Redirect link
    b'https://gist.githubusercontent.com/tonmoyahmedshuvo11-hash/e76593497e5a25b542a2db71a49ddaf4/raw/ApkUpdate',   # Update check
    b'https://gist.githubusercontent.com/tonmoyahmedshuvo11-hash/6ccbe39667dd7258b4b562ccb40b145b/raw',            # Base expiry
    b'https://gist.githubusercontent.com/tonmoyahmedshuvo11-hash/22fd95f870135c42e7d8c65ba6388fa5/raw',            # Base status
]

def build_new_urls(base_url):
    """Build new URLs based on provided base URL."""
    base = base_url.encode('utf-8') if isinstance(base_url, str) else base_url
    return [
        base + b'/raw',                                        # Version -> "V2"
        base + b'/raw/Expiry',                                 # Expiry -> "V2|YYYY-MM-DD"
        base + b'/raw',                                        # Status -> "LIVE"
        base + b'/raw/ApkRunOrCrash',                          # Run/Crash -> "LIVE"
        base + b'/raw/RedirectLink',                           # Redirect -> "Ok"
        base + b'/raw/ApkUpdate',                              # Update -> "V2"
        base + b'/raw/Expiry',                                 # Base expiry -> same as above
        base + b'/raw',                                        # Base status -> same as above
    ]

def patch_binary(input_path, output_path, new_base_url=None):
    """Patch DEMON-X binary by replacing gist URLs."""
    print(f"\n{'='*60}")
    print(f"  SPEED PROOFS - DEMON-X Key System Patcher")
    print(f"{'='*60}\n")

    if not os.path.exists(input_path):
        print(f"ERROR: Input file '{input_path}' not found!")
        return False

    with open(input_path, 'rb') as f:
        data = bytearray(f.read())

    print(f"Input file: {input_path}")
    print(f"Size: {len(data):,} bytes\n")

    # Determine new URLs
    if new_base_url:
        new_urls = build_new_urls(new_base_url)
        print(f"Using custom base URL: {new_base_url}\n")
        print("URL Replacements:")
    else:
        # Default: generate placeholder URLs for user to fill in
        print("WARNING: No base URL provided! Using PLACEHOLDER URLs.")
        print("You MUST update these URLs manually in the output binary.\n")
        placeholder_base = b"https://gist.githubusercontent.com/SPEEDPROOFS_USER/SPEEDPROOFS_GIST_ID"
        new_urls = build_new_urls(placeholder_base)
        for i, (old, new) in enumerate(zip(OLD_URLS, new_urls)):
            old_str = old.decode('utf-8', errors='ignore')
            new_str = new.decode('utf-8', errors='ignore')
            status = "UPDATED" if not new_str.startswith(b'SPEEDPROOFS') else "PLACEHOLDER"
            print(f"  [{i+1}] {old_str[:60]}... -> {status}")
        print("\n** IMPORTANT: Edit the output binary to replace placeholders! **\n")

    total_replaced = 0
    replaced_indices = []

    for old_url, new_url in zip(OLD_URLS, new_urls):
        # Find all occurrences of this URL in the binary
        positions = []
        search_start = 0
        while True:
            pos = data.find(old_url, search_start)
            if pos == -1:
                break
            positions.append(pos)
            search_start = pos + 1

        if positions:
            print(f"  Found {len(positions)} occurrence(s):")
            print(f"    OLD: {old_url.decode('utf-8', errors='ignore')}")
            print(f"    NEW: {new_url.decode('utf-8', errors='ignore')}")

            for pos in positions:
                # Calculate how much padding/truncation is needed
                new_len = len(new_url)
                old_len = len(old_url)

                if new_len <= old_len:
                    # New URL fits - pad with nulls if shorter
                    padded_new = new_url + b'\x00' * (old_len - new_len)
                    data[pos:pos+old_len] = padded_new
                else:
                    # New URL is longer - truncate (may cause issues)
                    print(f"    WARNING: New URL is {new_len} bytes, old was {old_len} bytes!")
                    print(f"    Truncating new URL to fit. This may cause instability.")
                    data[pos:pos+old_len] = new_url[:old_len]

                total_replaced += 1
                replaced_indices.append(pos)

        else:
            print(f"  NOT FOUND: {old_url.decode('utf-8', errors='ignore')}")

    # Save patched binary
    with open(output_path, 'wb') as f:
        f.write(data)

    print(f"\n{'='*60}")
    if total_replaced > 0:
        print(f"  SUCCESS: Patched {total_replaced} URL(s)")
        print(f"  Output: {output_path}")
    else:
        print(f"  FAILED: No URLs were replaced!")
        print(f"  Check if the input file contains the expected URLs.")
    print(f"{'='*60}\n")

    return total_replaced > 0

def verify_patch(input_path, output_path):
    """Verify the patch by checking if old URLs are gone and new ones exist."""
    with open(input_path, 'rb') as f:
        orig_data = f.read()
    with open(output_path, 'rb') as f:
        patched_data = f.read()

    print("\nVerification:")
    issues = []

    for old_url in OLD_URLS:
        if old_url in patched_data:
            count = patched_data.count(old_url)
            issues.append(f"  FAIL: Old URL still present ({count} times): {old_url[:50]}...")
        elif old_url not in orig_data:
            pass  # Not in original either
        else:
            print(f"  OK: Removed {old_url[:50]}...")

    # Check for new URLs
    for new_url in new_urls:
        if new_url in patched_data:
            print(f"  OK: Added {new_url[:50]}...")
        else:
            issues.append(f"  WARN: New URL not found: {new_url[:50]}...")

    if issues:
        print("\nIssues found:")
        for issue in issues:
            print(issue)
        return False
    return True

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        print(f"\nQuick usage:")
        print(f"  python {sys.argv[0]} DEMON-X.sh DEMON-X-patched 'YOUR_BASE_URL'")
        print(f"\nExample:")
        print(f"  python {sys.argv[0]} DEMON-X.sh DEMON-X-patched 'https://gist.githubusercontent.com/YOUR_USER/YOUR_GIST'")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    base_url = sys.argv[3] if len(sys.argv) > 3 else None

    success = patch_binary(input_file, output_file, base_url)

    if success and len(sys.argv) > 3:
        verify_patch(input_file, output_file)
