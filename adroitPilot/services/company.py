from .auth import PersonServices, EntityType
from .prediction import weightage
import re

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

    def get_matching_keywords(self, key, keywords):
        cleansed_data = []
        for data in keywords:
            # using regular expression to remove punctuations and considering only alphanumeric characters
            filtered_data = re.sub('[^\w^\.]', '', data.strip().lower())
            cleansed_data.append(filtered_data)

        keywords_list = self.db.read({key: {"$in": cleansed_data}}, {"keywords": 1, "_id": 0})
        keywords_dto = []
        for keywords_arr in list(keywords_list):
            for keyword in keywords_arr[key]:
                if keyword in cleansed_data:
                    keywords_dto.append(keyword.lower())
        return set(keywords_dto)

    def rank_companies(self, user_details):
        company_details = self.get_companies()
        prediction = weightage(user_details, company_details)
        return prediction
