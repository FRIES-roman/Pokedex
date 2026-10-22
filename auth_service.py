class AuthService:
    def __init__(self, uzivatele):
        self.uzivatele = uzivatele
    def najdi_uzivatele(self, email):
        for uzivatele in self.uzivatele:
            if uzivatele.email == email:
                return uzivatele

            return None
