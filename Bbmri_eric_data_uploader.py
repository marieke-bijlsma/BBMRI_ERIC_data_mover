import pprint

from Bbmri_eric_quality_checker.qualityChecker import QualityChecker
from Bbmri_eric_quality_checker.configParser import ConfigParser
from molgenis.molgenisConnector import MolgenisConnector


class BbmriEricDataUploader():
    def __init__(self, config):
        self.filter_rows = ""
        self.collections = ""
        self.biobanks = ""
        self.networks = ""
        self.persons = ""
        self.server = config['target_server']
        self.username = config['target_account']
        self.password = config['target_password']
        url = config['url']
        molgenis_connector = MolgenisConnector(url, config['account'], config['password'])
        self.retrieve_data(molgenis_connector)
        self.retrieve_country_data(config, molgenis_connector)

    def retrieve_country_data(self, config, molgenis_connector):
        countries = config['countries'].split(',')
        for country in countries:
            print(country)
            # filter out rows with invalid disease type/network
            collections = self.convert_refs(
                molgenis_connector.session.get("eu_bbmri_eric_{}_collections".format(country), num=10000))
            biobanks = self.convert_refs(
                molgenis_connector.session.get("eu_bbmri_eric_{}_biobanks".format(country), num=10000))
            persons = self.convert_refs(
                molgenis_connector.session.get("eu_bbmri_eric_{}_persons".format(country), num=10000))
            networks = self.convert_refs(
                molgenis_connector.session.get("eu_bbmri_eric_{}_networks".format(country), num=10000))
            if len(persons) > 0:
                try:
                    self.upload_data("eu_bbmri_eric_{}_persons".format(country), persons, self.server, self.username,
                                     self.password)
                except:
                    print("Uploading {} failed, is it already uploaded?".format(
                        "eu_bbmri_eric_{}_persons".format(country)))
            if len(networks) > 0:
                try:
                    self.upload_data("eu_bbmri_eric_{}_networks".format(country), networks, self.server, self.username,
                                 self.password)
                except:
                    print("Uploading {} failed, is it already uploaded?".format(
                        "eu_bbmri_eric_{}_networks".format(country)))
            if len(biobanks) > 0:
                try:
                    self.upload_data("eu_bbmri_eric_{}_biobanks".format(country), biobanks, self.server, self.username,
                                 self.password)
                except:
                    print("Uploading {} failed, is it already uploaded?".format(
                        "eu_bbmri_eric_{}_biobanks".format(country)))
            if len(collections) > 0:
                try:
                    self.upload_data("eu_bbmri_eric_{}_collections".format(country), collections, self.server,
                                 self.username, self.password)
                except:
                    print("Uploading {} failed, is it already uploaded?".format(
                        "eu_bbmri_eric_{}_collections".format(country)))

    def retrieve_data(self, molgenis_connector):
        qc = QualityChecker(molgenis_connector)
        qc.check_collection_data()
        qc.check_biobank_data()
        qc.check_network_data()
        qc.check_person_data()
        qc.logs.close()
        self.filter_rows = qc.breaking_errors
        self.collections = self.convert_refs(qc.collection_data)
        self.biobanks = self.convert_refs(qc.biobank_data)
        self.networks = self.convert_refs(qc.network_data)
        self.persons = self.convert_refs(qc.person_data)
        # order: persons, networks, biobanks, collections
        try:
            self.upload_data("eu_bbmri_eric_persons", self.persons, self.server, self.username, self.password)
        except:
            print("Uploading {} failed, is it already uploaded?".format("eu_bbmri_eric_persons"))
        try:
            self.upload_data("eu_bbmri_eric_networks", self.networks, self.server, self.username, self.password)
        except:
            print("Uploading {} failed, is it already uploaded?".format("eu_bbmri_eric_networks"))
        try:
            self.upload_data("eu_bbmri_eric_biobanks", self.biobanks, self.server, self.username, self.password)
        except:
            print("Uploading {} failed, is it already uploaded?".format("eu_bbmri_eric_biobanks"))
        try:
            self.upload_data("eu_bbmri_eric_collections", self.collections, self.server, self.username, self.password)
        except:
            print("Uploading {} failed, is it already uploaded?".format("eu_bbmri_eric_collections"))

    def upload_data(self, entity, entities, url, user, pwd):
        new_server = MolgenisConnector(url, user, pwd)
        print('Uploading {}...'.format(entity))
        status = new_server.session.add_all(entity, entities)

    def convert_refs(self, data):
        new_data = []
        for i, item in enumerate(data):
            new_item = item
            del new_item['_href']
            if new_item['id'] not in self.filter_rows['collection'] and new_item['id'] not in self.filter_rows[
                'biobank']:
                delete_network = False
                for key in new_item:
                    if type(new_item[key]) is dict:
                        ref = new_item[key]['id']
                        new_item[key] = ref
                    elif key == 'network':
                        if len(new_item[key]) > 0:
                            mref = [l['id'] for l in new_item[key]]
                            new_item[key] = mref[0]
                        else:
                            delete_network = True
                    elif type(new_item[key]) is list:
                        if len(new_item[key]) > 0:
                            # get id for each new_item in list
                            mref = [l['id'] for l in new_item[key]]
                            new_item[key] = mref
                if delete_network:
                    del new_item['network']
                new_data.append(new_item)
        return new_data

def main():
    config = ConfigParser().config
    data_uploader = BbmriEricDataUploader(config)


if __name__ == '__main__':
    main()
