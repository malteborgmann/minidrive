from typing import List

import vobject

from app.pydantic_schema import schema


def parse_vcards(vcf_content: str) -> List[schema.ContactCreate]:
    contacts = []

    vcards = list(vobject.readComponents(vcf_content))

    for vcard in vcards:
        first_name = ""
        last_name = ""

        # Namen extrahieren
        if hasattr(vcard, "n"):
            last_name = vcard.n.value.family
            first_name = vcard.n.value.given
        elif hasattr(vcard, "fn"):
            parts = vcard.fn.value.split(" ", 1)
            if len(parts) == 2:
                first_name, last_name = parts
            else:
                first_name = parts[0]

        company = ""
        if hasattr(vcard, "org"):
            org_val = vcard.org.value
            company = org_val[0] if isinstance(org_val, list) else org_val

        notes = ""
        if hasattr(vcard, "note"):
            notes = vcard.note.value

        address = ""
        if hasattr(vcard, "adr"):
            adr = vcard.adr.value
            addr_parts = [adr.street, adr.city, adr.code, adr.country]
            address = ", ".join([p for p in addr_parts if p])

        communications = []

        # Telefonnummern extrahieren
        if hasattr(vcard, "tel"):
            for tel in vcard.contents.get("tel", []):
                types = tel.params.get("TYPE", [])
                label = ",".join(types) if types else "phone"
                communications.append(
                    schema.CommunicationCreate(
                        comm_type="phone", label=label.lower(), value=tel.value
                    )
                )

        # E-Mail-Adressen extrahieren
        if hasattr(vcard, "email"):
            for em in vcard.contents.get("email", []):
                types = em.params.get("TYPE", [])
                label = ",".join(types) if types else "email"
                communications.append(
                    schema.CommunicationCreate(
                        comm_type="email", label=label.lower(), value=em.value
                    )
                )

        # Pydantic Schema
        contact_in = schema.ContactCreate(
            first_name=first_name,
            last_name=last_name,
            company=company,
            notes=notes,
            address=address,
            communications=communications,
        )

        contacts.append(contact_in)

    return contacts


if __name__ == "__main__":
    content = """BEGIN:VCARD
VERSION:3.0
N:Rust;Edwin;;;
FN:Edwin Rust
EMAIL;TYPE=INTERNET,HOME:kdrewes@example.org
TEL;TYPE=CELL,VOICE:+49(0)1966840149
ADR;TYPE=HOME:;;Klaas-Stumpf-Allee 9823;Biedenkopf;;66776;Germany
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Gutknecht;Antonios;;;
FN:Antonios Gutknecht
EMAIL;TYPE=INTERNET,HOME:marvinwerner@example.org
TEL;TYPE=CELL,VOICE:08266 14304
ADR;TYPE=HOME:;;Stiebitzstr. 95;Grevenbroich;;10194;Germany
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Heintze;Volkhard;;;
FN:Volkhard Heintze
EMAIL;TYPE=INTERNET,HOME:pruschketilman@example.com
TEL;TYPE=CELL,VOICE:06077047581
ADR;TYPE=HOME:;;Cäcilie-Dörschner-Ring 9-9;Hünfeld;;22720;Germany
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Kusch;Apollonia;;;
FN:Apollonia Kusch
EMAIL;TYPE=INTERNET,HOME:yjunitz@example.com
TEL;TYPE=CELL,VOICE:(05435) 151626
ADR;TYPE=HOME:;;Tlustekring 595;Ahaus;;68909;Germany
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Peukert;Halil;;;
FN:Halil Peukert
EMAIL;TYPE=INTERNET,HOME:gerlachgino@example.com
TEL;TYPE=CELL,VOICE:+49(0)0261 207042
ADR;TYPE=HOME:;;Birgitta-Dowerg-Weg 86/51;Lüneburg;;94770;Germany
END:VCARD
"""

    print(parse_vcards(content)[1].model_dump())
