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
N:Rogge;Martine;;;
FN:Martine Rogge
EMAIL;TYPE=INTERNET,HOME:adelinde95@example.org
TEL;TYPE=CELL,VOICE:06605 54127
ADR;TYPE=HOME:;;Hatice-Jäntsch-Ring 3180;Vilsbiburg;;02406;Germany
END:VCARD"""

    print(parse_vcards(content))
