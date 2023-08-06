from unittest import TestCase
from ifd.tools import getJsonFromImage
from ifd.entities import Image, Classification, Modele, Couleur, bbox, OCR, Detection, Couleur
import json

class getJsonFromImage_test(TestCase):
    def test_json_load_with_image(self):

        image : Image = Image()
        image.id = 1
        image.img_path = "/path/where/is/image"
        image.classification = Classification()
        image.classification.score = 0.25636
        image.classification.label = "TestLabel"
        image.classification.modele = Modele()
        image.classification.modele.label = 'EfficientNetV2'
        image.classification.modele.version = 'V4'
        image.ref_infra_pto = 'TF-1256-RE'


        detection = Detection()
        detection.label = "PBO_TEST"
        detection.score = 0.15688
        detection.modele = Modele()
        detection.modele.label = 'YoloV5'
        detection.modele.version = 'Detect-PBO'
        detection.bbox = bbox()
        detection.bbox.xmax = 125
        detection.bbox.xmin = 485
        detection.bbox.ymin = 1256
        detection.bbox.ymax = 2562

        couleur = Couleur()
        couleur.label = "VERT"
        couleur.score = 0.5689
        couleur.modele = Modele()
        couleur.modele.label = 'YoloV5'
        couleur.modele.version = 'Couleur-Smoove'
        couleur.bbox = bbox()
        couleur.bbox.xmax = 145
        couleur.bbox.xmin = 523
        couleur.bbox.ymin = 1455
        couleur.bbox.ymax = 1458

        detection.couleurs.append(couleur)
        image.detections.append(detection)

        image.ocr = OCR()
        image.ocr.label = "PM_TEST"
        image.ocr.score = 0.15688
        image.ocr.modele = Modele()
        image.ocr.modele.label = 'YoloV5'
        image.ocr.modele.version = 'v1-pto-s6'
        image.ocr.bbox = bbox()
        image.ocr.bbox.xmax = 658
        image.ocr.bbox.xmin = 475
        image.ocr.bbox.ymin = 1452
        image.ocr.bbox.ymax = 1457
        image.ocr.score_ocr = 0.5683
        image.ocr.label_ocr = 'TF-1256-RE'

        data : str = getJsonFromImage(image)


        self.assertIs(image.id, data["id"])
        self.assertIs(image.img_path, data["img_path"])
        self.assertIs(image.img_checksum, data["img_checksum"])
        self.assertIs(image.rotation, data["rotation"])
        self.assertIs(image.ref_infra_pto, data["ref_infra_pto"])

        self.assertIs(image.detections[0].score, data["detections"][0]["score"])
        self.assertIs(image.detections[0].label, data["detections"][0]["label"])
        self.assertIs(image.detections[0].bbox.xmin, data["detections"][0]["bbox"]["xmin"])
        self.assertIs(image.detections[0].bbox.xmax, data["detections"][0]["bbox"]["xmax"])
        self.assertIs(image.detections[0].bbox.ymin, data["detections"][0]["bbox"]["ymin"])
        self.assertIs(image.detections[0].bbox.ymax, data["detections"][0]["bbox"]["ymax"])
        self.assertIs(image.detections[0].modele.label, data["detections"][0]["modele"]["label"])
        self.assertIs(image.detections[0].modele.version, data["detections"][0]["modele"]["version"])

        self.assertIs(image.detections[0].couleurs[0].score, data["detections"][0]["couleurs"][0]["score"])
        self.assertIs(image.detections[0].couleurs[0].label, data["detections"][0]["couleurs"][0]["label"])
        self.assertIs(image.detections[0].couleurs[0].bbox.xmin, data["detections"][0]["couleurs"][0]["bbox"]["xmin"])
        self.assertIs(image.detections[0].couleurs[0].bbox.xmax, data["detections"][0]["couleurs"][0]["bbox"]["xmax"])
        self.assertIs(image.detections[0].couleurs[0].bbox.ymin, data["detections"][0]["couleurs"][0]["bbox"]["ymin"])
        self.assertIs(image.detections[0].couleurs[0].bbox.ymax, data["detections"][0]["couleurs"][0]["bbox"]["ymax"])
        self.assertIs(image.detections[0].couleurs[0].modele.label, data["detections"][0]["couleurs"][0]["modele"]["label"])
        self.assertIs(image.detections[0].couleurs[0].modele.version, data["detections"][0]["couleurs"][0]["modele"]["version"])

        self.assertIs(image.detections[0].couleurs[0].label, data["detections"][0]["couleurs"][0]["label"])
        self.assertIs(image.detections[0].couleurs[0].label, data["detections"][0]["couleurs"][0]["label"])

        self.assertIs(image.ocr.score_ocr, data["ocr"]["score_ocr"])
        self.assertIs(image.ocr.label_ocr, data["ocr"]["label_ocr"])
        self.assertIs(image.ocr.score, data["ocr"]["score"])
        self.assertIs(image.ocr.label, data["ocr"]["label"])
        self.assertIs(image.ocr.bbox.xmin, data["ocr"]["bbox"]["xmin"])
        self.assertIs(image.ocr.bbox.xmax, data["ocr"]["bbox"]["xmax"])
        self.assertIs(image.ocr.bbox.ymin, data["ocr"]["bbox"]["ymin"])
        self.assertIs(image.ocr.bbox.ymax, data["ocr"]["bbox"]["ymax"])
        self.assertIs(image.ocr.modele.label, data["ocr"]["modele"]["label"])
        self.assertIs(image.ocr.modele.version, data["ocr"]["modele"]["version"])
        