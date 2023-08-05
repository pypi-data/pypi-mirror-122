import unittest
from upswingutil.ml import cancellation_risk_score
import upswingutil as ul
from upswingutil.pms import PMS

ul.ENCRYPTION_SECRET = "S1335HwpKYqEk9CM0I2hFX3oXa5T2oU86OXgMSW4s6U="
ul.MONGO_URI = "mongodb://AdminUpSwingGlobal:Upswing098812Admin0165r@dev.db.upswing.global:27017/?authSource=admin&readPreference=primary&appname=Agent%20Oracle%20Dev&ssl=false"
ul.G_CLOUD_PROJECT = "aura-staging-31cae"
ul.FIREBASE = "/Users/harsh/upswing/github/api-oracle/SECRET/aura-staging-31cae-firebase-adminsdk-dyolr-7c135838e9.json"
ul.LOG_LEVEL_VALUE = 'DEBUG'


class TestCancellationRiskScore(unittest.TestCase):

    def test_creating_model_for_rms(self):
        """ Train and store model for RMS """
        orgId = '11249'
        crf = cancellation_risk_score(PMS.RMS, orgId)
        crf.preprocess()
        crf.train()



    def test_predict_from_model_rms(self):
        orgId = '11249'
        crf = cancellation_risk_score(PMS.RMS, orgId)
        result = crf.predict(9, 2, 1, 'unknown', 0, 104, 0, 11263, 0, 0, 'VIP', 'Duo', 52.0, 5.0, 78.0, 7, 11, 4.0)

        print(result)


if __name__ == '__main__':
    unittest.main()
