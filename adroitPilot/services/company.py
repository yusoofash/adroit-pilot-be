from .auth import PersonServices, EntityType


class Company(PersonServices):
    def __init__(self):
        company = EntityType.company.name
        super().__init__(company)

    def register_company(self, company_details):
        return self.register_service(company_details)

    def get_companies(self):
        return self.get_entity()

    def get_company(self, company_id):
        return self.get_entity(company_id)

    def authenticate_company(self, email, password):
        return self.authenticate(email, password)

    def update_company_details(self, company_id, details):
        return self.update_details(company_id, details)

    def companies_matching_keywords(self, keywords):
        companies = self.db.read({"keywords": {"$in": keywords}})
        companies_dto = []
        for company1 in list(companies):
            del company1['password']
            companies_dto.append(company1)
        return companies_dto