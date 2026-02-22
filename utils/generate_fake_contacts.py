from faker import Faker

def generate_vcf(n, filename="contacts.vcf"):
    fake = Faker('de_DE')
    
    with open(filename, "w", encoding="utf-8") as f:
        for _ in range(n):
            first_name = fake.first_name()
            last_name = fake.last_name()
            phone = fake.phone_number()
            email = fake.email()
            street = fake.street_address()
            city = fake.city()
            zip_code = fake.postcode()
            
            
            # Demo: https://de.wikipedia.org/wiki/VCard#vCard_4.0

            vcard = [
                "BEGIN:VCARD",
                "VERSION:4.0",
                f"KIND:individual",
                f"N:{last_name};{first_name};;;",
                f"FN:{first_name} {last_name}",
                f"EMAIL;TYPE=home:{email}",
                f"TEL;VALUE=uri;TYPE=home:tel:{phone.replace(' ', '')}",
                f"ADR;TYPE=home:;;{street};{city};;{zip_code};Germany",
                f"REV:{fake.date_time_this_year().strftime('%Y%m%dT%H%M%SZ')}",
                "END:VCARD",
            ]
            
            f.write("\n".join(vcard))
    
    print(f"Erfolgreich {n} Kontakte in {filename} erstellt.")

# Beispielaufruf für 10 Kontakte
generate_vcf(10)