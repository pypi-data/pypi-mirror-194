import re
from re import Pattern

from abuse_whois.schemas import Contact, WhoisRecord
from abuse_whois.utils import is_email
from abuse_whois.whois import get_whois_record

from .rules import load_rules


def get_whois_abuse_contact_by_regexp(
    record: WhoisRecord, *, abuse_email_pattern: Pattern = r"abuse@[a-z0-9\-.]+"
) -> Contact | None:
    provider = record.registrar or ""

    matches = re.findall(abuse_email_pattern, record.raw_text)
    if len(matches) == 0:
        return None

    # returns the email address in the bottom
    matches.reverse()
    for match in matches:
        if is_email(str(match)):
            return Contact(provider=provider, address=str(match))

    return None


def get_whois_abuse_contact(record: WhoisRecord) -> Contact | None:
    provider = record.registrar
    email: str | None = None

    # check email format for just in case
    if is_email(record.abuse.email or ""):
        email = record.abuse.email

    if email is None:
        # fallback to regexp based search
        contact = get_whois_abuse_contact_by_regexp(record)
        if contact is None:
            return None

        provider = contact.provider
        email = contact.address

    # use email's domain as a provider
    if is_email(provider or ""):
        provider = email.split("@")[-1]

    if provider is None or email is None:
        return None

    return Contact(provider=provider, address=email)


async def get_contact_from_whois(
    hostname: str,
) -> Contact | None:
    rules = load_rules()
    for rule in rules:
        if await rule.match(hostname):
            return rule.contact

    # Use whois registrar & abuse data
    try:
        whois_record = await get_whois_record(hostname)
    except Exception:
        return None

    return get_whois_abuse_contact(whois_record)
