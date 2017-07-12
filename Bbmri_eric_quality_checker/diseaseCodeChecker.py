import re, sys, os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR+"/data_model")

class DiseaseCodeChecker():
    def __init__(self):
        self.warningCodes = ['ORDO', 'orphanet', 'urn:miriam:icd:*', 'urn:miriam:icd:A04*']
        self.errorCodes = ['NA', 'OMIM', 'TRUE', 'urn:miriam:icd:01', 'urn:miriam:icd:02', 'urn:miriam:icd:03',
                           'urn:miriam:icd:04', 'urn:miriam:icd:05', 'urn:miriam:icd:06', 'urn:miriam:icd:07',
                           'urn:miriam:icd:08', 'urn:miriam:icd:09', 'urn:miriam:icd:10', 'urn:miriam:icd:11',
                           'urn:miriam:icd:12', 'urn:miriam:icd:13', 'urn:miriam:icd:14', 'urn:miriam:icd:15',
                           'urn:miriam:icd:16', 'urn:miriam:icd:17', 'urn:miriam:icd:18', 'urn:miriam:icd:19',
                           'urn:miriam:icd:20', 'urn:miriam:icd:21', 'urn:miriam:icd:22', 'urn:miriam:icd:A0']
        self.valid_disease_types = []

    def parse_disease_types(self):
        for i, line in enumerate(open("eu_bbmri_disease_types.csv")):
            if i != 0:
                line = line.split(",")
                self.valid_disease_types.append(line[0])

    def is_code_in_list(self, code, list):
        if code in list:
            return True
        else:
            return False

    def has_wildcard(self, code):
        pattern = r"(urn:miriam:icd:[A-Z]{1}\d{0,2})(\*)"
        if re.match(pattern, code):
            return True
        else:
            return False

    def check_code(self, code):
        log = []
        if not self.is_code_in_list(code, self.valid_disease_types):
            log.append('Diagnosis code not valid: ' + code)
            log.append('CRITICAL')
            log.append('COLLECTION DIAGNOSIS CODE NOT VALID')
            return log
        elif self.is_code_in_list(code, self.warningCodes):
            log.append('WARNING: Diagnosis contains wildcard: ' + code)
            log.append('WARNING')
            log.append('COLLECTION DIAGNOSIS CONTAINS WILDCARD')
            return log
        elif self.has_wildcard(code):
            log.append('WARNING: Diagnosis contains wildcard: ' + code)
            log.append('WARNING')
            log.append('COLLECTION DIAGNOSIS CONTAINS WILDCARD')
            return log
