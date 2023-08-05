from requests import get
from urllib.parse import urlencode

class SMSClient:
    """BulkSMSAPI Wrapper (bulksms.md)\n
    SMSClient object contains two methods: `send_sms_simple` & `send_sms_nde`.

    Args:
        username (str): Nume de utilizator unic al clientului.
        password (str): Parola de acces.
        sender (str): Nume ale senderilor  prestabilite în contract. Maximum 11 simboluri.
        dlrurl (str, optional): Adresa URL care va fi apelată pentru trimiterea raportului DLR. Defaults to ''.
        dlrmask (int, optional): Mască de biţi, pentru determinarea rapoartelor DLR necesare. Defaults to 31.
        charset (str, optional): Determină  codificarile în care se trimit textele mesajelor. Codificari disponibile: plaintext, windows-1251, utf8. Defaults to 'utf-8'.
        coding (str, optional): Folosiţi întotdeauna: 2. Defaults to '2'.
    """

    def __init__(
            self,
            username: str,
            password: str,
            sender: str,
            dlrurl: str = '',
            dlrmask: int = 31,
            charset: str = 'utf-8',
            coding: str = '2',
        ) -> None:
        self.base_url = 'https://api.bulksms.md:4432/UnifunBulkSMSAPI.asmx/SendSMSNoneDigitsEncoded?'
        self.username = username
        self.password = password
        self.sender = sender
        self.dlrurl = dlrurl
        self.dlrmask = dlrmask
        self.charset = charset
        self.coding = coding

    def _make_api_request(self, url: str, params: dict) -> dict:
        res = get(self.base_url + urlencode(params))
        return res

    def send_sms_simple(self, msisdn: str, body: str, prefix: str = '373') -> dict:
        """SendSMSSimple\n
        Varianta simplă a serviciului,
        care necesită date minime de intrare şi care nu necesită rapoarte de remitere SMS la abonat.
        În acest regim este posibilă trimiterea doar a mesajelor cu texte codificate în format plaintext,
        care conţin doar literele alfabetului latin nu mai mare de 160 de caractere. 

        Args:
            msisdn (str): Phone number without prefix.
            body (str): Body of the message.
            prefix (str, optional): Phone number prefix. Defaults to '373'.

        Returns:
            dict: Send message request response.
        """

        base_url = 'https://api.bulksms.md:4432/UnifunBulkSMSAPI.asmx/SendSMSSimple?'

        return self._make_api_request(base_url, {
            'username': self.username,
            'password': self.password,
            'from': self.sender,
            'to': prefix + msisdn,
            'text': body,
        })

    def send_sms_nde(self, msisdn: str, body: str, prefix: str = '373') -> dict:
        """SendSMSNoneDigitsEncoded\n
        Varianta deplină a serviciului,
        care permite trimiterea mesajelor SMS către abonaţi în diferite standarde de codificare,
        precum şi primirea rapoartelor de remitere a mesajului respectiv către abonat.

        Args:
            msisdn (str): Phone number without prefix.
            body (str): Body of the message.
            prefix (str, optional): Phone number prefix. Defaults to '373'.

        Returns:
            dict: Send message request response.
        """

        base_url = 'https://api.bulksms.md:4432/UnifunBulkSMSAPI.asmx/SendSMSNoneDigitsEncoded?'

        return self._make_api_request(base_url, {
            'username': self.username,
            'password': self.password,
            'charset': self.charset,
            'dlrmask': self.dlrmask,
            'dlrurl': self.dlrurl,
            'coding': self.coding,
            'from': self.sender,
            'to': prefix + msisdn,
            'text': body,
        })
