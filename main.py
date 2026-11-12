import json
from pathlib import Path

def baca_pengetahuan():
    lokasi_file = Path(__file__).with_name("kb_printer.json")

    with open(lokasi_file, "r", encoding="utf-8") as file:
        pengetahuan = json.load(file)

    return pengetahuan

def aturan_terpenuhi(aturan, memori):
    syarat = aturan["jika"]
    mode = aturan["mode"]

    if mode == "dan":
        return all(fakta in memori for fakta in syarat)

    elif mode == "atau":
        return any(fakta in memori for fakta in syarat)

    return False

def forward_chaining(aturan, memori):
    asal_kesimpulan = {}
    nomor_siklus = 1

    while True:
        ada_fakta_baru = False

        for rule in aturan:
            hasil = rule["maka"]

            if hasil in memori:
                continue

            if aturan_terpenuhi(rule, memori):
                memori.add(hasil)
                asal_kesimpulan[hasil] = rule

                print(
                    f"Siklus {nomor_siklus}: "
                    f"{rule['id']} -> {hasil}"
                )

                nomor_siklus += 1
                ada_fakta_baru = True

        if not ada_fakta_baru:
            break

    return memori, asal_kesimpulan

def tampilkan_alasan(fakta, asal_kesimpulan, fakta_awal, indent=0):
    spasi = " " * indent
    fakta_tampil = fakta.replace("_", " ").capitalize()

    if fakta in fakta_awal:
        print(f"{spasi}- {fakta_tampil} (fakta dari pengguna)")
        return

    if fakta not in asal_kesimpulan:
        return

    rule = asal_kesimpulan[fakta]
    sumber = ", ".join(rule["sumber"])

    print(f"{spasi}- {fakta_tampil} <- {rule['id']} (Sumber: {sumber})")

    for syarat in rule["jika"]:
        tampilkan_alasan(
            syarat,
            asal_kesimpulan,
            fakta_awal,
            indent + 4
        )

def main():
    pengetahuan = baca_pengetahuan()

    print("=" * 60)
    print(pengetahuan["judul"])
    print("=" * 60)

    print("\nJawab pertanyaan dengan y (ya) atau t (tidak).\n")

    aturan = pengetahuan["aturan"]

    semua_syarat = set()
    semua_hasil = set()

    for rule in aturan:
        semua_syarat.update(rule["jika"])
        semua_hasil.add(rule["maka"])

    fakta_awal = semua_syarat - semua_hasil

    memori = set()
    nomor = 1

    for fakta in pengetahuan["pertanyaan"]:
        if fakta not in fakta_awal:
            continue

        pertanyaan = pengetahuan["pertanyaan"][fakta]

        while True:
            jawaban = input(f"{nomor}. {pertanyaan} (y/t): ").lower().strip()

            if jawaban in ["y", "ya"]:
                memori.add(fakta)
                break

            elif jawaban in ["t", "tidak"]:
                break

            else:
                print("Jawaban tidak valid. Masukkan y atau t.")

        nomor += 1

    fakta_pengguna = memori.copy()

    print("\nFakta awal:", ", ".join(fakta_pengguna) if fakta_pengguna else "Tidak ada")

    print("\n--- PROSES FORWARD CHAINING ---")

    memori, asal_kesimpulan = forward_chaining(aturan, memori)

    kesimpulan_akhir = semua_hasil - semua_syarat

    hasil_ditemukan = [
        rule["maka"]
        for rule in aturan
        if rule["maka"] in kesimpulan_akhir
        and rule["maka"] in memori
    ]

    print("\n--- HASIL SISTEM PAKAR ---")

    if hasil_ditemukan:
        for hasil in hasil_ditemukan:
            nama_kesimpulan = hasil.replace("_", " ").capitalize()
            print(f"\nKesimpulan: {nama_kesimpulan}")
            print("Alasan:")

            tampilkan_alasan(
                hasil,
                asal_kesimpulan,
                fakta_pengguna,
                indent=2
            )
    else:
        print("Tidak ditemukan kesimpulan berdasarkan aturan yang tersedia.")

    print("\nCatatan:")
    print(pengetahuan["batas"])


if __name__ == "__main__":
    main()
