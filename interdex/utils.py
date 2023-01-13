from datetime import datetime
from json import dumps
from os import path


def convert_footer_to_date(footer_content: str):
    # Updated 02 Oct 2022 14:30 PST © 2022 Hurricane Electric
    return datetime.strptime(footer_content, f'Updated %d %b %Y %H:%M PST © {datetime.now().year} Hurricane Electric')


def date_to_json(date: datetime) -> str:
    return str(date)


def json_date_to_datetime(date: str) -> datetime:
    # 2022-10-02 14:30:00
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


def sanitize_string(string):
    return string.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ", "-").replace("--",
                                                                                                  "").strip().lower()


def get_dns_status(data) -> str:
    # <td class="centeralign">
    #   <img alt="O" src="/images/o.png?1142218094" />
    # </td>
    if len(data) > 0:
        data = data[0]
        alt = str(data["alt"]).lower()
        if alt == "o":
            return "OK"
        elif alt == "e":
            return "WARN"
        elif alt == "x":
            return "ERR"


def save_to_json(data: list, filename: str):
    print(f"Saving {filename}")
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(dumps(data, indent=4))


def split(a, n):
    """
    Splitting a list into N parts of approximately equal length
    """
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def get_current_time():
    return datetime.now()
