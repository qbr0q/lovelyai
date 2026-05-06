import re


def search_ticket_id(text: str) -> int:
    ticket_id_str = re.search(r'#(\d+)', text).group(1)
    if ticket_id_str:
        return int(ticket_id_str)
