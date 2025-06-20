import os, hashlib, json

def hash_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''): h.update(chunk)
    return h.hexdigest()

def scan_dir(directory):
    return {os.path.join(r, f): hash_file(os.path.join(r, f))
            for r, _, fs in os.walk(directory) for f in fs}

def main():
    folder = input("Directory to scan: ")
    mode = input("Type 'save' to store or 'check' to compare: ")
    db = "hashes.json"

    if mode == "save":
        with open(db, 'w') as f: json.dump(scan_dir(folder), f)
        print("Hashes saved.")
    elif mode == "check":
        old = json.load(open(db))
        new = scan_dir(folder)

        modified = [f for f in old if f in new and old[f] != new[f]]
        deleted = [f for f in old if f not in new]
        added = [f for f in new if f not in old]

        print("\nModified:", *modified, sep="\n" if modified else " None")
        print("Deleted:", *deleted, sep="\n" if deleted else " None")
        print("Added:", *added, sep="\n" if added else " None")
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()