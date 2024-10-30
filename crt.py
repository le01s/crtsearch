import requests
from bs4 import BeautifulSoup

def parse_certificates(domain):
    url = f'https://crt.sh/?q={domain}'

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error getting data: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    certificates_table = soup.find_all('table')[1]
    certificates = []

    for row in certificates_table.find_all('tr')[1:]:
        columns = row.find_all('td')

        if len(columns) >= 7:
            cert_data = {
                'crt_id': columns[0].text.strip(),
                'logged_at': columns[1].text.strip(),
                'not_before': columns[2].text.strip(),
                'not_after': columns[3].text.strip(),
                'common_name': columns[4].text.strip(),
                'matching_identities': columns[5].text.strip(),
                'issuer_name': columns[6].text.strip(),
            }
            certificates.append(cert_data)

    if not certificates:
        print("Certificates not found")
        return

    print("Common Names:")
    for cert in certificates:
        common_name = cert['common_name']
        if common_name:
            print(common_name)


if __name__ == '__main__':
    domain = input("Input domain (example - example.com): ")
    parse_certificates(domain)