from faker import Faker


def generate_vcf(n, filename="contacts.vcf"):
    fake = Faker("de_DE")

    with open(filename, "w", encoding="utf-8") as f:
        for _ in range(n):
            first_name = fake.first_name()
            last_name = fake.last_name()
            phone = fake.phone_number()
            email = fake.email()
            street = fake.street_name()
            number = fake.building_number()
            city = fake.city()
            zip_code = fake.postcode()

            # Demo: https://de.wikipedia.org/wiki/VCard#vCard_3.0
            # Using vCard 3.0 Format
            # Apple Contacts App uses vCard 3.0 Format as well as Google Contacts App.

            vcard = [
                "BEGIN:VCARD",
                "VERSION:3.0",
                f"N:{last_name};{first_name};;;",
                f"FN:{first_name} {last_name}",
                f"EMAIL;TYPE=INTERNET,HOME:{email}",
                f"TEL;TYPE=CELL,VOICE:{phone}",
                f"ADR;TYPE=HOME:;;{street} {number};{city};;{zip_code};Germany",
                "END:VCARD",
                "",
            ]
            f.write("\n".join(vcard))
    print(f"Erfolgreich {n} Kontakte in {filename} erstellt.")


generate_vcf(5)
