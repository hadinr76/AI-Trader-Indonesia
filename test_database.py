from database.database import Database

print("=" * 60)
print("DATABASE TEST")
print("=" * 60)

Database.initialize()

Database.save_scan(
    "BBCA",
    6500,
    100,
    90,
    96,
    "★★★★★",
    "BUY"
)

print("Data berhasil disimpan.\n")

history = Database.get_history("BBCA")

for row in history:
    print(row)